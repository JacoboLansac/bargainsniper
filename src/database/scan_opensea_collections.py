import os
import time
from os import path
import json
import requests
import nftconfigs as cfg
import jacotools


class OpenseaCollectionScanner:
    def __init__(self):
        self.limit_one_day_vol_eth = 10
        self.limit_one_day_sales = 40
        self.limit_total_supply = 1000
        self.limit_num_owners_pu = 0.25
        self.base_url = "https://api.opensea.io"

    def process_collections(self, perpage=100):
        offset = 0
        while True:
            url = f"{self.base_url}/api/v1/collections?offset={offset}&limit={perpage}"
            response = requests.request("GET", url)
            if response.status_code != 200:
                print(f"ERROR: {response.reason}")
                return

            data = response.json()
            collections = data['collections']
            for collection in collections:
                valid = self._process_collection(collection)
                if valid:
                    self._retrieve_assets(collection)

            offset += perpage

    def _collectionpath(self, slug):
        # Store data if we made it this far
        return path.join(cfg.datapath, 'collections', slug)

    def _process_collection(self, collection_data:dict):
        slug = collection_data['slug']
        # Filtering based on market stats
        stats = collection_data['stats']

        if (stats['one_day_volume'] < self.limit_one_day_vol_eth):
            print(f"skipping - low volume: [{slug}] : {stats['one_day_volume']}")
            return False

        if (stats['one_day_sales'] < self.limit_one_day_sales):
            print(f"skipping - low sales: [{slug}] : {stats['one_day_sales']}")
            return False

        if (stats['total_supply'] < self.limit_total_supply):
            print(f"skipping - low supply: [{slug}] : {stats['total_supply']}")
            return False

        if (stats['num_owners'] < self.limit_num_owners_pu * stats['total_supply']):
            print(f"skipping - low num_owners: [{slug}] : {stats['num_owners']}")
            return False

        collectionpath = self._collectionpath(slug)
        metadatapath = path.join(collectionpath, 'metadata', f"metadata_{slug}.json")
        os.makedirs(path.dirname(metadatapath), exist_ok=True)
        with open(metadatapath, 'w') as file:
            json.dump(collection_data, file, indent=2)
        print(f"SAVED: {metadatapath}")
        return True

    def _retrieve_assets(self, collection:dict, per_page=50):
        t = time.time()
        slug = collection['slug']
        print(f"Retrieving {collection['stats']['total_supply']} assets from {slug}")
        
        offset = 0
        while True:
            url = f"{self.base_url}/api/v1/assets?order_direction=desc&offset={offset}&limit={per_page}&collection={slug}"
            response = requests.request("GET", url)
            if response.status_code != 200:
                print(f"Finished with {slug} assets in {jacotools.display_time_in_nice_format(time.time()-t)}")
                return

            data = response.json()
            for asset in data['assets']:
                # Removing information to aleviate space
                asset['asset_contract'].pop('description')
                asset.pop('collection')
                asset.pop('sell_orders')

                asset_fpath = path.join(self._collectionpath(slug), 'assets', f"{slug}_{asset['token_id']}.json")
                os.makedirs(path.dirname(asset_fpath), exist_ok=True)
                with open(asset_fpath, 'w') as file:
                    json.dump(asset, file, indent=2)

            offset += per_page


if __name__ == '__main__':
    op = OpenseaCollectionScanner()
    op.process_collections()