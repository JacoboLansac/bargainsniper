import logging
from logging.config import fileConfig

fileConfig('logging_config.ini')
logger = logging.getLogger()
# logger.debug('often makes a very good meal of %s', 'visiting tourists')

# Database
filesdb_rootpath = '/home/jl/data/filebase'
