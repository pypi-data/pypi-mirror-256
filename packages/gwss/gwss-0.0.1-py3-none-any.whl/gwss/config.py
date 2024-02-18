import os
import yaml
import pathlib
from pathlib import Path
from gwss.logger import logger


logger.debug("Creating and loading 'config' object")
# >>> Path.joinpath(Path.home(), '.gwss')
# PosixPath('/home/ken/.gwss')
config = yaml.safe_load(open(Path.joinpath(Path.home(), '.gwss'), 'r'))
logger.debug("Created 'config' object")
