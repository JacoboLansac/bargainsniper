import numpy as np
import pandas as pd
import os

collections_root = "/home/jl/data/nftsniper/figures/"
collections = os.listdir(collections_root)

while True:

    collection = np.random.choice(collections)


