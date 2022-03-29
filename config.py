import logging
from os import path
from logging.config import fileConfig
import yaml

fileConfig('logging_config.ini')
logger = logging.getLogger()
# logger.debug('often makes a very good meal of %s', 'visiting tourists')

# setting up host machine paths
filesdb_rootpath = "/home/jl/data/filebase"
project_path = "/home/jl/projects/bargainsniper/"

# Configured collections
with open(path.join(project_path, "collections.yml"), 'r') as stream:
    collections = yaml.safe_load(stream)
