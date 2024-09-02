from typing import Tuple

import onnxruntime as ort
import numpy as np

__all__ = [
    'Detector'
]


def distance2bbox(points, distance, max_shape=None):
    """Decode distance prediction to bounding box.
    Args:
        points (Tensor): Shape (n, 2), [x, y].
        distance (Tensor): Distance from the given point to 4
            boundaries (left, top, right, bottom).
        max_shape (tuple): Shape of the image.
    Returns:
        Tensor: Decoded bboxes.
    """
    x1 = points[:, 0] - distance[:, 0]
    y1 = points[:, 1] - distance[:, 1]
    x2 = points[:, 0] + distance[:, 2]
    y2 = points[:, 1] + distance[:, 3]
    if max_shape is not None:
        x1 = x1.clamp(min=0, max=max_shape[1])
        y1 = y1.clamp(min=0, max=max_shape[0])
        x2 = x2.clamp(min=0, max=max_shape[1])
        y2 = y2.clamp(min=0, max=max_shape[0])
    return np.stack([x1, y1, x2, y2], axis=-1)


def distance2kps(points, distance, max_shape=None):
    """Decode distance prediction to bounding box.
    Args:
        points (Tensor): Shape (n, 2), [x, y].
        distance (Tensor): Distance from the given point to 4
            boundaries (left, top, right, bottom).
        max_shape (tuple): Shape of the image.
    Returns:
        Tensor: Decoded bboxes.
    """
    preds = []
    for i in range(0, distance.shape[1], 2):
        px = points[:, i % 2] + distance[:, i]
        py = points[:, i % 2 + 1] + distance[:, i + 1]
        if max_shape is not None:
            px = px.clamp(min=0, max=max_shape[1])
            py = py.clamp(min=0, max=max_shape[0])
        preds.append(px)
        preds.append(py)
    return np.stack(preds, axis=-1)


class Detector:
    def __init__(self, model_file: str, nms_thresh: float = .4, det_thresh: float = .5, min_res: float = 20,
                 input_size: Tuple[int, int] = (480, 640)) -> None:
        self.session = ort.InferenceSession(model_file, None,providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.center_cache = {}
        self.nms_thresh = nms_thresh
        self.det_thresh = det_thresh
        self.min_res = min_res

        self.input_name = self.session.get_inputs()[0].name
        self.input_size = input_size
        self.output_names = [o.name for o in self.session.get_outputs()]
        self.fmc = 3
        self.input_mean = 127.5
        self.input_std = 128.0
        self._feat_stride_fpn = [8, 16, 32]
        self._num_anchors = 2

    def forward(self, img: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        scores_list = []
        bboxes_list = []
        kps_list = []

        blob = cv2.dnn.blobFromImage(img, 1.0 / self.input_std, tuple(img.shape[0:2][::-1]),
                                     (self.input_mean, self.input_mean, self.input_mean), swapRB=True)
        net_outs = self.session.run(self.output_names, {self.input_name: blob})
        input_height = blob.shape[2]
        input_width = blob.shape[3]
        fmc = self.fmc

        for idx, stride in enumerate(self._feat_stride_fpn):
            scores = net_outs[idx]
            bbox_predicts = net_outs[idx + fmc]
            bbox_predicts = bbox_predicts * stride
            kps_predicts = net_outs[idx + fmc * 2] * stride
            height = input_height // stride
            width = input_width // stride
            key = (height, width, stride)
            if key in self.center_cache:
                anchor_centers = self.center_cache[key]
            else:
                anchor_centers = np.stack(np.mgrid[:height, :width][::-1], axis=-1).astype(np.float32)
                anchor_centers = (anchor_centers * stride).reshape((-1, 2))
                if self._num_anchors > 1:
                    anchor_centers = np.stack([anchor_centers] * self._num_anchors, axis=1).reshape((-1, 2))
                if len(self.center_cache) < 100:
                    self.center_cache[key] = anchor_centers
            # with size of anchors
            scores = scores[:len(anchor_centers)]
            bbox_predicts = bbox_predicts[:len(anchor_centers)]
            kps_predicts = kps_predicts[:len(anchor_centers)]
            pos_indices = np.where(scores >= self.det_thresh)[0]
            bboxes = distance2bbox(anchor_centers, bbox_predicts)
            pos_scores = scores[pos_indices]
            pos_bboxes = bboxes[pos_indices]
            scores_list.append(pos_scores)
            bboxes_list.append(pos_bboxes)
            key_points = distance2kps(anchor_centers, kps_predicts)
            key_points = key_points.reshape((key_points.shape[0], -1, 2))
            pos_key_points = key_points[pos_indices]
            kps_list.append(pos_key_points)

        scores = np.vstack(scores_list)
        bboxes_list = np.vstack(bboxes_list)
        kps_list = np.vstack(kps_list)

        return scores, bboxes_list, kps_list

    def detect(self, img: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:

        ref_size = img.shape[:2]
        img = cv2.resize(img, self.input_size[::-1])
        res_size = img.shape[:2]
        det_scale = (ref_size[0] / res_size[0], ref_size[1] / res_size[1])
        scores, boxes, points = self.forward(img)
        order = scores.ravel().argsort()[::-1]

        # Order
        scores = scores[order, :]
        boxes = boxes[order, :]
        points = points[order, :]

        # Scale
        boxes[:, [0, 2]] *= det_scale[1]
        boxes[:, [1, 3]] *= det_scale[0]
        points[:, :, [0]] *= det_scale[1]
        points[:, :, [1]] *= det_scale[0]

        keep_indices = self.nms(boxes, scores)

        # Keep
        scores = scores[keep_indices, :]
        boxes = boxes[keep_indices, :]
        points = points[keep_indices, :]

        # Keep min resolution
        if len(boxes) > 0:
            wh = boxes[:, [2, 3]] - boxes[:, [0, 1]]
            wh = wh[:, 0] * wh[:, 1]
            min_res_idx = np.where(wh > self.min_res)[0]
            scores = scores[min_res_idx, :]
            boxes = boxes[min_res_idx, :]
            points = points[min_res_idx, :]

        return scores, boxes, points

    def nms(self, boxes: np.ndarray, scores: np.ndarray):
        thresh = self.nms_thresh
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores.ravel().argsort()[::-1]
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            inds = np.where(ovr <= thresh)[0]
            order = order[inds + 1]

        return keep