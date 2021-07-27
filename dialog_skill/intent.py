import utils
from dialog_skill.text_item import TextItem


class Intent:
    def __init__(self, name: str, description: str, examples: list[str]):
        self.intent = utils.generate_identifier(name)
        self.description = utils.clean_value(description)
        self.examples = []
        for example in examples:
            self.examples.append(TextItem(utils.clean_value(example)))
