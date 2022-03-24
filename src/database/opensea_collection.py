from src.database import Dao

class OpenseaCollection:
    def __init__(self, contract_address:str):
        self.dao = Dao()
        self.id = contract_address
        self.slug = self.dao.get_collectoin_slug(contract_address)
        self.total_supply = 9999

    def token_ids(self) -> list:
        return list(range(1, self.total_supply))

