# Jacobo Lansac Nieto, Anemo Analytics, Python3
import numpy as np
import pandas as pd
import time
import os
import bconfig
from src.listener import OpenseaListener

listener = OpenseaListener()

collections = []
last_timestamp = None

while True:
    for slug, contrat_address in config.collections['Opensea'].items():

        listener.run(contrat_address, last_timestamp)
        last_timestamp = time.time()
