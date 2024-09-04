from typing import Tuple
import cv2
import math
import pickle
import onnxruntime as ort
import numpy as np
from skimage import transform as trans


def trans_points2d(pts, M):
    new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
    for i in range(pts.shape[0]):
        pt = pts[i]
        new_pt = np.array([pt[0], pt[1], 1.], dtype=np.float32)
        new_pt = np.dot(M, new_pt)
        new_pts[i] = new_pt[0:2]
    return new_pts


def trans_points3d(pts, M):
    scale = np.sqrt(M[0][0] * M[0][0] + M[0][1] * M[0][1])
    # print(scale)
    new_pts = np.zeros(shape=pts.shape, dtype=np.float32)
    for i in range(pts.shape[0]):
        pt = pts[i]
        new_pt = np.array([pt[0], pt[1], 1.], dtype=np.float32)
        new_pt = np.dot(M, new_pt)
        # print('new_pt', new_pt.shape, new_pt)
        new_pts[i][0:2] = new_pt[0:2]
        new_pts[i][2] = pts[i][2] * scale

    return new_pts


def trans_points(pts, M):
    if pts.shape[1] == 2:
        return trans_points2d(pts, M)
    else:
        return trans_points3d(pts, M)


def estimate_affine_matrix_3d23d(X, Y):
    X_homo = np.hstack((X, np.ones([X.shape[0], 1])))  # n x 4
    P = np.linalg.lstsq(X_homo, Y, rcond=None)[0].T  # Affine matrix. 3 x 4
    return P


def P2sRt(P):
    t = P[:, 3]
    R1 = P[0:1, :3]
    R2 = P[1:2, :3]
    s = (np.linalg.norm(R1) + np.linalg.norm(R2)) / 2.0
    r1 = R1 / np.linalg.norm(R1)
    r2 = R2 / np.linalg.norm(R2)
    r3 = np.cross(r1, r2)

    R = np.concatenate((r1, r2, r3), 0)
    return s, R, t


def matrix2angle(R):
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0
    rx, ry, rz = x * 180 / np.pi, y * 180 / np.pi, z * 180 / np.pi
    return rx, ry, rz


class Landmark:
    def __init__(self, model_file: str, lmk_file: str):
        self.input_mean = 127.5
        self.input_std = 128.0
        self.session = ort.InferenceSession(model_file, None, providers=['CUDAExecutionProvider',
                                                                         'CPUExecutionProvider'])

        input_cfg = self.session.get_inputs()[0]
        self.input_name = input_cfg.name
        self.input_size = tuple(input_cfg.shape[2:4][::-1])
        self.input_shape = input_cfg.shape
        self.output_names = [self.session.get_outputs()[0].name]
        self.lmk_dim = 3
        self.lmk_num = 68
        with open(lmk_file, 'rb') as f:
            self.mean_lmk = pickle.load(f)

    def get(self, img: np.ndarray, boxes: np.ndarray):
        if len(boxes) == 0:
            return np.empty((0, 3)), np.empty((0, 68, 2))
        wh = boxes[:, [2, 3]] - boxes[:, [0, 1]]
        ctr = (boxes[:, [2, 3]] + boxes[:, [0, 1]]) / 2
        scale = self.input_size[0] / (np.max(wh, axis=1) * 1.5)
        batched_images, affine = self.transform(img, ctr, scale, rotate=0.)
        batch = batched_images.shape[0]
        pred = self.session.run(self.output_names, {self.input_name: batched_images})[0]
        pred = pred.reshape((batch, -1, 3))
        pred = pred[:, self.lmk_num * -1:, :]
        pred[:, :, 0:2] += 1
        # pred[:, :, 0] *= im_scale[1]
        # pred[:, :, 1] *= im_scale[0]
        pred[:, :, 0:2] *= (self.input_size[0] // 2)
        pred[:, :, 2] *= (self.input_size[0] // 2)  # This could be merged with line above

        poses = self._get_pos(pred, affine)
        return poses, pred

    def _get_pos(self, pred: np.ndarray, affine: list) -> np.ndarray:
        poses = []
        for idx in range(len(pred)):
            m = affine[idx]
            land = pred[idx]
            im = cv2.invertAffineTransform(m)
            land = trans_points(land, im)
            P = estimate_affine_matrix_3d23d(self.mean_lmk, land)
            s, R, t = P2sRt(P)
            rx, ry, rz = matrix2angle(R)
            pose = np.array([rx, ry, rz], dtype=np.float32)
            poses.append(pose)

        return np.stack(poses, axis=0)

    def transform(self, img: np.ndarray, centers: np.ndarray, scales: np.ndarray, rotate: float) -> Tuple[
        np.ndarray, list]:
        images = []
        affine_matrices = []
        for idx in range(len(centers)):
            scale_ratio = scales[idx]
            center = centers[idx]
            rot = float(rotate) * np.pi / 180.0
            t1 = trans.SimilarityTransform(scale=scale_ratio)
            cx = center[0] * scale_ratio
            cy = center[1] * scale_ratio
            t2 = trans.SimilarityTransform(translation=(-1 * cx, -1 * cy))
            t3 = trans.SimilarityTransform(rotation=rot)
            t4 = trans.SimilarityTransform(translation=(self.input_size[0] / 2, self.input_size[0] / 2))
            t = t1 + t2 + t3 + t4
            M = t.params[0:2]
            cropped = cv2.warpAffine(img,
                                     M, self.input_size,
                                     borderValue=0.0)
            images.append(cropped)
            affine_matrices.append(M)

        return cv2.dnn.blobFromImages(images, 1 / self.input_std, self.input_size,
                                      [self.input_mean] * 3, swapRB=False), affine_matrices