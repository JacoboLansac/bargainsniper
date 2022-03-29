from .database import Database
from .metadata import Metadata
from .opensea_collection import OpenseaCollection
from .rarity import Rarity
from logging import getLogger
from typing import Optional


class Dao:
    SLUG = 'slug'
    ADDRESS = 'address'
    METADATA = 'metadata'
    TOKENID = 'tokenid'
    RARITY = 'rarity'

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

    def read_token_metadata(self, contract_address: str, tokenid: int) -> Optional[Metadata]:
        metadata = self.db.read_document(
            directory_id=f"{self.METADATA}/{contract_address}",
            document_key=tokenid
        )
        if metadata is not None:
            return Metadata(metadata)
        else:
            return None

    def save_token_metadata(self, metadata: dict, contract_address: str, tokenid: int):
        """For original metadata comming from the contract"""
        metadata = self._clean_metadata(metadata)
        metadata[self.TOKENID] = tokenid

        success = self.db.save_document(
            document=metadata,
            directory_id=f"{self.METADATA}/{contract_address}",
            document_key=str(tokenid)
        )
        if success:
            self.logger.debug(f"Saved metadata: {contract_address}/{tokenid}")

    def read_token_rarity(self, contract_address: str, tokenid: int) -> Optional[Rarity]:
        rarity_info = self.db.read_document(
            directory_id=f"{self.RARITY}/{contract_address}",
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
            directory_id=f"{self.RARITY}/{contract_address}",
            document_key=str(tokenid)
        )
        if success:
            self.logger.debug(f"Saved rarity: {contract_address}/{tokenid} ")

    def get_collection_address(self, collection: str) -> str:
        pass

    def get_token_rarity_rank(self, collection: str, tokenid: int):
        """
        Returns the calculated rarity rank based on the estimated rarities
        :param collection:
        :param tokenid:
        :return:
        """
        collection_address = self.get_collection_address(collection)
        token_rarity = self.read_token_rarity(collection_address, tokenid)
        return token_rarity.rarity_rank

    def get_token_fair_eth_price_estimation(self, collection: str, tokenid: int, listing_price: float):
        pass

    def _slug_to_address(self, slug: str) -> str:
        pass

    def _address_to_slug(self, collection_address: str) -> str:
        pass

    def _keys_to_ignore_from_metadata(self):
        return ['description']

    def _clean_metadata(self, metadata: dict) -> dict:
        metadata_copy = metadata.copy()
        for key in self._keys_to_ignore_from_metadata():
            try:
                del metadata_copy[key]
            except:
                pass
        return metadata_copy
