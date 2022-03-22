import numpy as np
import pandas as pd
import os
import json
import argparse
from src.downloader import Downloader

if __name__ == '__main__':

    # contact_address = "0xed5af388653567af2f388e6224dc7c4b3241c544"  # azuki
    contact_address = "0x86C35FA9665002C08801805280fF6a077B23c98A"  # catblox
    contract_abi = json.load(open("/home/jl/projects/bargainsniper/resources/abis/catblox_abi.json", "r"))

    downloader = Downloader(contact_address, contract_abi)
    downloader.download_collection_metadata_from_contract()