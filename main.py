from fastapi import FastAPI, Query, Path
import logging
from typing import Optional
from src.database import Dao
import numpy as np

logger = logging.getLogger()
# dao = Dao()
app = FastAPI()

COLLECTION = "collection"
TOKENID = "tokenid"
CURRENCY = "currency"


@app.get("/")
def root():
    return {"Hello": "world"}


@app.get("/test/{collection}/{tokenid}/")
def test(
        collection: str = Path(..., description='Collection contract address or opensea-slug'),
        tokenid: int = Path(..., description='tokenId from the collection contract'),
):
    return {
        "Test": True,
        COLLECTION: collection,
        TOKENID: tokenid,
    }


@app.get("/api/token/rarity-rank/")
def get_token_rarity_rank(collection: str, tokenid: int):
    try:
        # rarity = dao.get_token_rarity_rank(collection, tokenid)
        return {
            COLLECTION: collection,
            TOKENID: tokenid,
            'rarity-rank': np.random.rand()
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection} {tokenid}")
        return None


@app.get("/api/token/fair-price/")
def get_token_estimated_fair_eth_price(collection: str, tokenid: int, currency: Optional[str] = 'eth'):
    try:
        # fair_price = dao.get_token_fair_eth_price_estimation(collection, tokenid)
        return {
            COLLECTION: collection,
            TOKENID: tokenid,
            CURRENCY: currency,
            'fair-price': 10 * np.random.rand(),
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection} {tokenid}")
        return None


@app.get("/api/token/bargain-factor/")
def get_token_bargain_factor(collection: str, tokenid: int, listing_price: Optional[float] = None):
    # todo: I need to get the listing price from the POST request
    try:
        # fairprice = dao.get_token_fair_eth_price_estimation(collection, tokenid, listing_price)
        # bargain_factor = fairprice / listing_price
        return {
            COLLECTION: collection,
            TOKENID: tokenid,
            "bargain-factor": .1234
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection} {tokenid}")
        return None


@app.get("/api/collection/is-available/")
def is_collection_available(collection: str):
    try:
        # return dao.is_collection_available(collection)
        return {
            COLLECTION: collection,
            "available": True,
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection}")
        return False

# todo: make some endpoints to alow for multiple tokens request at the same time. Use Query()
