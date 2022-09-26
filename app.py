from fastapi import FastAPI, Query, Path, Depends, Body, HTTPException, status
from pydantic import Field, BaseModel
import logging
from enum import Enum
from typing import Optional
import numpy as np
from src.database import DaoRarity

# from src.database import Dao

logger = logging.getLogger()
rarity_dao = DaoRarity()
app = FastAPI()

COLLECTION = "collection"
TOKENID = "tokenid"
CURRENCY = "currency"


class Currencies(Enum):
    ETH = 'eth'


class Tags(Enum):
    TOKEN = 'Token'
    COLLECTION = 'Collection'
    LISTINGS = 'Listings'


class InputCollection:
    def __init__(self,
                 contract_address: str = Path(...,
                                              description='Collection identifier: contract address',
                                              example='0x0f78c6eee3c89ff37fd9ef96bd685830993636f2')):
        self.contract_address = contract_address


class InputTokenId:
    def __init__(self,
                 tokenid: int = Path(...,
                                     ge=0,
                                     description='Unique integer identifier of the token within the collection',
                                     example=2421)):
        self.tokenid = tokenid


@app.get("/")
def hello_world():
    return {"Welcome to bargain sniper!": "Please visit the /docs/ endpoint to see the API documentation and endpoints"}


@app.get("/api/rarity/token/rank/{contract_address}/{tokenid}", tags=[Tags.TOKEN])
def get_token_rarity_rank(input_tokenid: InputTokenId = Depends(), input_collection: InputCollection = Depends()):
    """
    Returns the estimated rarity rank of the token within the collection, based on the joint probability of its traits.
    """
    try:
        rarity_info = rarity_dao.read_token_rarity(input_collection.contract_address, input_tokenid.tokenid)
        if rarity_info is not None:
            rarity_rank = rarity_info.rarity_rank
        else:
            rarity_rank = None

        # rarity = dao.get_token_rarity_rank(collection, tokenid)
        return {
            COLLECTION: input_collection.contract_address,
            TOKENID: input_tokenid.tokenid,
            'rarity_rank': rarity_rank
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {input_collection.contract_address} {input_tokenid.tokenid}")
        return None


@app.get("/api/rarity/token/info/{contract_address}/{tokenid}", tags=[Tags.TOKEN])
def get_token_rarity_info(input_tokenid: InputTokenId = Depends(), input_collection: InputCollection = Depends()):
    """
    Returns the estimated rarity rank of the token within the collection, based on the joint probability of its traits.
    """
    try:
        rarity_info = rarity_dao.read_token_rarity(input_collection.contract_address, input_tokenid.tokenid)
        # rarity = dao.get_token_rarity_rank(collection, tokenid)
        return {
            COLLECTION: input_collection.contract_address,
            TOKENID: input_tokenid.tokenid,
            'rarity_info': rarity_info
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {input_collection.contract_address} {input_tokenid.tokenid}")
        return None


@app.get("/api/rarity/collection/exists/{contract_address}", tags=[Tags.COLLECTION])
def is_collection_available(input_collection: InputCollection = Depends()):
    """
    Only selected collections are tracked. This endpoint returns True if a collection is currently being tracked, and
    therefore the rarity information of its tokens can be extracted. If this endpoint returns false, the api will
    not provide info for the requested collection.
    """
    try:
        return {
            COLLECTION: input_collection.contract_address,
            "available": rarity_dao.is_collection_available(input_collection.contract_address),
        }
    except:
        logger.exception(f"Could not retrieve rarity rank: {input_collection.contract_address}")
        return False



@app.get("/api/rarity/collection/list", tags=[Tags.COLLECTION])
def available_collections():
    """
    Only selected collections are tracked. This endpoint returns True if a collection is currently being tracked, and
    therefore the rarity information of its tokens can be extracted. If this endpoint returns false, the api will
    not provide info for the requested collection.
    """
    try:
        collections = rarity_dao.list_available_collections()
        return {
            'rarity_available': collections
        }
    except:
        logger.exception(f"Could not retrieve available collections")
        return []




# @app.get("/api/token/fair-price/{collection}/{tokenid}", tags=[Tags.TOKEN])
# def get_token_estimated_fair_price(
#         input_tokenid: InputTokenId = Depends(),
#         input_collection: InputCollection = Depends(),
#         currency: str = Query('eth', description='Currency in which fair-price is returned', example='eth')
# ):
#     """
#     Returns the token fair price in eth, estimated from the relative prices and rarity ranks of all collection assets.
#     """
#     if currency != Currencies.ETH.value:
#         raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,
#                             detail='Only eth is supported as currency at the moment')
#
#     try:
#         # fair_price = dao.get_token_fair_eth_price_estimation(collection, tokenid)
#         return {
#             COLLECTION: input_collection.collection,
#             TOKENID: input_tokenid.tokenid,
#             CURRENCY: currency,
#             'fair_price_in_eth': round(10 * np.random.rand(), 4),
#         }
#     except:
#         logger.exception(f"Could not retrieve rarity rank: {input_collection.collection} {input_tokenid.tokenid}")
#         return None
#
#
# @app.get("/api/token/bargain-factor/{collection}/{tokenid}", tags=[Tags.TOKEN])
# def get_token_bargain_factor(
#         input_tokenid: InputTokenId = Depends(),
#         input_collection: InputCollection = Depends(),
#         listing_price_in_eth: float = Query(...,
#                                             description='The price in eth at which the asset has been listed',
#                                             example=0.543)):
#     """
#     Returns the bargain factor, calculated as the fair price relative to the listed price. The higher the bargain factor,
#     the more underpriced the asset. If bargain_factor=1, the asset considered listed at fair price, compared with the
#     rest of the rarities and prices.
#     """
#     # todo: I need to get the listing price from the POST request
#     try:
#         # fairprice = dao.get_token_fair_eth_price_estimation(collection, tokenid, listing_price)
#         fairprice = round(10 * np.random.rand(), 4)
#         bargain_factor = round(fairprice / listing_price_in_eth, 4)
#
#         return {
#             COLLECTION: input_collection.collection,
#             TOKENID: input_tokenid.tokenid,
#             "fair_price_in_eth": fairprice,
#             "listing_price_in_eth": listing_price_in_eth,
#             "bargain_factor": bargain_factor,
#         }
#     except:
#         logger.exception(f"Could not retrieve rarity rank: {input_collection.collection} {input_tokenid.tokenid}")
#         return None


# @app.get("/api/collection/price-walls/{collection}", tags=["Other-ideas"])
# def get_listing_price_walls(input_collection: InputCollection = Depends()):
#     """
#     Sometimes, the floor price is not as good indication as the price where most of the sell orders are. This method
#     identifies prices with high density of listings returns them, together with the number of listings in each price.
#     :param input_collection:
#     :return:
#     """
#     try:
#         wall = 5 * np.random.rand()
#         return [
#             {
#                 "price_in_eth": round(wall, 3),
#                 CURRENCY: Currencies.ETH.value,
#                 "number_of_listings": np.random.randint(25, 200),
#             },
#             {
#                 "price_in_eth": round((10 * np.random.rand() + 1) * wall, 3),
#                 CURRENCY: Currencies.ETH.value,
#                 "number_of_listings": np.random.randint(15, 400),
#             }
#         ]
#     except:
#         logger.exception(f"Could not retrieve listings for: {input_collection.collection}")
#         return None
