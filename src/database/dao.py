from .filesdb import FilesDB


class Dao:
    SLUG = 'slug'
    ADDRESS = 'address'

    def __init__(self):
        self.db = FilesDB()

    def get_collectoin_slug(self, collection_id: str) -> str:
        if self._detect_if_slug_or_address(collection_id) == self.SLUG:
            return collection_id
        else:
            return self.address_to_slug(collection_id)

    def get_collectoin_address(self, collection_id: str) -> str:
        if self._detect_if_slug_or_address(collection_id) == self.ADDRESS:
            return collection_id
        else:
            return self.slug_to_address(collection_id)

    def _detect_if_slug_or_address(self, collection_id: str) -> str:
        if collection_id.startswith('0x'):
            return self.ADDRESS
        else:
            return self.SLUG

    def get_token_metadata(self, collection_id: str, tokenid: int):
        pass

    def save_token_metadata(self, metadata:dict, collection_id: str, tokenid: int):
        pass

    def update_token_metadata(self, new_metadata:dict, collection_id:str, tokenid:int):
        pass

    def get_collection_address(self, collection_id: str) -> str:
        pass

    def slug_to_address(self, slug: str) -> str:
        pass

    def address_to_slug(self, collection_address: str) -> str:
        pass
