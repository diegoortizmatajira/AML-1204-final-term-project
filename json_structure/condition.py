class Condition:
    def __init__(self, intent: str = None, expression: str = None):
        self.intent: str = intent
        self.expression: str = expression
