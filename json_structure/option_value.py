class OptionValueInput:
    def __init__(self, text):
        self.text: str = text


class OptionValue:
    def __init__(self, text):
        self.input: OptionValueInput = OptionValueInput(text)
