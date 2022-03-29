import time
from typing import List, Optional
from logging import getLogger
from .database import Database
from .rarity import Rarity


class DaoRarity:
    TOKENID = 'tokenid'
    RARITY = 'rarity'

    def __init__(self):
        self.db = Database()
        self.logger = getLogger(self.__class__.__name__)

    def collection_directory_id(self, contract_address: str) -> str:
        return f"{self.RARITY}/{contract_address}"

    def is_collection_available(self, contract_address: str) -> bool:
        return self.db.exists_directory(self.collection_directory_id(contract_address))

    def read_token_rarity(self, contract_address: str, tokenid: int) -> Optional[Rarity]:
        rarity_info = self.db.read_document(
            directory_id=self.collection_directory_id(contract_address),
            document_key=tokenid
        )
        if rarity_info is not None:
            return Rarity(rarity_info)
        else:
            return None

    def save_token_rarity(self, rarity_info: dict, contract_address: str, tokenid: int):
        """For rarity information computed inhouse"""
        rarity_info[self.TOKENID] = tokenid
        success = self.db.save_document(
            document=rarity_info,
            directory_id=self.collection_directory_id(contract_address),
            document_key=str(tokenid)
        )
        if success:
            self.logger.debug(f"Saved rarity: {contract_address}/{tokenid} ")

    def read_collection_rarities(self, contract_address: str, tokenids: List[int]):
        """
        I tested the loading times using the RarityOject and pure jsons and there is no difference
        Loading 2000 items takes about 0.072 seconds, so it is decently low (loading from disk)
        :param contract_address:
        :param tokenids:
        :return:
        """
        t = time.time()
        rarities = []
        for tokenid in tokenids:
            rarities.append(self.read_token_rarity(contract_address, tokenid))
        self.logger.info(f"Loaded {len(rarities)} rarities in {round(time.time() - t, 3)} seconds")
        return rarities
