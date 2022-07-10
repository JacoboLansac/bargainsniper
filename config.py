import logging
import os
from os import path
import platform
import yaml
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.config import fileConfig

# Project root path
project_path = path.dirname(__file__)
logpath = path.join(project_path, 'logs')
os.makedirs(logpath, exist_ok=True)

# Logger configuration
# fileConfig('logging_config.ini')
# logger = logging.getLogger()
logger = logging.getLogger('')
logger.setLevel(logging.INFO)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
# File rotating handler
filerotatingHandler = TimedRotatingFileHandler(path.join(logpath, 'run.log'), when="d", interval=1, backupCount=5)
filerotatingHandler.setLevel(logging.INFO)
filerotatingHandler.setFormatter(formatter)
logger.addHandler(filerotatingHandler)

# Database path for filesdb
filesdb_rootpath = path.join(path.expanduser('~'), 'data', 'filebase')
os.makedirs(filesdb_rootpath, exist_ok=True)


# Configured collections
if platform.node() == 'jl-ThinkBook':
    environment = 'test'
elif platform.node() == 'jacoserver-droplet':
    environment = 'prod'
else:
    raise ValueError("platform not contemplated")

with open(path.join(project_path, "collections.yml"), 'r') as stream:
    collections = yaml.safe_load(stream)[environment]
