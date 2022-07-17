import os

from .database import Database
from .metadata import Metadata
from .rarity import Rarity
from logging import getLogger
from typing import Optional, List
import os


class DaoMetadata:
    METADATA = 'metadata'
    TOKENID = 'tokenid'

    def __init__(self):
        self.db = Database()
        self.logger = getLogger(self.__class__.__name__)

    def collection_directory_id(self, contract_address: str) -> str:
        return f"{self.METADATA}/{contract_address}"

    def list_available_collections(self):
        return self.db.list_directories(self.METADATA)

    def is_collection_available(self, contract_address: str) -> bool:
        return self.db.exists_directory(self.collection_directory_id(contract_address))

    def read_token_metadata(self, contract_address: str, tokenid: int) -> Optional[Metadata]:
        metadata = self.db.read_document(
            directory_id=self.collection_directory_id(contract_address),
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
            directory_id=self.collection_directory_id(contract_address),
            document_key=str(tokenid)
        )
        if success:
            self.logger.debug(f"Saved metadata: {contract_address}/{tokenid}")

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

    def list_available_tokenids(self, contract_address:str) -> List[int]:
        return sorted(int(tokenid) for tokenid in self.db.list_documents(self.collection_directory_id(contract_address)))