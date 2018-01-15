import hpsearch.client

def record(trial_id, score):
    c = client.HpsearchClient(trial_id)
    c.record(score)
