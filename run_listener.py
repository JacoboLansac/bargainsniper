# Jacobo Lansac Nieto, Anemo Analytics, Python3
import numpy as np
import pandas as pd
import os
import config
from src.listener import OpenseaListener

listener = OpenseaListener()

collections = []

while True:
    for slug, contrat_address in config.collections['Opensea'].items():
        listener.run(contrat_address)
