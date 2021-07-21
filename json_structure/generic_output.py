from json_structure.option import Option
from json_structure.output_value import OutputValue


class GenericOutput:
    values: list[OutputValue] = []
    option: list[Option] = []
    esponse_type: str = None
    selection_policy: str = 'sequential'
    repeat_on_reprompt: bool = True
