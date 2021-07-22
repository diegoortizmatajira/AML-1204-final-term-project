from excel_loading import ExcelInput, ExcelHeader
from json_structure.action import Action
from json_structure.condition import Condition
from json_structure.entity import Entity
from json_structure.entity_value import EntityValue
from json_structure.option import Option
from json_structure.skill import Skill

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


# Adds the standard greeting
def add_welcome_dialog(result: Skill, header: ExcelHeader):
    welcome_action = Action('Greet customer', 'welcome', Condition(expression='welcome'))
    welcome_action.add_response_text(get_step_name(), header.welcome_message)
    result.workspace.actions.append(welcome_action)


def add_service_feedback_dialog(result: Skill, header: ExcelHeader):
    feedback_entity = Entity('feedback_entity')
    feedback_entity.values.append(EntityValue('useful', ['yes']))
    feedback_entity.values.append(EntityValue('not useful', ['no']))
    result.workspace.entities.append(feedback_entity)
    feedback_action = Action('Service feedback', 'feedback', Condition(expression='true'))
    feedback_action.add_response_options(get_step_name(), header.feedback_message, [
        Option('Useful', 'yes'),
        Option('Not useful', 'no')
    ])
    result.workspace.actions.append(feedback_action)


def generate_skill(input: list[ExcelInput], header: ExcelHeader) -> Skill:
    result = Skill(header.name, header.description)
    add_welcome_dialog(result, header)
    # add_service_feedback_dialog(result, header)
    return result
