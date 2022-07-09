import time
import config
from logging import getLogger
from typing import Optional
from src.database.dao_metadata import DaoMetadata
from src.web3utils import infura_https
from web3 import Web3
import re
import web3.exceptions
import requests
from src.downloaders.abi_manager import AbiManager

# import grequests


class MetadataDownloader:
    def __init__(self, contract_address: str):
        self.dao = DaoMetadata()
        self.web3 = Web3(Web3.HTTPProvider(infura_https()))
        self.logger = getLogger(self.__class__.__name__)

        abi_manager = AbiManager()

        self.contract_address = contract_address
        self.contract_abi = abi_manager.read_abi(contract_address)

        self.contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(self.contract_address),
            abi=self.contract_abi)

    def _connection_check(self):
        if not self.web3.isConnected():
            raise ConnectionError("Not connected to web3")

    def infer_base_uri(self) -> Optional[str]:
        try:
            return self.contract.functions.baseURI().call()
        except web3.exceptions.ABIFunctionNotFound:
            try:
                tokenId = 123
                tokenURI1 = self.contract.functions.tokenURI(tokenId).call()
                if tokenURI1.endswith(str(tokenId)):
                    return re.sub(str(tokenId) + '$', '', tokenURI1)
                else:
                    return None
            except web3.exceptions.ABIFunctionNotFound:
                return None

    def download_batch_metadata_from_contract(self, offset: int, batchsize: int) -> list:
        self._connection_check()
        base_uri = self.infer_base_uri()
        if base_uri is None:
            self.logger.exception(f"base_uri could not be inferred")
            return []

        # todo: paralelize this with grequests or similar
        urls = [(_tokenid, f"{base_uri}{_tokenid}") for _tokenid in range(offset, offset + batchsize)]

        batch_metadata = []
        for tokenid, url in urls:
            response = requests.get(url)
            if response.status_code == 200:
                batch_metadata.append((tokenid, response.json()))
            else:
                self.logger.error(f"Could not retrieve metadata for tokenid={tokenid}: {response.reason}")
        return batch_metadata

    def get_collection_total_supply_from_contract(self) -> (int, None):
        self._connection_check()
        # todo: perhaps redo this using brownie
        try:
            return self.contract.functions.totalSupply().call()
        except web3.exceptions.ABIFunctionNotFound:
            self.logger.exception(f"Could not retrive totalSupply")
            return None

    def download_collection_metadata_from_contract(self, batchsize=20, force_full_download=False):
        self._connection_check()
        total_supply = self.get_collection_total_supply_from_contract()
        total_supply = total_supply or 10000

        if force_full_download:
            start_token_id = 1
        else:
            already_downloaded_tokenids = self.dao.list_available_tokenids(self.contract_address)

            if already_downloaded_tokenids:
                start_token_id = int(max(already_downloaded_tokenids))
            else:
                start_token_id = 1

        n_attemps = 3
        btime = time.time()
        for offset in range(start_token_id, total_supply, batchsize):

            batchsize = min(batchsize, total_supply - start_token_id)
            attempt = 0
            success = False

            while not success:
                try:
                    self.logger.info(f"downloading tokenids: [{offset} -> {offset + batchsize}] [{self.contract_address}]")

                    batch_metadata = self.download_batch_metadata_from_contract(offset=offset, batchsize=batchsize)

                    if not batch_metadata:
                        self.logger.info(f"Not a single tokenId returned metadata. Jumping to next")
                        break

                    for tokenid, token_metadata in batch_metadata:
                        self.dao.save_token_metadata(token_metadata, self.contract_address, tokenid)

                    # Download time estimations
                    average_token_download_time = round((time.time() - btime) / (offset + batchsize), 3)
                    self.logger.info(f"Average download time: {average_token_download_time} secs / token. "
                          f"Estimated time: {round(total_supply * average_token_download_time / 3600, 2)} hours")

                    success = True

                except:
                    if attempt < n_attemps:
                        attempt += 1
                        time.sleep(30)
                    else:
                        raise Exception(f"Could not download offset={offset} after {n_attemps} attempts")

        # Download the missing ones
        already_downloaded_tokenids = self.dao.list_available_tokenids(self.contract_address)
        missing = [tokenid for tokenid in range(total_supply) if tokenid not in already_downloaded_tokenids]

        # TODO: do a smart round of downloading missing ones

