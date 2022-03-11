from flask import Flask

app = Flask(__name__)


@app.route("/api/token/rarity-rank/<collection_id>/<tokenid>", methods=['GET'])
def get_token_rarity_rank(collection_id: str, tokenid: int):
    pass


@app.route("/api/token/fair-eth-price/<collection_id>/<tokenid>", methods=['GET'])
def get_token_estimated_fair_eth_price(collection_id: str, tokenid: int):
    pass


@app.route("/api/token/bargain-factor/<collection_id>/<tokenid>", methods=['GET'])
def get_token_bargain_factor(collection_id: str, tokenid: int):
    pass


@app.route("/api/collection/is-available/<collection_id>", methods=['GET'])
def is_collection_available(collection_id: str):
    pass


@app.route("/api/collection/request/<collection_id>/", methods=['POST'])
def request_collection_initialization(collection_id: str):
    pass
