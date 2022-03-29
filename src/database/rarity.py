class Rarity:
    PROBABILITY = "probability"
    LOGPROBABILITY = "logprobability"
    RARITY = "rarity"
    RARITYRANK = "rarity_rank"
    TOKENID = "tokenid"

    def __init__(self, rarity_info: dict):
        self.tokenid = int(rarity_info.get(self.TOKENID))
        self.rarity_rank = int(rarity_info.get(self.RARITYRANK))
        self.logprobability = rarity_info.get(self.LOGPROBABILITY)
        # self.probability = rarity_info.get(self.PROBABILITY, None)
        # self.rarity = rarity_info.get(self.RARITY, None)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.tokenid}>"
