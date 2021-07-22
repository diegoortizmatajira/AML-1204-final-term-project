from excel_loading import ExcelInput, ExcelHeader
from json_structure.action import Action
from json_structure.output_value import OutputValue
from json_structure.skill import Skill
from json_structure.step import Step

question_count = 0
menu_count = 0
step_count = 0
menu_intention_count = 0
previous_action_id = None


# Generates a step name incrementing the counter
def get_step_name() -> str:
    global step_count
    step_count = step_count + 1
    return f'step_{step_count:04d}'


# Adds the standard greeting and default common chat elements
def add_initial_dialog(result: Skill, header: ExcelHeader):
    welcome_action = Action('Greet customer', 'welcome')
    welcome_step1 = Step(get_step_name())
    welcome_step1.output.generic.values.append(OutputValue(text=header.welcome_message))
    welcome_step1.output.generic.response_type = 'text'
    welcome_step1.resolver.type = 'continue'
    welcome_action.steps.append(welcome_step1)
    result.workspace.actions.append(welcome_action)


def generate_skill(input: list[ExcelInput], header: ExcelHeader) -> Skill:
    result = Skill(header.name, header.description)
    add_initial_dialog(result, header)
    return result
