"""
## Rarity calculations
- downloading tokens attributes (requests / openseaAPI)
- calculate rarity based on attributes appearance
- store rarity and rank in my databases
- estimate fair valuations using log(price/listings) & log(rarity)
- for new listings, calculate bargain-ratio and valuation-ratio
"""
import pandas as pd
import logging
import numpy as np
from src.database import Dao
from src.database import OpenseaCollection
import config
from src.database.metadata import Metadata
from src.database.rarity import Rarity


class RarityCalculator:
    TRAIT_FREQ = 'trait_freq'
    TRAIT_LOG_FREQ = 'trait_log_freq'

    def __init__(self, contract_address: str):
        self.dao = Dao()
        self.contract_address = contract_address
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_traitsdf(self) -> pd.DataFrame:
        collection = OpenseaCollection(self.contract_address)
        collection_attributes = []
        for tokenid in collection.token_ids():
            token_metadata = self.dao.read_token_metadata(self.contract_address, tokenid)
            if token_metadata is None:
                continue
            for attribute in token_metadata.attributes:
                attr = attribute.copy()
                attr.update({Metadata.TOKENID: tokenid})
                collection_attributes.append(attr)

        if not collection_attributes:
            self.logger.exception(f"collection attributes df is empty")
            return pd.DataFrame()

        traitsdf = pd.DataFrame(collection_attributes)
        traitsdf['count'] = 1
        traitsdf.set_index([Metadata.TRAIT_TYPE, Metadata.TRAIT_VALUE], inplace=True)
        return traitsdf

    def estimate_rarities(self, traitsdf: pd.DataFrame):
        n_unique_tokens = len(set(traitsdf[Metadata.TOKENID]))
        trait_freqs = traitsdf.groupby([Metadata.TRAIT_TYPE, Metadata.TRAIT_VALUE])['count'].sum() / n_unique_tokens
        # traitsdf[self.TRAIT_FREQ] = trait_freqs
        traitsdf[self.TRAIT_LOG_FREQ] = np.log(trait_freqs)
        # Rarities is the product of all probabilities (lower product, more rarity)
        # np.log(traitsdf.groupby(Metadata.TOKENID)[self.TRAIT_FREQ].apply(np.prod))
        raritiesdf = traitsdf.groupby(Metadata.TOKENID)[self.TRAIT_LOG_FREQ].sum().to_frame(Rarity.LOGPROBABILITY)
        raritiesdf.sort_values(by=Rarity.LOGPROBABILITY, inplace=True)
        raritiesdf[Rarity.RARITYRANK] = np.arange(1, len(raritiesdf) + 1)
        raritiesdf.sort_index(inplace=True)
        return raritiesdf

    def run(self):
        self.logger.debug(f"Collecting traits from database")
        traitsdf = self.get_traitsdf()

        self.logger.info(f"Computing rarities")
        raritiesdf = self.estimate_rarities(traitsdf)

        self.logger.info(f"Saving rarities in database")
        for tokenid, tokeninfo in raritiesdf.iterrows():
            self.dao.save_token_rarity(tokeninfo.to_dict(), self.contract_address, tokenid)

        self.logger.info(f"Rarities processing done.")
