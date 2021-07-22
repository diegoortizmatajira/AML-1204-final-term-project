class ScalarTextExpression:
    def __init__(self, scalar: str):
        self.scalar: str = scalar


class TextExpression:
    def __init__(self):
        self.concat: list[ScalarTextExpression] = []

    def add_scalar(self, scalar: str):
        self.concat.append(ScalarTextExpression(scalar))
