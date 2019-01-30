import argparse
import os

import pyhocon

from . import converter
from ..logging import experiment_path, logger

__all__ = [
    'config'
]

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='path to config file')
args, _ = parser.parse_known_args()

config = pyhocon.ConfigFactory.parse_file(args.config)

config_parser = argparse.ArgumentParser()
for key in converter.compact_keys(config):
    config_parser.add_argument(f'--{key}')

config_args, _ = config_parser.parse_known_args()

# Replace config
for key, value in config_args.__dict__.items():
    if value is not None:
        logger.info(f'Replace: {key} => {value}')
        config[key] = value

with open(os.path.join(experiment_path, 'config.conf'), 'w') as f:
    f.write(pyhocon.HOCONConverter.to_hocon(config))
