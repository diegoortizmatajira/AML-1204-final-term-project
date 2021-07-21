from json_structure.action import Action
from json_structure.entity import Entity
from json_structure.intent import Intent
from json_structure.metadata import Metadata
from json_structure.system_settings import SystemSettings
from json_structure.variable import Variable


class Workspace:
    actions: list[Action] = []
    intents: list[Intent] = []
    entities: list[Entity] = []
    metadata: Metadata = Metadata()
    variables: list[Variable] = []
    counterexamples: [] = []
    system_settings: SystemSettings = SystemSettings()
    learning_opt_out: bool = False
