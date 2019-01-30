import argparse
import logging
import os
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument('--logdir', default='experiments')
parser.add_argument('--experiment', default='DEFAULT')
args, _ = parser.parse_known_args()

timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime())
experiment_path = os.path.join(args.logdir, f'{timestamp}_{args.experiment}')
os.makedirs(experiment_path)

logger = logging.getLogger("torchlearning")

formatter = logging.Formatter(
    "%(asctime)s %(levelname)-8s: %(message)s"
)

file_handler = logging.FileHandler(os.path.join(experiment_path, "training.log"))
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.setLevel(logging.DEBUG)

__all__ = [
    "logger",
    "experiment_path"
]
