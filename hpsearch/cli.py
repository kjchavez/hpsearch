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
    trial_id = uuid.uuid4().hex
    FNULL = open(os.devnull, 'w')

    launcher = config.get('launcher', 'python')
    script = config['script']

    params = sampler.sample()
    trial = Trial(config['name'], trial_id, params)
    params['trial_id'] = trial_id
    args = ['--%s=%s' % (key, value) for key, value in params.items()]
    p = subprocess.Popen([launcher, script] + args) #,
                         #stdout=FNULL, stderr=FNULL)
    trial.set_pid(p.pid)
    print("PID:", p.pid)
    print(sampler.sample())


@cli.command()
@click.option("--name", type=str, default="")
def show_trials(name):
    for trial_dir in os.listdir(consts.TRIAL_METRICS_DIR):
        trial = Trial.from_trial_id(trial_dir)
        if trial.experiment_name.startswith(name):
            print("%s:%s = %0.4f" % (trial.experiment_name, trial.trial_id, trial.max_score()))

if __name__ == "__main__":
    cli()
