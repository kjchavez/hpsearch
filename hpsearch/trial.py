from hpsearch import consts
import time
import os
import yaml

class Trial(object):
    def __init__(self, experiment_name, trial_id, params):
        self.trial_id = trial_id
        self.experiment_name = experiment_name
        self.trial_dir = os.path.join(consts.TRIAL_METRICS_DIR, trial_id)
        if not os.path.exists(self.trial_dir):
            os.makedirs(self.trial_dir)

        self._metadata_filename = os.path.join(self.trial_dir, "METADATA")
        if not os.path.exists(self._metadata_filename):
            with open(self._metadata_filename, 'w') as fp:
                yaml.dump({'experiment': experiment_name, 'trial_id': trial_id, 'start_time':
                           time.time()}, fp)

        self._scores_filename = os.path.join(self.trial_dir, "scores.txt")
        self._params_filename = os.path.join(self.trial_dir, "params.yaml")
        self.params = params
        with open(self._params_filename, 'w') as fp:
            yaml.dump(params, fp)

    @staticmethod
    def from_trial_id(trial_id):
        """ Attempts to restore all info from the trial directory. """
        trial_dir = os.path.join(consts.TRIAL_METRICS_DIR, trial_id)
        if not os.path.isdir(trial_dir):
            raise ValueError("Invalid trial id")

        with open(os.path.join(trial_dir, "params.yaml")) as fp:
            params = yaml.load(fp)

        with open(os.path.join(trial_dir, 'METADATA')) as fp:
            metadata = yaml.load(fp)

        return Trial(metadata['experiment'], trial_id, params)


    def add_score(self, score):
        with open(self._scores_filename, 'a') as fp:
            print("%0.3f:%f" % (time.time(), score), file=fp)

    def set_pid(self, pid):
        with open(os.path.join(self.trial_dir, 'pid'), 'w') as fp:
            print(pid, file=fp)

    def scores(self):
        if not os.path.exists(self._scores_filename):
            return []

        with open(self._scores_filename) as fp:
            data = fp.readlines()

        _scores = []
        for line in data:
            t, s = line.split(":", 1)
            _scores.append((float(t), float(s)))

        return _scores

