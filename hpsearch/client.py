import os
import time

from hpsearch import consts
from hpsearch.trial import Trial

class HpsearchClient(object):
    def __init__(self, trial_id):
        self.trial = Trial.from_trial_id(trial_id)

    def record(self, score):
        try:
            score = float(score)
        except:
            raise TypeError("|score| must be castable to float")

        self.trial.add_score(score)
