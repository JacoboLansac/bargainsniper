from flask import Flask
from src.database import Dao
import logging

logger = logging.getLogger()
app = Flask(__name__)
dao = Dao()



@app.route("/api/token/rarity-rank/<collection_id>/<tokenid>", methods=['GET'])
def get_token_rarity_rank(collection_id: str, tokenid: int):
    try:
        return dao.get_token_rarity_rank(collection_id, tokenid)
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection_id} {tokenid}")
        return None


@app.route("/api/token/fair-eth-price/<collection_id>/<tokenid>", methods=['GET'])
def get_token_estimated_fair_eth_price(collection_id: str, tokenid: int):
    try:
        return dao.get_token_fair_eth_price_estimation(collection_id, tokenid)
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection_id} {tokenid}")
        return None


@app.route("/api/token/bargain-factor/<collection_id>/<tokenid>", methods=['POST'])
def get_token_bargain_factor(collection_id: str, tokenid: int, listing_price):
    # todo: I need to get the listing price from the POST request
    try:
        return dao.get_token_fair_eth_price_estimation(collection_id, tokenid, listing_price)
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection_id} {tokenid}")
        return None


@app.route("/api/collection/is-available/<collection_id>", methods=['GET'])
def is_collection_available(collection_id: str):
    try:
        return dao.is_collection_available(collection_id)
    except:
        logger.exception(f"Could not retrieve rarity rank: {collection_id}")
        return False


@app.route("/api/collection/request/<collection_id>/", methods=['POST'])
def request_collection_initialization(collection_id: str):
    #todo: trigger download collection metadata
    #todo: trigger download of all collection listings from opensea
    #todo: trigger collection tracking
    pass
