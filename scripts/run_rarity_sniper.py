import traceback
import time
import jacotools as jtools
from src.models.rarity_sniper import RaritySniper
from jacotools import notificators

if __name__ == '__main__':

    emailer = notificators.Emailer('raritysniper', cooldown_freq='10s')
    sleep_time_hours = 0.1
    nassets = 500 if jtools.is_debugging() else None

    collections = [
        "sipherianflash",
        "monsterbuds",
        "chill-frogs",
        "wonky-stonks",
        "habbo-avatars",
        "moose-trax-nft",
        "evolvingforest",
        "galaxy-fight-club",
        "foxfam",
        "thegoobers",
        "jungle-freaks-by-trosley",
        "mutant-ape-yacht-club",
        "the-doge-pound",
        "niftydegen",
        "theyakuzacatssociety",
    ]
    while True:
        print(f"Running RaritySniper on: {collections}")
        for collection in collections:
            try:
                rsniper = RaritySniper(collection, max_eth_price=5)
                rsniper.run(max_n_assets=nassets)
            except Exception as e:
                emailer.notify('exception',
                    content=f"[NFT sniper]: Exception on {collection}: {traceback.format_exc()}",
                    subject=f"Exception in nftsniper",
                )

        time.sleep(60 * 60 * sleep_time_hours)

