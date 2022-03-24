
class Metadata:
    NAME = "name"
    ATTRIBUTES = "attributes"
    IMAGE = "image"
    DESCRIPTION = "description"
    TRAIT_TYPE = "trait_type"
    TRAIT_VALUE = "value"
    TOKENID = "tokenid"

    def __init__(self, metadata: dict):
        self.name = metadata.get(self.NAME, None)
        self.image = metadata.get(self.IMAGE, None)
        self.attributes = metadata.get(self.ATTRIBUTES, [])
        self.tokenid = metadata.get(self.TOKENID, None)

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.name}>"
