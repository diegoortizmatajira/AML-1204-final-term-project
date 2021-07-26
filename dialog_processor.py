from dialog_skill.dialog_node import StandardDialogNode, GenericOptionsOutput, OptionResponse, FolderDialogNode
from dialog_skill.entity import Entity, EntityValue, ENTITY_VALUE_TYPE_SYNONYMS
from dialog_skill.skill import Skill
from excel_loading import ExcelHeader, ExcelInput

contadorPreguntas = 0
contadorMenus = 0
contadorIntencionesMenus = 0
idNodoEnlaceMenuPredecesor = None
node_count = 0


def get_node_id() -> str:
    global node_count
    node_count = node_count + 1
    return f'node_{node_count:04d}'


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
    service_feedback_node.previous_sibling = welcome_dialog_node.id
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
    formal_query_node.parent = service_feedback_node.id
    formal_query_node.add_response_options(header.formal_offering_message, [
        OptionResponse("Menu", "Menu"),
        OptionResponse("No, thank you..", "Finish")
    ])
    result.dialog_nodes.append(formal_query_node)

    finish_node = StandardDialogNode(get_node_id(), "Finish", f"@{formal_query_entity.entity}:Finish")
    finish_node.parent = formal_query_node.id
    finish_node.add_response_paragraph(header.final_message)
    result.dialog_nodes.append(finish_node)

    return service_feedback_node.id, service_feedback_node.id


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
    new_folder_node.previous_sibling = previous_sibling_id;
    result.dialog_nodes.append(new_folder_node);
    return new_folder_node.id, new_folder_node.id


def generate_dialog_skill(questions: list[ExcelInput], header: ExcelHeader) -> Skill:
    result = Skill(header.name, header.description, 'en')
    previous_sibling_id, formal_query_id = add_initial_dialog(result, header)
    previous_sibling_id, menu_folder_id = add_menu_folder(result, previous_sibling_id)

    add_not_understanding_dialog(result, previous_sibling_id)
    return result
