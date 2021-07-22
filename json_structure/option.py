from json_structure.option_value import OptionValue


class Option:
    def __init__(self):
        self.label: str = None
        self.value: OptionValue = OptionValue()
