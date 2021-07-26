import utils

ENTITY_VALUE_TYPE_SYNONYMS = 'synonyms'
ENTITY_VALUE_TYPE_PATTER = 'pattern'


class EntityValue:
    def __init__(self, entity_type: str, value: str, synonyms: list[str]):
        self.type = entity_type
        self.value = utils.clean_value(value)
        self.synonyms = []
        for synonym in synonyms:
            self.synonyms.append(utils.clean_value(synonym))


class Entity:
    def __init__(self, name: str, values: list[EntityValue], fuzzy_match: bool = False):
        self.entity = utils.generate_identifier(name)
        self.fuzzy_match = fuzzy_match
        self.values: list[EntityValue] = values
