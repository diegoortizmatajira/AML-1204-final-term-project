from json_structure.entity_value import EntityValue


class Entity:
    def __init__(self, entity, values: list[EntityValue]):
        self.entity: str = entity
        self.values: list[EntityValue] = values
        self.fuzzy_match: bool = True

    def add_value(self, value: str, synonyms: list[str]):
        self.values.append(EntityValue(value, synonyms))
