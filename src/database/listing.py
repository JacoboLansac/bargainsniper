class Listing:
    TOKENID = "tokenid"
    COLLECTION_SLUG = "collection_slug"
    PRICE_ETH = 'price_eth'
    COLLECTION_ADDRESS = "collection_address"

    def __init__(self, listing_info: dict):
        self.tokenid = int(listing_info.get(self.TOKENID))
        self.collection_slug = int(listing_info.get(self.COLLECTION_SLUG))
        self.collection_address = listing_info.get(self.COLLECTION_ADDRESS)
        self.price_eth = listing_info.get(self.PRICE_ETH)
        self.info = listing_info.copy()

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.tokenid}>"
