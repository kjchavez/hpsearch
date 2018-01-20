import os

HPSEARCH_DIR = os.path.join(os.path.expanduser('~'), 'var', 'hpsearch')
TRIAL_METRICS_DIR = os.path.join(HPSEARCH_DIR, "trials")

# Goals
MAXIMIZE = 'MAXIMIZE'
MINIMIZE = 'MINIMIZE'
