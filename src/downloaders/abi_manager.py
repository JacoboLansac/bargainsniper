import dotenv
from os import path
import os
import requests
from logging import getLogger
import config
import json

dotenv.load_dotenv()


class AbiManager:
    def __init__(self):
        self.etherscan_API_KEY = os.getenv("ETHERSCAN_TOKEN")
        self.logger = getLogger(self.__class__.__name__)

    def read_abi(self, contract_address: str):
        _abi_path = self.get_abi_path(contract_address)
        self._make_sure_abi_is_downloaded(contract_address)

        abi = json.load(open(_abi_path, 'r'))

        return abi

    def get_abi_path(self, contract_address: str):
        return path.join(config.project_path, 'resources', 'abis', contract_address)

    def _download_abi_from_etherscan(self, contract_address: str) -> (str, None):
        self.logger.info(f"Downloading abi for {contract_address}")

        query = f'https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.etherscan_API_KEY}'
        response = requests.get(query)

        if response.status_code != 200:
            self.logger.exception(f"Could not download abi from etherscan for: {contract_address}")
            return None

        return response.json()['result']

    def _save_abi(self, abi: str, contract_address: str):
        abi_path = self.get_abi_path(contract_address)
        os.makedirs(path.dirname(abi_path), exist_ok=True)
        json.dump(json.loads(abi), open(abi_path, 'w'), indent=2)

    def _make_sure_abi_is_downloaded(self, contract_address: str):
        _abi_path = self.get_abi_path(contract_address)
        if not path.isfile(_abi_path):
            abi = self._download_abi_from_etherscan(contract_address)
            if abi:
                self._save_abi(abi, contract_address)
            else:
                self.logger.exception(f"Abi is empty. Not saving")


if __name__ == '__main__':
    contract = '0xc5b52253f5225835cc81c52cdb3d6a22bc3b0c93'
    abi_manager = AbiManager()
    print(abi_manager.read_abi(contract))
