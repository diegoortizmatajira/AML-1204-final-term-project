from json_structure.entity_value import EntityValue


class Entity:
    def __init__(self, entity):
        self.entity: str = entity
        self.values: list[EntityValue] = []
        self.fuzzy_match: bool = True
