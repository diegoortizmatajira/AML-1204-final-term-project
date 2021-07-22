from json_structure.action import Action
from json_structure.entity import Entity
from json_structure.intent import Intent
from json_structure.metadata import Metadata
from json_structure.system_settings import SystemSettings
from json_structure.variable import Variable


class Workspace:
    def __init__(self):
        self.actions: list[Action] = []
        self.intents: list[Intent] = []
        self.entities: list[Entity] = []
        self.metadata: Metadata = Metadata()
        self.variables: list[Variable] = []
        self.counterexamples: [] = []
        self.system_settings: SystemSettings = SystemSettings()
        self.learning_opt_out: bool = False
