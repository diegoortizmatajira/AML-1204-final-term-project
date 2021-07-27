from typing import Optional

import utils
from dialog_skill.text_item import TextItem

DIALOG_NODE_TYPE_FRAME = 'frame'
DIALOG_NODE_TYPE_EVENT_HANDLER = 'event_handler'
DIALOG_NODE_TYPE_RESPONSE_CONDITION = 'response_condition'
DIALOG_NODE_TYPE_STANDARD = 'standard'
DIALOG_NODE_TYPE_FOLDER = 'folder'

GENERIC_TYPE_TEXT = 'text'
GENERIC_TYPE_OPTION = 'option'


class OptionResponseValue:
    def __init__(self, input_value: str):
        self.input = TextItem(input_value)


class OptionResponse:
    def __init__(self, label: str, value: str):
        self.label = label
        self.value = OptionResponseValue(value)


class GenericOutput:
    def __init__(self, response_type: str):
        self.response_type = response_type
        self.options: Optional[list[OptionResponse]] = None


class GenericTextOutput(GenericOutput):
    def __init__(self, texts: list[str]):
        GenericOutput.__init__(self, GENERIC_TYPE_TEXT)
        self.values: list[TextItem] = []
        for text in texts:
            self.values.append(TextItem(text))


class GenericOptionsOutput(GenericOutput):
    def __init__(self, title: str, options: list[OptionResponse]):
        GenericOutput.__init__(self, GENERIC_TYPE_OPTION)
        self.title = title
        self.options: list[OptionResponse] = options


class DialogOutput:
    def __init__(self):
        self.generic: list[GenericOutput] = []


SELECTION_POLICY_TYPE_SEQUENTIAL = 'sequential'
DIALOG_NODE_NEXT_STEP_BEHAVIOR_JUMP_TO = 'jump_to'
DIALOG_NODE_NEXT_STEP_SELECTOR_BODY = 'body'


class DialogNodeNextStep:
    def __init__(self, dialog_node: str):
        self.behavior = DIALOG_NODE_NEXT_STEP_BEHAVIOR_JUMP_TO
        self.selector = DIALOG_NODE_NEXT_STEP_SELECTOR_BODY
        self.dialog_node = dialog_node


class DialogNode:
    def __init__(self, node_id: str, title: str, node_type: str):
        self.dialog_node = node_id
        self.title = utils.clean_value(title)
        self.type = node_type
        self.parent: Optional[str] = None
        self.previous_sibling = None
        self.metadata = {}
        self.selection_policy = SELECTION_POLICY_TYPE_SEQUENTIAL
        self.next_step = None


class FolderDialogNode(DialogNode):
    def __init__(self, node_id: str, title: str):
        DialogNode.__init__(self, node_id, title, DIALOG_NODE_TYPE_FOLDER)


class StandardDialogNode(DialogNode):
    def __init__(self, node_id: str, title, condition):
        DialogNode.__init__(self, node_id, title, DIALOG_NODE_TYPE_STANDARD)
        self.conditions = condition
        self.output = DialogOutput()

    def add_response_paragraph(self, text: str):
        self.output.generic.append(GenericTextOutput([text]))

    def add_response_paragraphs(self, texts: list[str]):
        self.output.generic.append(GenericTextOutput(texts))

    def add_response_options(self, title: str, options: list[OptionResponse]):
        self.output.generic.append(GenericOptionsOutput(title, options))

    def add_options_to_last_response(self, menu_name: str, other_options_text: str):
        current_menu_answer = self.output.generic[-1]
        if len(current_menu_answer.options) == 20:
            current_menu_answer = GenericOptionsOutput(other_options_text)
            self.output.generic.append(current_menu_answer)
        current_menu_answer.options.append(OptionResponse(menu_name, menu_name))
