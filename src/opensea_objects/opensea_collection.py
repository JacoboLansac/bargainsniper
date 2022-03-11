import requests
from os import path
import platform

ASSETS = 'assets'


class OpenseaCollection:
    def __init__(self, slug: str = None, data: dict = None):
        if (slug is None) and (data is None):
            raise ValueError("At least one of the inputs must be different than None")

        # Initalize collection data
        if slug is None:
            if data is None:
                raise ValueError("If slug is None, data must be probided for initialization")
            else:
                self.data = data
                self.slug = self.data['slug']
        else:
            self.slug = slug
            self.data = self._get_collection_data()

        self.stats = self.data['stats']
        self.name = self.data['name']
        self.floor_price = float(self.stats['floor_price'])
        self.total_supply = int(self.stats['total_supply'])
        self.datapath = path.join(self.get_datapath(), 'collections', self.slug)
        self.collection_url = f'https://opensea.io/collection/{self.slug}'
        print(f"Init: {self.__class__.__name__}: {self.slug}")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.slug}"

    def get_datapath(self):
        if 'ThinkBook' in platform.node():
            homepath = path.expanduser('~')
            datapath = path.join(homepath, 'data', 'nftsniper')
        else:
            datapath = path.join('data', 'nftsniper')
        return datapath

    def _get_collection_data(self):
        print(f"Loading collection info")
        sample_assets = self.query_collection_items(offset=0, per_page=1)
        if not sample_assets:
            raise KeyError(f"No assets found for {self.slug}. Check spelling")
        else:
            sample_asset = sample_assets[0]
            address = sample_asset['asset_contract']['address']
            token_id = sample_asset['token_id']
            single_asset = self.get_single_asset(address, token_id)
            return single_asset['collection']

    def get_single_asset(self, contract_address: str, token_id: int):
        url = f"https://api.opensea.io/api/v1/asset/{contract_address}/{token_id}/"
        response = requests.request("GET", url)
        return response.json()

    def query_collection_items(self, offset: int, per_page: int) -> list:
        print(f"fetching {self.slug}: {per_page} items: from {offset} to {offset + per_page}")
        url = "https://api.opensea.io/api/v1/assets"
        querystring = {
            # "order_by": "sale_price", "order_direction": "desc",
            "offset": str(offset),
            "limit": str(per_page),
            "collection": self.slug
        }
        response = requests.request("GET", url, params=querystring)
        if response.status_code != 200:
            print(f"Error or finished")
            return []
        data = response.json()[ASSETS]
        return data


if __name__ == '__main__':
    opc = OpenseaCollection('niftydegen')
