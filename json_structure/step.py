from json_structure.step_output import StepOutput


class StepResolver:
    type: str = None


class Step:
    step: str = None
    output: StepOutput = StepOutput()
    handlers: list[str] = []
    resolver: StepResolver = StepResolver()
    variable: str = None
