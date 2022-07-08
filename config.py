import logging
import os
from os import path
from logging.config import fileConfig
import yaml

fileConfig(path.join(path.dirname(__file__), 'logging_config.ini'))
logger = logging.getLogger()
# logger.debug('often makes a very good meal of %s', 'visiting tourists')

# setting up host machine paths
filesdb_rootpath = path.join(path.expanduser('~'), 'data', 'filebase')
project_path = path.dirname(__file__)

os.makedirs(filesdb_rootpath, exist_ok=True)


# Configured collections
with open(path.join(project_path, "collections.yml"), 'r') as stream:
    collections = yaml.safe_load(stream)
