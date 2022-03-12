from fastapi import FastAPI
from src.database import Dao
import logging
import numpy as np
from typing import Optional

logger = logging.getLogger()
dao = Dao()
app = FastAPI()



@app.get("/")
def root():
    return {"Hello": "world"}


@app.get("/api/token/rarity-rank/<collection>/<tokenid>")
def get_token_rarity_rank(collection:str, tokenid:int):
    try:
        rarity = dao.get_token_rarity_rank(collection, tokenid)
        return {"Rarity": rarity}
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection} {tokenid}")
        return None


@app.get("/api/token/fair-eth-price/<collection>/<tokenid>")
def get_token_estimated_fair_eth_price(collection: str, tokenid: int):
    try:
        fair_price = dao.get_token_fair_eth_price_estimation(collection, tokenid)
        return {"fair-eth-price": fair_price}
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection} {tokenid}")
        return None


@app.get("/api/token/bargain-factor/<collection>/<tokenid>")
def get_token_bargain_factor(collection: str, tokenid: int, listing_price:Optional[float]=None):
    # todo: I need to get the listing price from the POST request
    try:
        fairprice = dao.get_token_fair_eth_price_estimation(collection, tokenid, listing_price)
        bargain_factor = fairprice / listing_price
        return {"bargain-factor": bargain_factor}
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection} {tokenid}")
        return None


@app.get("/api/collection/is-available/<collection>")
def is_collection_available(collection: str):
    try:
        return dao.is_collection_available(collection)
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection}")
        return False


@app.route("/api/collection/request/<collection_id>/", methods=['POST'])
def request_collection_initialization(collection_id: str):
    #todo: this is not necesary at the moment, as I can do this step manually myself
    # todo: trigger download collection metadata
    # todo: trigger download of all collection listings from opensea
    # todo: trigger collection tracking
    pass
