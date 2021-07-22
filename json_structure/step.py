from json_structure.step_output import StepOutput


class StepResolver:
    def __init__(self):
        self.type: str = None


class Step:
    def __init__(self, step):
        self.step: str = step
        self.output: StepOutput = StepOutput()
        self.handlers: list[str] = []
        self.resolver: StepResolver = StepResolver()
        self.variable: str = None
