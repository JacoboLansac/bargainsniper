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

    def _download_abi_from_etherscan(self, contract_address: str):
        query = f'https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.etherscan_API_KEY}'
        response = requests.get(query)

        if response.status_code != 200:
            self.logger.exception(f"Could not get abi from {contract_address}")
            return {}

        return response.json()

    def _save_abi(self, abi: dict, contract_address: str):
        json.dump(abi, open(self.get_abi_path(contract_address), 'w'))

    def read_abi(self, contract_address: str):
        _abi_path = self.get_abi_path(contract_address)
        if not path.isfile(_abi_path):
            abi = self._download_abi_from_etherscan(contract_address)
            self._save_abi(abi, contract_address)
        else:
            abi = json.load(open(_abi_path, 'w'))

        return abi

    def get_abi_path(self, contract_address: str):
        return path.join(config.project_path, 'resources', 'abis', contract_address)


if __name__ == '__main__':
    contract = '0xc5b52253f5225835cc81c52cdb3d6a22bc3b0c93'
    abi_manager = AbiManager()
    print(abi_manager.read_abi(contract))
