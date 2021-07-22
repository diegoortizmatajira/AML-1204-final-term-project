from json_structure.text_expression import TextExpression


class OutputValue:
    text_expression: TextExpression = None
    text: str = None

    def __init__(self, text: str = None, text_expression: TextExpression = None):
        self.text = text
        self.text_expression = text_expression
