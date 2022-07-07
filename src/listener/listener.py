import pandas as pd
from typing import Optional
from src.database.dao_opensea import OpenseaDao
from src.database.dao_rarity import DaoRarity
from src.database.dao_listing import DaoListing
from logging import getLogger
import numpy as np
from typing import List
from src.database.listing import Listing
from src.database.rarity import Rarity


class OpenseaListener:
    def __init__(self):
        self.NFTmarketplace = OpenseaDao()
        self.daorarity = DaoRarity()
        self.daolistings = DaoListing()
        self.logger = getLogger(self.__class__.__name__)


    def update_collection_prices(self):
        pass

    def fair_price_estimations(self, listings: List[Listing], rarities: List[Rarity]) -> pd.DataFrame:
        pass

    def snipe_bargains(self, rarity_price_data:pd.DataFrame, profit_margin:0.5) -> list:
        pass

    def notify(self, bargain_tokenids: list):
        pass

    def run(self, contract_address:str, last_timestamp:Optional[int]):

        # Get listings from opensea (since when? I need to store last time we retrieved listings)
        listings = self.NFTmarketplace.get_listings(collection_slug=contract_address)
        listings = [Listing({}), Listing({}), Listing({}), ]

        if not listings:
            self.logger.info(f"No new listings. Skipping re-calculations")
            return

        # Update listings in database
        for listing in listings:
            self.daolistings.save_token_listing(listing.info(), contract_address, listing.tokenid)

        # Fake listed tokenids
        tokenids = list(np.random.randint(1, 10000, 2000))

        # Load from db the rarities of all listed tokens (not only the ones listened just now)
        rarities = self.daorarity.read_collection_rarities(contract_address, tokenids)

        rarity_price_data = self.fair_price_estimations(listings, rarities)

        bargains_tokenids = self.snipe_bargains(rarity_price_data, profit_margin=0.5)

        self.notify(bargains_tokenids)
