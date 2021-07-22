from json_structure.action_variable import ActionVariable
from json_structure.condition import Condition
from json_structure.generic_output import GenericOutput
from json_structure.option import Option
from json_structure.option_value import OptionValue
from json_structure.output_value import OutputValue
from json_structure.step import Step
from json_structure.text_expression import TextExpression


class Action:
    def __init__(self, title: str, action: str):
        self.steps: list[Step] = []
        self.title: str = title
        self.action: str = action
        self.handlers: list[str] = []
        self.condition: Condition = Condition()
        self.variables: list[ActionVariable] = []
        self.next_action: str = None
        self.disambiguation_opt_out: bool = False

    def add_response_text(self, step_name: str, text: str):
        if text:
            step = Step(step_name)
            generic_response = GenericOutput()
            generic_response.values.append(OutputValue(text=text))
            generic_response.response_type = 'text'
            step.output.generic.append(generic_response)
            step.resolver.type = 'continue'
            self.steps.append(step)

    def add_response_options(self, step_name: str, text: str, options: list[Option]):
        if text:
            step = Step(step_name)
            # Adds the text before showing the options
            generic_text_response = GenericOutput()
            generic_text_response.values.append(OutputValue(text_expression=TextExpression([text])))
            generic_text_response.response_type = 'text'
            generic_text_response.selection_policy = 'sequential'
            step.output.generic.append(generic_text_response)
            # Adds the options to be shown
            generic_options_response = GenericOutput()
            generic_options_response.options = options
            generic_options_response.response_type = 'option'
            generic_options_response.repeat_on_reprompt = True
            step.output.generic.append(generic_options_response)
            step.resolver.type = 'continue'
            self.steps.append(step)
