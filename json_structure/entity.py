from json_structure.entity_value import EntityValue


class Entity:
    def __init__(self):
        self.entity: str = None
        self.values: list[EntityValue] = []
        self.fuzzy_match: bool = True
