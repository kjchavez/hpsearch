import click
import json
import yaml
import uuid
import os
import subprocess

from hpsearch import parameter
from hpsearch import consts
from hpsearch.trial import Trial

def is_valid(config):
    if 'name' not in config:
        print("Config must have a 'name'")
        return False
    if 'params' not in config or len(config['params']) == 0:
        print("Config must have 'params' list with at least one param")
        return False
    if 'script' not in config:
        print("Config must have a 'script'")
        return False

    return True

def load_config_file(config_file):
    valid_yaml = True
    valid_json = True
    with open(config_file) as fp:
        try:
             config = yaml.load(fp)
        except:
            valid_yaml = False

    if not valid_yaml:
        with open(config_file) as fp:
            try:
                config = json.load(fp)
            except:
                valid_json = False

    if not valid_yaml and not valid_json:
        raise ValueError("Config is not in YAML or JSON format.")

    return config

def parse_duration(duration_str):
    """ Parses string durations into an integer number of seconds.

    Supported format (as regex): [0-9]+[smh]
    """
    unit = duration_str[-1]
    if unit not in ('s', 'm', 'h'):
        raise ValueError("Invalid duration string")
    multiplier = { 's': 1, 'm': 60, 'h': 3600 }
    return int(duration_str[0:-1])*multiplier[unit]

@click.group()
def cli():
    pass

@cli.command()
@click.argument("config_file", type=click.Path(exists=True))
def run(config_file):
    config = load_config_file(config_file)
    if not is_valid(config):
        return

    print("Running hyperparameter search with configuration:")
    print(json.dumps(config, indent=2))
    sampler = parameter.MultiParameterSampler(config['params'])
    launcher = config.get('launcher', 'python')
    script = config['script']

    samples = [sampler.sample() for _ in range(config['maxTrials'])]
    # Run them sequentially for now.
    if config['maxParallelTrials'] > 1:
        print("Parallel trials not yet supported. Running sequentially")

    for x in samples:
        trial_id = uuid.uuid4().hex
        trial = Trial(config, trial_id, x)
        stdout = open(trial.stdout(), 'a');
        stderr = open(trial.stderr(), 'a');
        args = ['--%s=%s' % (key, value) for key, value in x.items()]
        args.append('--trial_id=%s' % trial_id)
        p = subprocess.Popen([launcher, script] + args,
                             stdout=stdout, stderr=stderr)
        trial.set_pid(p.pid)
        print("Running trial with pid=%s" % p.pid)
        print("Params=", json.dumps(x))

        # Wait some max run time, then KILL the process.
        timeout = parse_duration(config['maxTrialTime'])
        try:
            p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            print("Trial exceeded timeout. Terminating")
            p.terminate()

@cli.command()
@click.option("--name", type=str, default="")
def show_trials(name):
    for trial_dir in os.listdir(consts.TRIAL_METRICS_DIR):
        trial = Trial.from_trial_id(trial_dir)
        if trial.experiment_name.startswith(name):
            print("%s:%s = %0.4f" % (trial.experiment_name, trial.trial_id, trial.max_score()))

@cli.command()
@click.option("--max_trials", type=int, default=10, help="How many trials to show per experiment")
def show(max_trials):
    experiments = {}
    for trial_dir in os.listdir(consts.TRIAL_METRICS_DIR):
        try:
            trial = Trial.from_trial_id(trial_dir)
        except:
            print("Failed to read trial", trial_dir)
            continue

        if trial.experiment_name not in experiments:
            experiments[trial.experiment_name] = []
        experiments[trial.experiment_name].append(trial)

    for name, trials in experiments.items():
        goal = trials[0].experiment['goal']
        print("="*80)
        print("{:<30} ({} trials)   {}".format(name, len(trials), goal))
        print("="*80)
        scored_trials = sorted((trial.best_score(), trial) for trial in trials)
        if goal == consts.MAXIMIZE:
            scored_trials.reverse()
        for score, trial in scored_trials[0:max_trials]:
            params_str = json.dumps(trial.params)
            if len(params_str) > 38:
                params_str = params_str[0:35] + "..."
            print("{:.8}...  best_score={:<7.4f}  params={}".format(trial.trial_id, score,
                                                                         params_str))

if __name__ == "__main__":
    cli()
