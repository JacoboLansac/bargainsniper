import os
from os import path
import json
from src.downloaders import MetadataDownloader
from src.rarity import RarityCalculator
import config
from src.web3utils.utils import get_abi
from logging import getLogger

logger = getLogger(path.basename(__file__))

if __name__ == '__main__':

    logger.critical(f"Starting downloads")
    logger.info(f"Configured collections to download:")
    [logger.info(f"\t{address}\t[{name}]") for name, address in config.collections['Opensea'].items()]

    for name, collection_address in config.collections['Opensea'].items():
        logger.info(f"Starting download: [{name}][{collection_address}]")
        contract_address = collection_address

        # Download metadata from
        downloader = MetadataDownloader(contract_address)
        downloader.download_collection_metadata_from_contract()

        rarity_calculator = RarityCalculator(contract_address)
        rarity_calculator.run()
