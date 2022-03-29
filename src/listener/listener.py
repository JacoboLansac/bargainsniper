from src.database.dao_opensea import DaoOpensea
from src.database.dao_rarity import DaoRarity
from logging import getLogger
import numpy as np


class OpenseaListener:
    def __init__(self):
        self.marketplace = DaoOpensea()
        self.daorarity = DaoRarity()
        self.logger = getLogger(self.__class__.__name__)


    def update_collection_prices(self):
        pass

    def fair_price_estimations(self):
        pass

    def snipe_bargains(self):
        pass

    def notify(self):
        pass

    def run(self, contract_address:str):

        # Get listings from opensea (since when? I need to store last time we retrieved listings)
        # listings = self.marketplace.get_listings(collection_slug=contract_address)
        listings = [{}, {}]

        if not listings:
            self.logger.info(f"No new listings. Skipping re-calculations")
            return

        # Fake listed tokenids
        tokenids = list(np.random.randint(1, 10000, 2000))

        # Load from db the rarities of all listed tokens (not only the ones listened just now)
        rarirties = self.daorarity.read_collection_rarities(contract_address, tokenids)

        # todo: updates prices from database (remove sold items, add new listed items)
        # todo: weighted regression to establish the fair price
        # todo: find bargains
        # todo: notify
