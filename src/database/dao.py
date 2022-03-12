from .database import Database


class Dao:
    SLUG = 'slug'
    ADDRESS = 'address'

    def __init__(self):
        self.db = Database()

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
        return self.db.exists_collection(collection_id)

    def _detect_if_slug_or_address(self, collection: str) -> str:
        if collection.startswith('0x'):
            return self.ADDRESS
        else:
            return self.SLUG

    def get_token_metadata(self, collection: str, tokenid: int):
        pass

    def save_token_metadata(self, metadata: dict, collection: str, tokenid: int):
        pass

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
