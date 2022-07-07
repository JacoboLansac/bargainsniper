import os
from typing import Optional
import json
from logging import getLogger
import config
from os import path


class FilesDB:
    def __init__(self):
        self.logger = getLogger(self.__class__.__name__)
        self.rootpath = config.filesdb_rootpath

    def save_document(self, document: dict, directory_id: str, document_key: (int, str), overwrite=True) -> bool:
        if not self.create_directory(directory_id):
            self.create_directory(directory_id)

        document_path = self._document_path(directory_id, document_key)

        if path.isfile(document_path) and not overwrite:
            self.logger.exception(f"{document_path} already exists and overwrite=False")
            return False
        else:
            try:
                json.dump(document, open(document_path, 'w'), indent=2)
                return True
            except:
                self.logger.exception(f"Could not save document: {document_path}")
                return False

    def read_document(self, directory_id: str, document_key: (str, int)) -> Optional[dict]:
        document_path = self._document_path(directory_id, document_key)
        if path.isfile(document_path):
            try:
                return json.load(open(document_path, 'r'))
            except:
                self.logger.exception(f"Could not read document: {document_path}")
                return None
        self.logger.error(f"Document not existing: {document_path}")
        return None

    def list_documents(self, directory_id:str) -> list:
        directory = self._directory_path(directory_id)
        try:
            return os.listdir(directory)
        except:
            return []

    def exists_directory(self, directory_id: str) -> bool:
        return path.isdir(self._directory_path(directory_id))

    def create_directory(self, directory_id: str):
        os.makedirs(self._directory_path(directory_id), exist_ok=True)

    def find_document(self, directory_id: str, filters: tuple):
        raise NotImplementedError

    def _directory_path(self, directory_id: str):
        return path.join(self.rootpath, directory_id)

    def _document_path(self, directory_id: str, document_key: str):
        return path.join(self._directory_path(directory_id), str(document_key))

