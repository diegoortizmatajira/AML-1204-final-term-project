from json_structure.option import Option
from json_structure.output_value import OutputValue


class GenericOutput:
    def __init__(self):
        self.values: list[OutputValue] = None
        self.options: list[Option] = None
        self.response_type: str = None
        self.selection_policy: str = None
        self.repeat_on_reprompt: bool = None
