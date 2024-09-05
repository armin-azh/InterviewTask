from datetime import timedelta, datetime
import numpy as np
from numpy.linalg import norm as l2norm


class FaceTracker:
    trk_id = 0

    def __init__(self, threshold=80.5, max_live_sec=10):
        super(FaceTracker, self).__init__()
        self.track_list = np.empty((0, 512))
        self.map_id = np.empty((0,), dtype=int)
        self.timestamps = np.empty((0,))

        self.threshold = threshold
        self.delta = timedelta(seconds=max_live_sec)

    @classmethod
    def generate_new_id(cls):
        tr_id = cls.trk_id
        cls.trk_id += 1
        return tr_id

    def update(self, embeds: np.ndarray):
        if len(embeds) > 0:
            norms = l2norm(embeds, axis=1)
            norms_idx = np.where(norms > 17.0)[0]
            embeddings = embeds[norms_idx, ...]
        else:
            return np.empty((0, 1)), []

        if len(self.track_list) == 0:
            # Initiate the tracker list
            self.track_list = np.concatenate([self.track_list, embeddings])
            self.map_id = np.concatenate([self.map_id, [self.generate_new_id() for _ in range(len(self.track_list))]])
            self.timestamps = np.concatenate(
                [self.timestamps, [datetime.now().timestamp() for _ in range(len(self.track_list))]])
            return np.array(self.map_id, dtype=int).reshape((-1, 1)), norms_idx
        else:
            track_id = []
            sim = np.dot(embeddings, self.track_list.T)
            max_sim_idx = np.argmax(sim, axis=1)
            max_sim = np.max(sim, axis=1)

            max_sim_po_idx = np.where(max_sim > self.threshold)[0]
            max_sim_ne_idx = np.where(max_sim <= self.threshold)[0]

            track_id += self.map_id[max_sim_idx[max_sim_po_idx]].tolist()
            self.track_list[max_sim_idx[max_sim_po_idx], :] = embeddings[max_sim_po_idx, :]  # Replace
            # modify the time stamp
            for idx in max_sim_idx[max_sim_po_idx]:
                self.timestamps[idx] = datetime.now().timestamp()

            prev_len = len(self.track_list)
            self.track_list = np.concatenate([self.track_list, embeddings[max_sim_ne_idx, :]])  # Add Negative Samples
            next_len = len(self.track_list)
            n_trk = [self.generate_new_id() for _ in range(prev_len, next_len)]
            self.map_id = np.concatenate([self.map_id, n_trk])
            self.timestamps = np.concatenate(
                [self.timestamps, [datetime.now().timestamp() for _ in range(prev_len, next_len)]])
            track_id += n_trk

            # prune some time exceeded entities
            no_exc_idx = []
            for idx, ts in enumerate(self.timestamps):
                ts = datetime.fromtimestamp(ts)
                if datetime.now() - ts < self.delta:
                    no_exc_idx.append(idx)

            if len(no_exc_idx) > 0:
                self.track_list = self.track_list[no_exc_idx, :]
                self.map_id = self.map_id[no_exc_idx]
                self.timestamps = self.timestamps[no_exc_idx]

            return np.array(track_id, dtype=int).reshape((-1, 1)), norms_idx