import os
import json
from src.downloaders import MetadataDownloader
from src.rarity import RarityCalculator
import config
from src.web3utils.utils import get_abi

if __name__ == '__main__':

    for collection_slug, collection_address in config.collections['Opensea'].items():
        contract_address = collection_address
        contract_abi = get_abi(collection_slug)  # this should be done based on the contract, not slug

        # Download metadata from
        downloader = MetadataDownloader(contract_address, contract_abi)
        downloader.download_collection_metadata_from_contract()

        rarity_calculator = RarityCalculator(contract_address)
        rarity_calculator.run()
