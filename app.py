from fastapi import FastAPI, Query, Path, Depends, Body, HTTPException, status
from pydantic import Field
import logging
from enum import Enum
from typing import Optional
from src.database import Dao
import numpy as np

logger = logging.getLogger()
# dao = Dao()
app = FastAPI()

COLLECTION = "collection"
TOKENID = "tokenid"
CURRENCY = "currency"

class Currencies(Enum):
    ETH = 'eth'


class Tags(Enum):
    TOKEN = 'Token'
    COLLECTION = 'Collection'


class TokenInputs:
    def __init__(
            self,
            collection: str = Path(..., description='Collection identifier: contract address or opensea-slug'),
            tokenid: int = Path(..., description='Token unique identifier within the collection'),
    ):
        self.collection = collection
        self.tokenid = tokenid

#
# class OtherInputs:
#     def __init__(self,
#                  ethprice: int = Body(..., description='price in eth', example='eth')
#                  ):
#         self.ethprice = ethprice


@app.get("/")
def root():
    return {"Hello": "world"}


@app.get("/api/token/rarity-rank/{collection}/{tokenid}", tags=[Tags.TOKEN])
def get_token_rarity_rank(token_inputs: TokenInputs = Depends()):
    """
    Returns the estimated rarity rank of the token within based on the probability of occurente of its traits
    """
    try:
        # rarity = dao.get_token_rarity_rank(collection, tokenid)
        return {
            COLLECTION: token_inputs.collection,
            TOKENID: token_inputs.tokenid,
            'rarity-rank': np.random.randint(1, 9999)
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {token_inputs.collection} {token_inputs.tokenid}")
        return None


@app.get("/api/token/fair-price/{collection}/{tokenid}", tags=[Tags.TOKEN])
def get_token_estimated_fair_price(
        token_inputs: TokenInputs = Depends(),
        currency: str = Query('eth', description='Currency in which fair-price is returned', example='eth')
):
    """
    Returns the token fair price in eth, estimated from the relative prices and rarity ranks of all collection assets
    """
    if currency != Currencies.ETH.value:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail='Only eth is supported as currency')

    try:
        # fair_price = dao.get_token_fair_eth_price_estimation(collection, tokenid)
        return {
            COLLECTION: token_inputs.collection,
            TOKENID: token_inputs.tokenid,
            CURRENCY: currency,
            'fair-price': 10 * np.random.rand(),
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {token_inputs.collection} {token_inputs.tokenid}")
        return None


@app.get("/api/token/bargain-factor/{collection}/{tokenid}", tags=[Tags.TOKEN])
def get_token_bargain_factor(
        token_inputs: TokenInputs = Depends(),
        listing_price_in_eth: float = Query(..., description='The price in eth at which the asset has been listed')):
    """
    Returns the bargain factor, calculated as the fair price relative to the listed price. The higher the bargain factor,
    the more underpriced the asset. If bargain_factor=1, the asset is correctly priced.
    """
    # todo: I need to get the listing price from the POST request
    try:
        # fairprice = dao.get_token_fair_eth_price_estimation(collection, tokenid, listing_price)
        # bargain_factor = fairprice / listing_price
        return {
            COLLECTION: token_inputs.collection,
            TOKENID: token_inputs.tokenid,
            'listing-price': listing_price_in_eth,
            "bargain-factor": .1234
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {token_inputs.collection} {token_inputs.tokenid}")
        return None


@app.get("/api/collection/is-available/{collection}", tags=[Tags.COLLECTION])
def is_collection_available(
        collection: str = Path(..., description='Collection identifier: contract address or opensea-slug')):
    """
    Only selected collections are tracked. This endpoint returns True if a colleciton is currently being tracked, and
    therefore the rarity information of its tokens can be extracted
    """
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
