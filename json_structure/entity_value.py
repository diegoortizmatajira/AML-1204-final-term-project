class EntityValue:
    def __init__(self, value: str, synonyms: list[str]):
        self.type: str = 'synonyms'
        self.value: str = value
        self.synonyms: list[str] = synonyms
