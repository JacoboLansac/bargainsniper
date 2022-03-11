from src.database.dao import Dao


class Downloader:
    def __init__(self):
        self.dao = Dao()

    def download_token_metadata_from_contract(self, collection_id: str, tokenId: int) -> dict:
        pass

    def get_collection_total_supply_from_contract(self, collection_id: str) -> int:
        pass

    def download_collection_metadata_from_contract(self, collection_id: str):
        total_supply = self.get_collection_total_supply_from_contract(collection_id)
        contract_address = self.dao.get_collection_address(collection_id)

        for tokenid in range(1, total_supply):
            token_metadata = self.download_token_metadata_from_contract(contract_address, tokenid)
            collection_address = self.dao.get_collection_address(collection_id)
            self.dao.save_token_metadata(token_metadata, collection_address, tokenid)

