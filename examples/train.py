import argparse
import hpsearch
import random
import time

parser = argparse.ArgumentParser()
parser.add_argument("--number", type=float, required=True)
parser.add_argument("--category", type=str, required=True)
parser.add_argument("--trial_id", required=True)
args = parser.parse_args()

score = 2.5*len(args.category) - abs(1 - args.number)
print(score)
hpsearch.record(args.trial_id, score)

# Add a really long delay sometimes.
if random.random() < 0.5:
    time.sleep(20)
