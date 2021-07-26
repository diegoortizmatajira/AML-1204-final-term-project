import utils
from dialog_skill.dialog_node import DialogNode
from dialog_skill.entity import Entity
from dialog_skill.intent import Intent


class SkillMetadataApiVersion:
    def __init__(self):
        self.major_version: str = 'v1'
        self.minor_version: str = '2018-09-20'


class SkillMetadata:
    def __init__(self):
        self.api_version: SkillMetadataApiVersion = SkillMetadataApiVersion()


class Skill:
    def __init__(self, name: str, description: str, language: str):
        self.name = utils.clean_value(name)
        self.description = utils.clean_value(description)
        self.language = language
        self.intents: list[Intent] = []
        self.entities: list[Entity] = []
        self.metadata = SkillMetadata()
        self.dialog_nodes: list[DialogNode] = []
