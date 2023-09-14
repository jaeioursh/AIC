import numpy as np
import warnings

class Behaviors:
    def __init__(self, p, st_size, act_size):
        self.p = p
        self.poi_types = 2
        self.v_e_vals = 2
        self.battery = np.zeros(self.p.time_steps)
        self.trajectory = np.zeros((2, self.p.time_steps))  # 2 for x & y position
        self.full_action = np.zeros((act_size, self.p.time_steps))  # 2 poi types, 4 sensors, 2 behaviors (v & e)
        self.full_st = np.zeros((st_size, self.p.time_steps))
        self.cf_vals = np.zeros((self.p.counter, self.p.time_steps))
        self.distill_action = np.zeros((2 + self.v_e_vals, self.p.time_steps))  # poi type (0 or 1), v, e, dist to closest poi
        self.bins = np.zeros((12, self.p.time_steps))

    def reset(self):
        self.battery = np.zeros_like(self.battery)
        self.trajectory = np.zeros_like(self.trajectory)
        self.full_action = np.zeros_like(self.full_action)
        self.full_st = np.zeros_like(self.full_st)
        self.cf_vals = np.zeros_like(self.cf_vals)
        self.distill_action = np.zeros_like(self.distill_action)
        self.bins = np.zeros_like(self.bins)

    def update(self, ts, st, act, pos, bins):
        self.battery[ts] = st[-1]
        self.full_st[:, ts] = st
        self.full_action[:, ts] = act
        self.trajectory[:, ts] = pos
        for i, b in enumerate(bins[0]):
            vals = [d for _, d in b]
            if vals:
                self.bins[i, ts] = min(vals)
            else:
                self.bins[i, ts] = np.nan

    def distilled_act(self):
        idx = np.argmax(self.full_action[:-2], axis=0)
        self.distill_action[0, :] = np.floor(idx / self.p.n_sensors).astype(int)
        self.distill_action[1:3, :] = self.full_action[-2:]
        self.distill_action[3, :] = np.nanmin(self.bins[:8, :], axis=0)

    def total_d(self):
        # calculates total euclidean distance traveled from trajectory, normalized for the max possible distance (speed * time)
        xy_ds = (self.trajectory[:, 0:-1] - self.trajectory[:, 1:]) ** 2
        return np.sum(np.sqrt(xy_ds[0, :] + xy_ds[1, :]) / self.p.speed) / self.p.time_steps

    def summary_stats(self):
        self.distilled_act()
        batt = [self.battery[-1]]
        dist = [self.total_d()]
        by_type_v_e = np.zeros((self.poi_types, self.v_e_vals))
        by_type_combo = np.zeros(self.poi_types)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            for p in range(self.poi_types):
                ve_vals = self.distill_action[1:3, self.distill_action[0] == p]
                by_type_v_e[p, :] = np.nan_to_num(np.mean(ve_vals, axis=1))
                by_type_combo[p] = np.nan_to_num(np.mean(ve_vals))
            by_type_v_e = by_type_v_e.flatten()
            by_v_or_e = np.mean(self.distill_action[1:3,:], axis=1)
            full_act = np.mean(self.full_action, axis=1)
        bh_dict = {'battery': batt, 'distance': dist, 'type sep': by_type_v_e, 'type combo': by_type_combo,
                   'v or e': by_v_or_e, 'full act': full_act}

        return bh_dict

    def get_beh(self, bh_strs):
        bh_d = self.summary_stats()
        vals = [val for key, val in bh_d.items() if key in bh_strs]
        return np.concatenate(vals)


if __name__ == '__main__':
    from pymap_elites_multiobjective.parameters import p200000 as param
    b = Behaviors(param, 5, 8)