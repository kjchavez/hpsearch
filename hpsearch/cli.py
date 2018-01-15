import click
import json
import yaml

from hpsearch import parameter

def is_valid(config):
    if 'name' not in config:
        print("Config must have a 'name'")
        return False
    if 'params' not in config or len(config['params']) == 0:
        print("Config must have 'params' list with at least one param")
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
    print(sampler.sample())

if __name__ == "__main__":
    cli()
