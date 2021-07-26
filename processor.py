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


def add_welcome_dialog(result: Skill, header: ExcelHeader, next_action: str):
    # Adds the standard greeting
    welcome_action = Action('Greet customer', 'welcome', Condition(expression='welcome'))
    welcome_action.add_response_text(get_step_name(), header.welcome_message)
    welcome_action.next_action = next_action
    result.workspace.actions.append(welcome_action)


def add_question(result: Skill, question: ExcelInput, next_action: str):
    question_name = get_question_name()
    intent_name = question_name
    question_intent = Intent(intent_name, [question.Question])
    result.workspace.intents.append(question_intent)

    question_action = Action(question.Question, question_name, condition=Condition(intent=intent_name))
    question_action.add_response_text_expression(get_step_name(), question.Answer)
    question_action.next_action = next_action
    result.workspace.actions.append(question_action)


def add_menu(result: Skill, questions: list[ExcelInput]):
    print('do something')
    # I have to iterate through the different values in Category_1
    # for each value create an intention with the value
    # create an action to display options with the values of Category_2 related to category_1
    menu_intent = Intent('menu_intent', ['Category 1'])
    result.workspace.intents.append(menu_intent)

    menu_entity = Entity('options_category_1', [
        EntityValue('Subcategory 1', []),
        EntityValue('Subcategory 2', []),
        EntityValue('question 1', [])
    ])
    result.workspace.entities.append(menu_entity)

    menu_action = Action('namexxx', 'namexxx', condition=Condition(intent='menu_intent'))
    menu_action.add_response_options(get_step_name(), 'Please select one option', [
        Option('Subcategory 1', 'Subcategory 1'),
        Option('Subcategory 2', 'Subcategory 2'),
        Option('question 1', 'question 1'),
    ], 'options_category_1')
    result.workspace.actions.append(menu_action)

    return menu_action.action


def generate_skill(questions: list[ExcelInput], header: ExcelHeader) -> Skill:
    result = Skill(header.name, header.description)
    main_menu = add_menu(result, questions)
    add_welcome_dialog(result, header, main_menu)
    for question in questions:
        add_question(result, question, main_menu)
    return result
