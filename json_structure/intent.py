class IntentExamples:
    def __init__(self):
        self.text: str = None


class Intent:
    def __init__(self):
        self.intent: str = None
        self.examples: list[IntentExamples] = []
