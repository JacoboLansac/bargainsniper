from dotenv import load_dotenv
import os

load_dotenv()


def infura_https():
    infura_project_id = os.getenv("WEB3_INFURA_PROJECT_ID")
    if infura_project_id is None:
        raise ValueError("WEB3_INFURA_PROJECT_ID is None")
    return f"https://mainnet.infura.io/v3/{infura_project_id}"

