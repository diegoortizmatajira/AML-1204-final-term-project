from json_structure.option import Option
from json_structure.output_value import OutputValue


class GenericOutput:
    def __init__(self):
        self.values: list[OutputValue] = []
        self.option: list[Option] = []
        self.response_type: str = None
        self.selection_policy: str = 'sequential'
        self.repeat_on_reprompt: bool = True
