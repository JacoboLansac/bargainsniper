import traceback

import jacotools
from src.opensea_objects.opensea_collection import OpenseaCollection
from src.models.rarity_sniper import RaritySniper
from jacotools import notificators
# from src.scrappers import ImmutableScrapper
# from src.immutable_collection import ImmutableCollection


class FloorDetector:
    def __init__(self):
        self.base_url = "https://api.opensea.io"
        # self.limit_one_day_vol_eth = 1
        # self.limit_one_day_sales = 1
        # self.limit_total_supply = 1000
        # self.limit_num_owners_pu = 0.2
        self.cooldown_freq = '1s' if jacotools.is_debugging() else '1d'
        self.discorder = notificators.Discorder('floordetector', cooldown_freq=self.cooldown_freq)
        self.telegramer = notificators.Telegramer('foolrdetector', cooldown_freq=self.cooldown_freq)
        self.emailer = notificators.Emailer('foolrdetector', cooldown_freq=self.cooldown_freq)
        self.imalive = notificators.ImAlive(self.__class__.__name__)
        # self.immutable_scrapper = ImmutableScrapper()

        # Prices are in ETH
        self.opensea_price_targets = {
            "monsterbuds": 0.06,
            "doge-pound-puppies-real": 0.4,
            "evolvingforest": 0.04,
            "bofadeeznuts": 0.1,
            "kaiju-kingz": 2.5,
            "cool-cats-nft": 4,
            "mutant-ape-yacht-club": 3,
            "headdao": 0.1,
            "the-doge-pound": 1.5,
            "neo-tokyo-identities": 4,
            "chill-frogs": 0.1,
        }

        self.immutable_price_targets = {
            "Astro Bros": {
                'address': '0x9c77027170eda1808262809771067bee23830050',
                'price_target': 0.06,
            },
            "Moody Krows": {
                'address': '0x5f32923175e13713242b3ddd632bdee82ab5f509',
                'price_target': 0.3,
            },
            "LandLoot": {
                'address': '0xd278f51207d30cd9616ad0841a7486eca16e1f4a',
                'price_target': 0.08,
            }
        }

    def check_floor_prices(self):
        """
        Goes through the config collections, reads the floor price and compares it to the
        :return:
        """
        # for slug, col_data in self.immutable_price_targets.items():
        #     icollection = ImmutableCollection(slug, col_data['address'])
        #     print(f"\n{icollection.slug} floor price: {icollection.floor_price} ETH")
        #     if icollection.floor_price < col_data['price_target']:
        #         self.notify_floor_drop(icollection, col_data['price_target'])

        for slug, eth_price_target in self.opensea_price_targets.items():
            try:
                collection = OpenseaCollection(slug=slug)
                print(f"\n{collection.slug} floor price: {collection.floor_price} ETH")
                if collection.floor_price < eth_price_target:

                    self.notify_floor_drop(collection, eth_price_target)
                    self.run_rarity_sniper(collection)
            except Exception as e:
                self.telegramer.notify('exception', traceback.format_exc(), bypass_cooldown=True)

        self.imalive.notify()

    def notify_floor_drop(self, collection, eth_price_target:float):
        mssg = f"**{collection.name}** is below price target." \
               f"\nPrice target: {eth_price_target} ETH" \
               f"\nFloor price: {collection.floor_price} ETH" \
               f"\n{collection.collection_url}"

        self.discorder.notify(collection.slug, mssg)
        self.telegramer.notify(collection.slug, mssg)
        self.emailer.notify(collection.slug, mssg, subject=f'Floor Price: {collection.slug}')

    def run_rarity_sniper(self, collection:OpenseaCollection):
        rsniper = RaritySniper(collection.slug, max_eth_price=3*collection.floor_price)
        rsniper.run()

    # def _valid_stats(self, collection:OpenseaCollection) -> bool:
    #
    #     stats = collection.stats
    #     if (stats['one_day_volume'] < self.limit_one_day_vol_eth):
    #         # print(f"skipping - low volume: [{collection.slug}] : {stats['one_day_volume']}")
    #         return False
    #
    #     elif (stats['one_day_sales'] < self.limit_one_day_sales):
    #         print(f"skipping - low sales: [{collection.slug}] : {stats['one_day_sales']}")
    #         return False
    #
    #     elif (stats['total_supply'] < self.limit_total_supply):
    #         print(f"skipping - low supply: [{collection.slug}] : {stats['total_supply']}")
    #         return False
    #
    #     elif (stats['num_owners'] < self.limit_num_owners_pu * stats['total_supply']):
    #         print(f"skipping - low num_owners: [{collection.slug}] : {stats['num_owners']}")
    #         return False
    #
    #     elif (stats['one_day_volume'] == stats['seven_day_volume']):
    #         print(f"skipping - dayvol == weekvol: [{collection.slug}] : {stats['one_day_volume']}")
    #         return False
    #
    #     else:
    #         return True


if __name__ == '__main__':
    fd = FloorDetector()
    fd.check_floor_prices()

    # col = OpenseaCollection(slug='jungle-freaks-by-trosley')
    # fd.process_collections()
