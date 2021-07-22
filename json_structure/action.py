from json_structure.action_variable import ActionVariable
from json_structure.condition import Condition
from json_structure.step import Step


class Action:
    def __init__(self, title, action):
        self.steps: list[Step] = []
        self.title: str = title
        self.action: str = action
        self.handlers: list[str] = []
        self.condition: Condition = Condition()
        self.variables: list[ActionVariable] = []
        self.next_action: str = None
        self.disambiguation_opt_out: bool = False
