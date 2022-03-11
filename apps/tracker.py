# todo: should we track one collection per thread or multiple ones
# todo: I'll base my fair price exclusively on listings. That allows me to ignore mechanics of tracking both sells and listings

# todo: probably this should be re-done by tracking multiple collections in the same thread. Launch a thread every 20 collections or more

class CollectionTracker:
    def __init__(self, collection_id: str):
        # todo: try to keep this class as low-memory as possible. Multiple threads may be launched in paralell (for each collection)
        self.collection_id = collection_id
        pass

    def run(self):
        while True:
            # todo: retrieve new listings from opensea
            # todo: retrieve fair prices from database.
            # todo: CHALLENGE: an items listing should not affect itself, but only the next listings (perhaps neglectible if lambda high?)
            # todo: update collection fair price curve recursively (recursive linear fit on transformed data)
            # todo: update collection fairprice function in database
            pass
