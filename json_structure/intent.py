class IntentExamples:
    def __init__(self, text: str):
        self.text: str = text


class Intent:
    def __init__(self, intent: str, examples: list[str]):
        self.intent: str = intent
        self.examples: list[IntentExamples] = []
        for example in examples:
            self.examples.append(IntentExamples(example))
