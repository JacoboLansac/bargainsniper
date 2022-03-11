from src.database import Dao

class OpenseaCollection:
    def __init__(self, collection_id:str):
        self.dao = Dao()
        self.id = collection_id
        self.slug = self.dao.get_collectoin_slug(collection_id)
        self.total_supply = 9999

    def token_ids(self) -> list:
        return list(range(1, self.total_supply))

