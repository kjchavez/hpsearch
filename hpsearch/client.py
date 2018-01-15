import os
import time

class HpsearchClient(object):
    TRIAL_METRIC_DIR = "/tmp/hpsearch"
    def __init__(self, trial_id):
        self.trial_id = trial_id
        if not os.path.exists(HpsearchClient.TRIAL_METRIC_DIR):
            os.makedirs(HpsearchClient.TRIAL_METRIC_DIR)

    def record(self, score):
        try:
            score = float(score)
        except:
            raise TypeError("|score| must be castable to float")

        with open(os.path.join(HpsearchClient.TRIAL_METRIC_DIR, self.trial_id), 'a') as fp:
            print("%0.3f:%f" % (time.time(), score), file=fp)

