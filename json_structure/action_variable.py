from utils import clean_title


class ActionVariable:
    def __init__(self, variable: str, title: str = None):
        self.title: str = clean_title(title)
        self.variable: str = variable
