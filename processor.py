from excel_loading import ExcelInput, ExcelHeader
from json_structure.action import Action
from json_structure.condition import Condition
from json_structure.entity import Entity
from json_structure.entity_value import EntityValue
from json_structure.intent import Intent
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


def get_question_name() -> str:
    global question_count
    question_count = question_count + 1
    return f'question_{question_count:04d}'


def add_welcome_dialog(result: Skill, header: ExcelHeader):
    # Adds the standard greeting
    welcome_action = Action('Greet customer', 'welcome', Condition(expression='welcome'))
    welcome_action.add_response_text(get_step_name(), header.welcome_message)
    result.workspace.actions.append(welcome_action)


def add_question(result: Skill, question: ExcelInput):
    question_name = get_question_name()
    intent_name = question_name
    question_intent = Intent(intent_name, [question.Question])
    result.workspace.intents.append(question_intent)

    question_action = Action(question_name, question_name, condition=Condition(intent=intent_name))
    question_action.add_response_text(get_step_name(), question.Answer)
    result.workspace.actions.append(question_action)


def generate_skill(questions: list[ExcelInput], header: ExcelHeader) -> Skill:
    result = Skill(header.name, header.description)
    add_welcome_dialog(result, header)
    for question in questions:
        add_question(result, question)
    return result
