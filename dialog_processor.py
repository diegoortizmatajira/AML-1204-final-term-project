from typing import Callable, Optional

from dialog_skill.dialog_node import StandardDialogNode, OptionResponse, FolderDialogNode, \
    DialogNode, DialogNodeNextStep
from dialog_skill.entity import Entity, EntityValue, ENTITY_VALUE_TYPE_SYNONYMS
from dialog_skill.intent import Intent
from dialog_skill.skill import Skill
from excel_loading import ExcelHeader, ExcelInput

node_count = 0
menu_intent_count = 0
menu_count = 0
question_count = 0
previous_menu_link_id = None


def get_node_id() -> str:
    global node_count
    node_count = node_count + 1
    return f'node_{node_count:04d}'


def get_menu_id() -> str:
    global menu_count
    menu_count = menu_count + 1
    return f'menu_option_{menu_count:04d}'


def get_menu_intent_id() -> str:
    global menu_intent_count
    menu_intent_count = menu_intent_count + 1
    return f'menu_intent_{menu_intent_count:04d}'


def get_question_intent_id() -> str:
    global question_count
    question_count = question_count + 1
    return f'question_intent_{question_count:04d}'


def add_initial_dialog(result: Skill, header: ExcelHeader) -> (str, str):
    welcome_dialog_node = StandardDialogNode(get_node_id(), 'Welcome', 'welcome')
    welcome_dialog_node.add_response_paragraph(header.welcome_message)
    result.dialog_nodes.append(welcome_dialog_node)

    service_feedback_entity = Entity('service_feedback_options', [
        EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, 'Not useful', ['No']),
        EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, 'Useful', ['Yes'])
    ], True)
    result.entities.append(service_feedback_entity)

    service_feedback_node = StandardDialogNode(get_node_id(), 'Service feedback', '')
    service_feedback_node.previous_sibling = welcome_dialog_node.dialog_node
    service_feedback_node.add_response_options("Was the answer you received useful?", [
        OptionResponse("Yes", "Useful"),
        OptionResponse("No", "Not useful")
    ])
    result.dialog_nodes.append(service_feedback_node)

    formal_query_entity = Entity("formal_query_entity", [
        EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, "Finish", ["No, thank you", "That's it", "End", "Exit"])
    ], True)
    result.entities.append(formal_query_entity)

    formal_query_node = StandardDialogNode(get_node_id(), header.formal_offering_message,
                                           f"@{formal_query_entity.entity}")
    formal_query_node.parent = service_feedback_node.dialog_node
    formal_query_node.add_response_options(header.formal_offering_message, [
        OptionResponse("Menu", "Menu"),
        OptionResponse("No, thank you..", "Finish")
    ])
    result.dialog_nodes.append(formal_query_node)

    finish_node = StandardDialogNode(get_node_id(), "Finish", f"@{formal_query_entity.entity}:Finish")
    finish_node.parent = formal_query_node.dialog_node
    finish_node.add_response_paragraph(header.final_message)
    result.dialog_nodes.append(finish_node)

    return service_feedback_node.dialog_node, service_feedback_node.dialog_node


def add_not_understanding_dialog(result: Skill, previous_sibling_id: str):
    not_understanding_node = StandardDialogNode(get_node_id(), "Not understanding", "anything_else")
    not_understanding_node.add_response_paragraphs([
        "I haven't understood, Please re-phrase the query.",
        "Can you use other words? I didn't got what you said",
        "Cannot understand the meaning"
    ])
    not_understanding_node.previous_sibling = previous_sibling_id
    result.dialog_nodes.append(not_understanding_node)


def add_menu_folder(result: Skill, previous_sibling_id: str):
    new_folder_node = FolderDialogNode(get_node_id(), "Folder for menu dialog nodes")
    new_folder_node.previous_sibling = previous_sibling_id
    result.dialog_nodes.append(new_folder_node)
    return new_folder_node.dialog_node, new_folder_node.dialog_node


def add_main_menu(result: Skill, previous_sibling_id: str, header: ExcelHeader) -> (str, DialogNode, Entity):
    main_menu_intention = Intent(get_menu_intent_id(), "Intention to view the main menu", [
        "Menu",
        "What can you do?",
        "How can you help me?"
    ])
    result.intents.append(main_menu_intention)

    main_menu_node = StandardDialogNode(get_node_id(), "Main Menu", f"#{main_menu_intention.intent}")
    main_menu_node.PreviousSiblingId = previous_sibling_id
    main_menu_node.add_response_options(header.selection_message, [])
    result.dialog_nodes.append(main_menu_node)

    main_menu_entity = Entity('main_menu_options', [], True)
    result.entities.append(main_menu_entity)

    return main_menu_node.dialog_node, main_menu_node, main_menu_entity


class ProcessingContext:
    def __init__(self, level: int, parent_node: Optional[DialogNode], previous_sibling_id: Optional[str],
                 menu_node: Optional[StandardDialogNode],
                 menu_entity: Optional[Entity], formal_query_id: str, menu_folder_id: str,
                 previous_menu_id: Optional[str]):
        self.level = level
        self.parent_node = parent_node
        self.previous_sibling_id = previous_sibling_id
        self.menu_node = menu_node
        self.menu_entity = menu_entity
        self.formal_query_id = formal_query_id
        self.menu_folder_id = menu_folder_id
        self.previous_menu_id = previous_menu_id

    def new_folder_context(self, new_folder: str):
        new_folder_node = FolderDialogNode(get_node_id(), new_folder)
        if self.parent_node:
            new_folder_node.parent = self.parent_node.dialog_node
        new_folder_node.previous_sibling = self.previous_sibling_id

        return ProcessingContext(
            level=self.level + 1,
            parent_node=new_folder_node,
            previous_sibling_id=None,
            menu_node=None,
            menu_entity=None,
            formal_query_id=self.formal_query_id,
            menu_folder_id=self.menu_folder_id,
            previous_menu_id=None
        )

    def new_finish_context(self):
        return ProcessingContext(
            level=99999,
            parent_node=self.parent_node,
            previous_sibling_id=self.previous_sibling_id,
            menu_node=self.menu_node,
            menu_entity=self.menu_entity,
            previous_menu_id=None,
            formal_query_id=self.formal_query_id,
            menu_folder_id=self.menu_folder_id
        )


def get_grouping_criteria(level: int) -> Optional[Callable[[ExcelInput], str]]:
    if level == 1:
        return lambda row: row.Category_1
    elif level == 2:
        return lambda row: row.Category_2
    elif level == 3:
        return lambda row: row.Category_3
    elif level == 4:
        return lambda row: row.Category_4
    elif level == 4:
        return lambda row: row.Category_5
    else:
        return None


def get_groups(questions: list[ExcelInput], criteria: Callable[[ExcelInput], str]) -> dict[str, list[ExcelInput]]:
    result = {}
    for question in questions:
        key = criteria(question)
        group_list = result.get(key, [])
        group_list.append(question)
        result[key] = group_list
    return result


def has_menu_options(questions: list[ExcelInput]) -> bool:
    for question in questions:
        if not question.Show_in_menu:
            return False
    return True


def create_menu(result: Skill, header: ExcelHeader, menu_name: str, context: ProcessingContext) -> (DialogNode, Entity):
    context.menu_entity.values.append(EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, menu_name, []))
    context.menu_node.add_options_to_last_response(menu_name, header.selection_continuation_message)

    menu_node = StandardDialogNode(get_node_id(), menu_name, f'@{context.menu_entity.entity}:{menu_name}')
    menu_node.parent = context.menu_node.dialog_node
    menu_node.previous_sibling = context.previous_menu_id
    menu_node.add_response_options(header.selection_message, [])
    result.dialog_nodes.append(menu_node)

    menu_entity = Entity(get_menu_id(), [])
    result.entities.append(menu_entity)

    return menu_node, menu_entity


def clean_skill_empty_nodes(result: Skill) -> Skill:
    for entity in result.entities[:]:
        if len(entity.values) == 0:
            result.entities.remove(entity)
    return result


def process_level(result: Skill, questions: list[ExcelInput], header: ExcelHeader, context: ProcessingContext) -> str:
    global previous_menu_link_id
    criteria = get_grouping_criteria(context.level)
    if criteria:
        # Get the questions grouped by the values in the category column corresponding to the level
        groups = get_groups(questions, criteria)
        for key, group_list in groups.items():
            if key:
                new_folder_context = context.new_folder_context(key)
                result.dialog_nodes.append(new_folder_context.parent_node)
                if context.menu_node and context.menu_entity and has_menu_options(group_list):
                    new_folder_context.menu_node, new_folder_context.menu_entity = create_menu(result, header, key,
                                                                                               context)
                    context.previous_menu_id = new_folder_context.menu_node.dialog_node
                menu_intention = Intent(get_menu_intent_id(), key, [key])
                result.intents.append(menu_intention)

                link_node = StandardDialogNode(get_node_id(), key, f'#{menu_intention.intent}')
                link_node.parent = new_folder_context.menu_folder_id
                link_node.previous_sibling = previous_menu_link_id
                link_node.next_step = DialogNodeNextStep(new_folder_context.menu_node.dialog_node)
                result.dialog_nodes.append(link_node)
                previous_menu_link_id = link_node.dialog_node

                process_level(result, group_list, header, new_folder_context)
                if new_folder_context.parent_node:
                    context.previous_sibling_id = new_folder_context.parent_node.dialog_node
            else:
                context.previous_sibling_id = process_level(result, group_list, header, context.new_finish_context())
    else:
        # If there is no grouping criteria, it creates the questions
        for question in questions:
            if context.menu_node and context.menu_entity and question.Show_in_menu:
                context.menu_node.add_options_to_last_response(question.Question, header.selection_continuation_message)

            question_intent = Intent(get_question_intent_id(), question.Question, [question.Question])
            result.intents.append(question_intent)

            answer_node = StandardDialogNode(get_node_id(), question.Question, f'#{question_intent.intent}')
            answer_node.add_response_paragraph(question.Answer)
            if context.parent_node:
                answer_node.parent = context.parent_node.dialog_node
            answer_node.previous_sibling = context.previous_sibling_id
            answer_node.next_step = DialogNodeNextStep(context.formal_query_id)
            result.dialog_nodes.append(answer_node)
            context.previous_sibling_id = answer_node.dialog_node

    return context.previous_sibling_id


def generate_dialog_skill(questions: list[ExcelInput], header: ExcelHeader) -> Skill:
    result = Skill(header.name, header.description, 'en')
    previous_sibling_id, formal_query_id = add_initial_dialog(result, header)
    previous_sibling_id, menu_folder_id = add_menu_folder(result, previous_sibling_id)
    previous_sibling_id, main_menu_node, main_menu_entity = add_main_menu(result, previous_sibling_id, header)
    initial_context = ProcessingContext(
        level=1,
        parent_node=None,
        previous_sibling_id=previous_sibling_id,
        menu_node=main_menu_node,
        menu_entity=main_menu_entity,
        formal_query_id=formal_query_id,
        menu_folder_id=menu_folder_id,
        previous_menu_id=None
    )
    previous_sibling_id = process_level(result, questions, header, initial_context)
    add_not_understanding_dialog(result, previous_sibling_id)
    return clean_skill_empty_nodes(result)
