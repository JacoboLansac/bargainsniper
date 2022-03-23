"""
## Rarity calculations
- downloading tokens attributes (requests / openseaAPI)
- calculate rarity based on attributes appearance
- store rarity and rank in my databases
- estimate fair valuations using log(price/listings) & log(rarity)
- for new listings, calculate bargain-ratio and valuation-ratio
"""
from src.database import Dao
from src.downloader import Downloader
from src.database import OpenseaCollection


class RarityCalculator:
    def __init__(self):
        self.dao = Dao()
        self.downloader = Downloader()


    def initialize_collection(self, colleciton_id:str) -> bool:
        # todo: perhaps this shold throw an asyncronous thread in the background

        # This may take a while
        self.downloader.download_collection_metadata_from_contract(colleciton_id)

        # When the download is done, we can calculate rarities

    def calculate_rarities(self, collection_id:str):
        collection = OpenseaCollection(collection_id)

        attributes = []
        for tokenid in collection.token_ids():
            token_metadata = self.dao.read_token_metadata(collection_id, tokenid)

            #todo: extract attributes

        #todo: compute rarity
        #todo: save rarities update document in database

        self.dao.update_token_metadata(token_metadata)





