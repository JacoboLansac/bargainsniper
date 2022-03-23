from .database import Database
from logging import getLogger


class Dao:
    SLUG = 'slug'
    ADDRESS = 'address'
    METADATA = 'metadata'

    def __init__(self):
        self.db = Database()
        self.logger = getLogger(self.__class__.__name__)

    def get_collectoin_slug(self, collection: str) -> str:
        if self._detect_if_slug_or_address(collection) == self.SLUG:
            return collection
        else:
            return self._address_to_slug(collection)

    def get_collectoin_address(self, collection: str) -> str:
        if self._detect_if_slug_or_address(collection) == self.ADDRESS:
            return collection
        else:
            return self._slug_to_address(collection)

    def collection_id(self, address) -> str:
        pass

    def is_collection_available(self, collection) -> bool:
        collection_id = self.collection_id(self.get_collection_address(collection))
        return self.db.exists_directory(collection_id)

    def _detect_if_slug_or_address(self, collection: str) -> str:
        if collection.startswith('0x'):
            return self.ADDRESS
        else:
            return self.SLUG

    def read_token_metadata(self, contract_address: str, tokenid: int):
        return self.db.read_document(
            directory_id=f"{self.METADATA}/{contract_address}",
            document_key=tokenid
        )

    def save_token_metadata(self, metadata: dict, contract_address: str, tokenid: int):
        success = self.db.save_document(
            document=metadata,
            directory_id=f"{self.METADATA}/{contract_address}",
            document_key=str(tokenid)
        )
        if success:
            self.logger.debug(f"Saved: {contract_address}:{tokenid} metadata")

    def update_token_metadata(self, new_metadata: dict, collection: str, tokenid: int):
        pass

    def get_collection_address(self, collection: str) -> str:
        pass

    def get_token_rarity_rank(self, collection: str, tokenid: int):
        pass

    def get_token_fair_eth_price_estimation(self, collection: str, tokenid: int, listing_price:float):
        pass

    def _slug_to_address(self, slug: str) -> str:
        pass

    def _address_to_slug(self, collection_address: str) -> str:
        pass
