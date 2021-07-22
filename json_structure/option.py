from json_structure.option_value import OptionValue


class Option:
    def __init__(self, label: str, input_value: str):
        self.label: str = label
        self.value: OptionValue = OptionValue(input_value)
