from dotenv import load_dotenv
from os import path
import os
import json
from bconfig import project_path

load_dotenv()


def infura_https():
    infura_project_id = os.getenv("WEB3_INFURA_PROJECT_ID")
    if infura_project_id is None:
        raise ValueError("WEB3_INFURA_PROJECT_ID is None")
    return f"https://mainnet.infura.io/v3/{infura_project_id}"


def get_abi(collection_slug: str):
    return json.load(open(path.join(project_path, f"resources/abis/{collection_slug}_abi.json"), "r"))
