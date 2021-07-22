class EntityValue:
    def __init__(self):
        self.type: str = 'synonyms'
        self.value: str = None
        self.synonyms: list[str] = []
