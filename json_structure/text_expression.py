class ScalarTextExpression:
    def __init__(self, scalar: str):
        self.scalar: str = scalar


class TextExpression:
    def __init__(self, scalar_list: list[str]):
        self.concat: list[ScalarTextExpression] = []
        for scalar in scalar_list:
            self.add_scalar(scalar)

    def add_scalar(self, scalar: str):
        self.concat.append(ScalarTextExpression(scalar))
