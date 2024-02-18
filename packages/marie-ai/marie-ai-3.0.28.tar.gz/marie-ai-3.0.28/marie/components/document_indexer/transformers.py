import os
from typing import Any, Callable, List, Optional, Tuple, Union

import numpy as np
import torch
import torch.nn as nn
from docarray import DocList
from PIL import Image, ImageDraw
from torch.nn import Module
from transformers import (
    AutoModelForTokenClassification,
    LayoutLMv3FeatureExtractor,
    LayoutLMv3Processor,
    LayoutLMv3TokenizerFast,
)

from marie.components.document_indexer.base import BaseDocumentIndexer
from marie.constants import __model_path__
from marie.executor.ner.utils import (
    draw_box,
    get_font,
    get_random_color,
    unnormalize_box,
    visualize_extract_kv,
)
from marie.logging.logger import MarieLogger
from marie.models.utils import initialize_device_settings
from marie.utils.overlap import find_overlap_horizontal, merge_bboxes_as_block

from ...api.docs import BatchableMarieDoc, MarieDoc
from ...boxes.line_processor import find_line_number
from ...logging.profile import TimeContext
from ...ocr import CoordinateFormat
from ...registry.model_registry import ModelRegistry
from ...utils.docs import frames_from_docs
from ...utils.json import load_json_file
from ...utils.utils import ensure_exists


class TransformersDocumentIndexer(BaseDocumentIndexer):
    """
    Transformer based model for document indexing(Named Entity Recognition) using the HuggingFace's transformers framework
    (https://github.com/huggingface/transformers).
    """

    def __init__(
        self,
        model_name_or_path: Union[str, os.PathLike],
        model_version: Optional[str] = None,
        tokenizer: Optional[str] = None,
        use_gpu: bool = True,
        top_k: Optional[int] = 1,
        task: str = "transformers-document-indexer",
        batch_size: int = 16,
        use_auth_token: Optional[Union[str, bool]] = None,
        devices: Optional[List[Union[str, "torch.device"]]] = None,
        show_error: Optional[Union[str, bool]] = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.logger = MarieLogger(self.__class__.__name__).logger
        self.logger.info(f"Document indexer : {model_name_or_path}")
        self.show_error = show_error  # show prediction errors
        self.batch_size = batch_size
        self.task = task

        self.logger.info(f"NER Extraction component : {model_name_or_path}")

        resolved_devices, _ = initialize_device_settings(
            devices=devices, use_cuda=use_gpu, multi_gpu=False
        )
        if len(resolved_devices) > 1:
            self.logger.warning(
                "Multiple devices are not supported in %s inference, using the first device %s.",
                self.__class__.__name__,
                resolved_devices[0],
            )
        self.device = resolved_devices[0]

        registry_kwargs = {
            "__model_path__": __model_path__,
            "use_auth_token": use_auth_token,
        }

        model_name_or_path = ModelRegistry.get(
            model_name_or_path,
            version=None,
            raise_exceptions_for_missing_entries=True,
            **registry_kwargs,
        )
        assert os.path.exists(model_name_or_path)
        self.logger.info(f"Resolved model : {model_name_or_path}")

        ensure_exists("/tmp/tensors")
        ensure_exists("/tmp/tensors/json")

        # TODO: config could be loaded from a file or passed as a parameter
        config_path = os.path.join(model_name_or_path, "marie.json")
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                "Expected config 'marie.json' not found in model directory"
            )

        self.logger.info(f"NER loading from : {config_path}")
        self.init_configuration = load_json_file(config_path)

        self.debug_visuals = self.init_configuration["debug"]["visualize"]["enabled"]
        self.debug_visuals_overlay = self.init_configuration["debug"]["visualize"][
            "overlay"
        ]
        self.debug_visuals_icr = self.init_configuration["debug"]["visualize"]["icr"]
        self.debug_visuals_ner = self.init_configuration["debug"]["visualize"]["ner"]
        self.debug_visuals_prediction = self.init_configuration["debug"]["visualize"][
            "prediction"
        ]

        self.debug_scores = self.init_configuration["debug"]["scores"]
        self.debug_colors = self.init_configuration["debug"]["colors"]

        self.labels = self.init_configuration["labels"]

        self.model = self.__load_model(
            model_name_or_path, self.labels, self.device.type
        )
        self.processor = self.__create_processor()

    def __create_processor(self):
        """prepare for the model"""
        # Method:2 Create Layout processor with custom future extractor
        # Max model size is 512, so we will need to handle any documents larger than that
        feature_extractor = LayoutLMv3FeatureExtractor(
            apply_ocr=False, do_resize=True, resample=Image.BILINEAR
        )
        tokenizer = LayoutLMv3TokenizerFast.from_pretrained(
            "microsoft/layoutlmv3-large",
            only_label_first_subword=False,
        )

        processor = LayoutLMv3Processor(
            feature_extractor=feature_extractor, tokenizer=tokenizer
        )

        return processor

    def __load_model(self, model_dir: str, labels: list[str], device: str):
        """
        Create token classification model
        """
        labels, id2label, label2id = self.get_label_info(labels)
        model = AutoModelForTokenClassification.from_pretrained(
            model_dir, num_labels=len(labels), label2id=label2id, id2label=id2label
        )

        model.eval()
        model.to(device)

        return model

    def optimize_model(self, model: nn.Module) -> Callable | Module:
        """Optimizes the model for inference. This method is called by the __init__ method."""
        if True:
            return model
        try:
            with TimeContext("Compiling model", logger=self.logger):
                # Optimize model for Inference time
                for param in model.parameters():
                    param.grad = None
                print("**** COMPILING NER Model***")
                import torch._dynamo as dynamo

                # Default torchinductor causes OOM when running on 24GB GPU, cache memory is never relased
                # Switching to use cudagraphs
                # torch._dynamo.config.set("inductor", "cache_memory", 0)
                # mode options: default, reduce-overhead, max-autotune
                # default, reduce-overhead, max-autotune
                # ['aot_ts_nvfuser', 'cudagraphs', 'inductor', 'ipex', 'nvprims_nvfuser', 'onnxrt', 'tensorrt', 'tvm']

                model = torch.compile(
                    model, mode="max-autotune", fullgraph=True, backend="cudagraphs"
                )
                print("**** COMPILED ***")

                return model
        except Exception as err:
            self.logger.warning(f"Model compile not supported: {err}")
            return model

    def get_label_info(self, labels: list[str]):
        self.logger.debug(f"Labels : {labels}")

        id2label = {v: k for v, k in enumerate(labels)}
        label2id = {k: v for v, k in enumerate(labels)}

        return labels, id2label, label2id

    def _filter(
        self, values: List[Any], probabilities: List[float], threshold: float
    ) -> List[Any]:
        return [
            value for probs, value in zip(probabilities, values) if probs >= threshold
        ]

    def predict(
        self,
        documents: DocList[MarieDoc],
        words: Optional[List[List[str]]] = None,
        boxes: Optional[List[List[List[int]]]] = None,
        batch_size: Optional[int] = None,
    ) -> DocList[MarieDoc]:
        if batch_size is None:
            batch_size = self.batch_size

        if len(documents) == 0:
            return documents

        if self.task == "transformers-document-indexer":
            assert (
                words is not None and boxes is not None
            ), "words and boxes must be provided for sequence classification"
            assert (
                len(documents) == len(words) == len(boxes)
            ), "documents, words and boxes must have the same length"

        # create a named tuple of (document, words, boxes) for each document

        batchable_docs = DocList(
            BatchableMarieDoc(
                tensor=doc.tensor,
                words=word,
                boxes=box,
            )
            for doc, word, box in zip(documents, words, boxes)
        )

        labels = self.labels
        frames = frames_from_docs(batchable_docs)
        for batchable_doc, frame in zip(batchable_docs, frames):
            t = batchable_doc.tensor
            w = batchable_doc.words
            b = batchable_doc.boxes
            self.logger.info(f"Batchable Doc : {frame.shape}")

            # Perform inference
            self.logger.info(f"Performing inference")
            # convert tensor to PIL image
            z = t.astype(np.uint8)  # .transpose(1, 2, 0)
            frame = Image.fromarray(z)
            r = self.inference(
                image=frame, words=w, boxes=b, labels=labels, threshold=0.5
            )

        results = DocList[MarieDoc]()
        return results

    def inference(
        self,
        image: Any,
        words: List[Any],
        boxes: List[Any],
        labels: List[str],
        threshold: float,
    ) -> Tuple[List, List, List]:
        """Run Inference on the model with given processor"""
        self.logger.info(f"Performing inference")
        model = self.model
        processor = self.processor
        device = self.device

        labels, id2label, label2id = self.get_label_info(labels)
        os.environ["TOKENIZERS_PARALLELISM"] = "true"
        self.logger.info(
            f"Tokenizer parallelism: {os.environ.get('TOKENIZERS_PARALLELISM', 'true')}"
        )

        width, height = image.size
        # partition the words and boxes into batches of 512 tokens with 128 stride
        # stride is the number of tokens to move forward, this is to handle long documents that are larger than 512 tokens
        # there will be overlap between the batches, so we will need to handle that later

        self.logger.info("Named Entity Inference")
        self.logger.info(f"Words : {len(words)} ::  {words}")
        self.logger.info(f"Boxes : {len(boxes)}")
        assert len(words) == len(boxes)

        encoding = processor(
            # fmt: off
            image,
            words,
            boxes=boxes,
            truncation=True,
            return_offsets_mapping=True,
            return_overflowing_tokens=True,
            stride=128,
            padding="max_length",
            return_tensors="pt",
            max_length=512,
            # fmt: on
        )

        offset_mapping_batched = encoding.pop("offset_mapping")
        overflow_to_sample_mapping = encoding.pop("overflow_to_sample_mapping")
        # encoding["pixel_values"] = torch.stack(encoding["pixel_values"], dim=0)

        # Debug tensor info
        self.debug_visuals = True
        if self.debug_visuals:
            img_tensor = encoding["pixel_values"]
            img = Image.fromarray(
                (img_tensor[0].cpu()).numpy().astype(np.uint8).transpose(1, 2, 0)
            )
            img.save(f"/tmp/tensors/tensor.png")

        # ensure proper device placement
        for k in encoding.keys():
            if k != "pixel_values":
                encoding[k] = encoding[k].to(device)
            else:
                encoding[k] = torch.cat([x.unsqueeze(0) for x in encoding[k]]).to(
                    device
                )

        # Perform forward pass
        with torch.inference_mode():
            outputs = model(**encoding)
            # Get the predictions and probabilities
            probs = (
                nn.softmax(outputs.logits.squeeze(), dim=1).max(dim=1).values.tolist()
            )
            # The model outputs logits of shape (batch_size, seq_len, num_labels).
            logits = outputs.logits
            batch_size, seq_len, num_labels = logits.shape
            # Get the predictions and bounding boxes by batch and convert to list
            predictions_batched = logits.argmax(-1).squeeze().tolist()
            token_boxes_batched = encoding.bbox.squeeze().tolist()
            normalized_logits_batched = (
                outputs.logits.softmax(dim=-1).squeeze().tolist()
            )

            # If batch size is 1, convert to list
            if batch_size == 1:
                predictions_batched = [predictions_batched]
                token_boxes_batched = [token_boxes_batched]
                normalized_logits_batched = [normalized_logits_batched]

            out_prediction = []
            out_boxes = []
            out_scores = []

            for batch_index in range(batch_size):
                # Get the predictions and bounding boxes for the current batch
                predictions = predictions_batched[batch_index]
                token_boxes = token_boxes_batched[batch_index]
                normalized_logits = normalized_logits_batched[batch_index]
                offset_mapping = offset_mapping_batched[batch_index]

                # TODO : Filer the results
                # Filter the predictions and bounding boxes based on a threshold
                # predictions = _filter(_predictions, probs, threshold)
                # token_boxes = _filter(_token_boxes, probs, threshold)

                # Only keep non-subword predictions
                is_subword = np.array(offset_mapping.squeeze().tolist())[:, 0] != 0

                true_predictions = [
                    id2label[pred]
                    for idx, pred in enumerate(predictions)
                    if not is_subword[idx]
                ]

                true_boxes = [
                    unnormalize_box(box, width, height)
                    for idx, box in enumerate(token_boxes)
                    if not is_subword[idx]
                ]
                # convert boxes from float to int
                true_boxes = [[int(b) for b in box] for box in true_boxes]

                true_scores = [
                    round(normalized_logits[idx][val], 6)
                    for idx, val in enumerate(predictions)
                    if not is_subword[idx]
                ]

                assert len(true_predictions) == len(true_boxes) == len(true_scores)

                # Not sure why we have this, but we need to remove [0, 0, 0, 0] boxes
                true_predictions = [
                    pred
                    for pred, box in zip(true_predictions, true_boxes)
                    if box != [0, 0, 0, 0]
                ]
                true_boxes = [box for box in true_boxes if box != [0, 0, 0, 0]]
                true_scores = [
                    score
                    for score, box in zip(true_scores, true_boxes)
                    if box != [0, 0, 0, 0]
                ]

                # check if there are duplicate boxes (example : 159000444_1.png)
                # why are there duplicate boxes??
                for box in true_boxes:
                    if true_boxes.count(box) > 1:
                        self.logger.warning(f"Duplicate box found : {box}")
                        current_idx = true_boxes.index(box)
                        true_predictions.pop(current_idx)
                        true_boxes.pop(current_idx)
                        true_scores.pop(current_idx)

                if batch_index > 0:
                    for idx, box in enumerate(out_boxes):
                        if box in true_boxes:
                            current_idx = true_boxes.index(box)
                            if true_scores[current_idx] >= out_scores[idx]:
                                out_prediction[idx] = true_predictions[current_idx]
                                out_scores[idx] = true_scores[current_idx]

                            true_predictions.pop(current_idx)
                            true_boxes.pop(current_idx)
                            true_scores.pop(current_idx)

                out_prediction.extend(true_predictions)
                out_boxes.extend(true_boxes)
                out_scores.extend(true_scores)

        original_boxes = []
        for box in boxes:
            original_boxes.append([int(b) for b in unnormalize_box(box, width, height)])

        # align words and boxes with predictions and scores
        out_prediction, out_boxes, out_scores = self.align_predictions(
            words, original_boxes, out_prediction, out_boxes, out_scores
        )

        assert len(out_prediction) == len(words)
        return out_prediction, out_boxes, out_scores

    def align_predictions(
        self,
        words,
        original_boxes: [],
        out_prediction: [],
        out_boxes: [],
        out_scores: [],
    ):
        """Align predictions with words and boxes"""

        aligned_prediction = []
        aligned_boxes = []
        aligned_scores = []

        for idx, word in enumerate(words):
            box = original_boxes[idx]
            if box in out_boxes:
                current_idx = out_boxes.index(box)
                aligned_prediction.append(out_prediction[current_idx])
                aligned_boxes.append(out_boxes[current_idx])
                aligned_scores.append(out_scores[current_idx])
            else:
                raise ValueError(f"Box not found for alignment: {box}")

        return aligned_prediction, aligned_boxes, aligned_scores

    def postprocess(self, frames, annotations, ocr_results, file_hash):
        """Post-process extracted data"""
        assert len(annotations) == len(ocr_results) == len(frames)
        for k, _image in enumerate(frames):
            if not isinstance(_image, Image.Image):
                raise "Frame should have been an PIL.Image instance"

        # need to normalize all data from XYXY to XYWH as the NER process required XYXY and assets were saved XYXY format
        self.logger.debug("Changing coordinate format from xyxy->xywh")

        for data in ocr_results:
            for word in data["words"]:
                word["box"] = CoordinateFormat.convert(
                    word["box"], CoordinateFormat.XYXY, CoordinateFormat.XYWH
                )

        for data in annotations:
            for i, box in enumerate(data["boxes"]):
                box = CoordinateFormat.convert(
                    box, CoordinateFormat.XYXY, CoordinateFormat.XYWH
                )
                data["boxes"][i] = box

        aggregated_ner = []
        aggregated_kv = []
        aggregated_meta = []

        # expected NER and key/value pairs
        expected_ner = self.init_configuration["expected_ner"]
        expected_keys = self.init_configuration["expected_keys"]
        expected_pair = self.init_configuration["expected_pair"]

        for i, (ocr, annotation, frame) in enumerate(
            zip(ocr_results, annotations, frames)
        ):
            self.logger.info(f"Processing page # {i}")
            # lines and boxes are already in the right reading order TOP->BOTTOM, LEFT-TO-RIGHT so no need to sort
            lines_bboxes = np.array(ocr["meta"]["lines_bboxes"])
            true_predictions = annotation["predictions"]
            true_boxes = annotation["boxes"]
            true_scores = annotation["scores"]

            viz_img = frame.copy()
            draw = ImageDraw.Draw(viz_img, "RGBA")
            font = get_font(14)
            # aggregate prediction by their line numbers

            groups = {}
            for pred_idx, (prediction, pred_box, pred_score) in enumerate(
                zip(true_predictions, true_boxes, true_scores)
            ):
                # discard 'O' other
                label = prediction[2:]
                if not label:
                    continue
                # two labels that need to be removed [0.0, 0.0, 0.0, 0.0]  [2578.0, 3 3292.0, 0.0, 0.0]
                if np.array_equal(pred_box, [0.0, 0.0, 0.0, 0.0]) or (
                    pred_box[2] == 0 and pred_box[3] == 0
                ):
                    continue

                line_number = find_line_number(lines_bboxes, pred_box)
                if line_number not in groups:
                    groups[line_number] = []
                groups[line_number].append(pred_idx)

            # aggregate boxes into key/value pairs via simple state machine for each line
            aggregated_keys = {}

            for line_idx, line_box in enumerate(lines_bboxes):
                if line_idx not in groups:
                    self.logger.debug(
                        f"Line does not have any groups : {line_idx} : {line_box}"
                    )
                    continue

                prediction_indexes = np.array(groups[line_idx])
                line_aggregator = []

                for key in expected_keys:
                    spans = []
                    skip_to = -1
                    for m in range(0, len(prediction_indexes)):
                        if skip_to != -1 and m <= skip_to:
                            continue
                        pred_idx = prediction_indexes[m]
                        prediction = true_predictions[pred_idx]
                        label = prediction[2:]
                        aggregator = []

                        if label == key:
                            for n in range(m, len(prediction_indexes)):
                                pred_idx = prediction_indexes[n]
                                prediction = true_predictions[pred_idx]
                                label = prediction[2:]
                                if label != key:
                                    break
                                aggregator.append(pred_idx)
                                skip_to = n

                        if len(aggregator) > 0:
                            spans.append(aggregator)

                    if len(spans) > 0:
                        line_aggregator.append({"key": key, "groups": spans})

                true_predictions = np.array(true_predictions)
                true_boxes = np.array(true_boxes)
                true_scores = np.array(true_scores)

                for line_agg in line_aggregator:
                    field = line_agg["key"]
                    group_indexes = line_agg["groups"]

                    for group_index in group_indexes:
                        bboxes = true_boxes[group_index]
                        scores = true_scores[group_index]
                        group_score = round(np.average(scores), 6)
                        # create a bounding box around our blocks which could be possibly overlapping or being split
                        group_bbox = merge_bboxes_as_block(bboxes)

                        key_result = {
                            "line": line_idx,
                            "key": field,
                            "bbox": group_bbox,
                            "score": group_score,
                        }

                        if line_idx not in aggregated_keys:
                            aggregated_keys[line_idx] = []
                        aggregated_keys[line_idx].append(key_result)

                        if self.debug_visuals:
                            color_map = self.init_configuration["debug"]["colors"]
                            color = (
                                color_map[field]
                                if field in color_map
                                else get_random_color()
                            )

                            draw_box(
                                draw,
                                group_bbox,
                                None,
                                color,
                                font,
                            )

            # check if we have possible overlaps when there is a mislabeled token, this could be a flag
            # Strategy used here is a horizontal overlap, if we have it then we will aggregate them
            # B-PAN I-PAN I-PAN B-PAN-ANS I-PAN
            if self.init_configuration["mislabeled_token_strategy"] == "aggregate":
                for key in expected_keys:
                    for ag_key in aggregated_keys.keys():
                        row_items = aggregated_keys[ag_key]
                        bboxes = [row["bbox"] for row in row_items if row["key"] == key]
                        visited = [False for _ in range(0, len(bboxes))]
                        to_merge = {}

                        for idx in range(0, len(bboxes)):
                            if visited[idx]:
                                continue
                            visited[idx] = True
                            box = bboxes[idx]
                            overlaps, indexes, scores = find_overlap_horizontal(
                                box, bboxes
                            )
                            to_merge[ag_key] = [idx]

                            for _, overlap_idx in zip(overlaps, indexes):
                                visited[overlap_idx] = True
                                to_merge[ag_key].append(overlap_idx)

                        for _k, idxs in to_merge.items():
                            items = aggregated_keys[_k]
                            items = np.array(items)
                            # there is nothing to merge, except the original block
                            if len(idxs) == 1:
                                continue

                            idxs = np.array(idxs)
                            picks = items[idxs]
                            remaining = np.delete(items, idxs)

                            score_avg = round(
                                np.average([item["score"] for item in picks]), 6
                            )
                            block = merge_bboxes_as_block(
                                [item["bbox"] for item in picks]
                            )

                            new_item = picks[0]
                            new_item["score"] = score_avg
                            new_item["bbox"] = block

                            aggregated_keys[_k] = np.concatenate(
                                ([new_item], remaining)
                            )

            # expected fields groups that indicate that the field could have been present
            # but it might not have been associated with KV pair mapping, does not apply to NER

            possible_fields = self.init_configuration["possible_fields"]
            possible_field_meta = {}

            for field in possible_fields.keys():
                fields = possible_fields[field]
                possible_field_meta[field] = {"page": i, "found": False, "fields": []}
                for k in aggregated_keys.keys():
                    ner_keys = aggregated_keys[k]
                    for ner_key in ner_keys:
                        key = ner_key["key"]
                        if key in fields:
                            possible_field_meta[field]["found"] = True
                            possible_field_meta[field]["fields"].append(key)

            aggregated_meta.append({"page": i, "fields": possible_field_meta})

            # Aggregate KV pairs, this can overlap with NER tags so caution need to be taken
            for pair in expected_pair:
                expected_question = pair[0]
                expected_answer = pair[1]

                for k in aggregated_keys.keys():
                    ner_keys = aggregated_keys[k]

                    found_key = None
                    found_val = None

                    for ner_key in ner_keys:
                        key = ner_key["key"]
                        if expected_question == key:
                            found_key = ner_key
                            continue
                        # find the first match
                        if found_key is not None and found_val is None:
                            # find the first match
                            for exp_key in expected_answer:
                                if key in exp_key:
                                    found_val = ner_key
                                    break

                            if found_val is not None:
                                bbox_q = found_key["bbox"]
                                bbox_a = found_val["bbox"]

                                if bbox_a[0] < bbox_q[0]:
                                    self.logger.warning(
                                        "Answer is not on the right of question"
                                    )
                                    continue

                                category = found_key["key"]
                                kv_result = {
                                    "page": i,
                                    "category": category,
                                    "value": {
                                        "question": found_key,
                                        "answer": found_val,
                                    },
                                }

                                aggregated_kv.append(kv_result)

            # Collect NER tags
            for tag in expected_ner:
                for k in aggregated_keys.keys():
                    ner_keys = aggregated_keys[k]
                    for ner_key in ner_keys:
                        key = ner_key["key"]
                        if key == tag:
                            ner_result = {
                                "page": i,
                                "category": tag,
                                "value": {
                                    "answer": ner_key,
                                },
                            }
                            aggregated_ner.append(ner_result)

            if self.debug_visuals and self.debug_visuals_overlay:
                viz_img.save(f"/tmp/tensors/extract_{file_hash}_{i}.png")

        # TODO : IS THIS NEEDED ANYMORE ???
        # self.decorate_aggregates_with_text(aggregated_ner, frames)
        # self.decorate_aggregates_with_text(aggregated_kv, frames)

        # visualize results per page
        if self.debug_visuals and self.debug_visuals_ner:
            for k in range(0, len(frames)):
                output_filename = f"/tmp/tensors/ner_{file_hash}_{k}.png"
                items = []
                items.extend([row for row in aggregated_kv if int(row["page"]) == k])
                items.extend([row for row in aggregated_ner if int(row["page"]) == k])
                visualize_extract_kv(output_filename, frames[k], items)

        results = {
            "meta": aggregated_meta,
            "kv": aggregated_kv,
            "ner": aggregated_ner,
        }
        self.logger.debug(f" results : {results}")
        return results
