from typing import Callable, Optional

from dialog_skill.dialog_node import StandardDialogNode, OptionResponse, FolderDialogNode, \
    DialogNode, DialogNodeNextStep
from dialog_skill.entity import Entity, EntityValue, ENTITY_VALUE_TYPE_SYNONYMS
from dialog_skill.intent import Intent
from dialog_skill.skill import Skill
from excel_loading import ExcelHeader, ExcelInput

# Counters for created automatic identifiers
node_count = 0
menu_intent_count = 0
menu_count = 0
question_count = 0
# References the last menu that was created
previous_menu_link_id = None


# Generates an identifier based on Node counter
def get_node_id() -> str:
    global node_count
    node_count = node_count + 1
    return f'node_{node_count:04d}'


# Generates an identifier based on Menu counter
def get_menu_id() -> str:
    global menu_count
    menu_count = menu_count + 1
    return f'menu_option_{menu_count:04d}'


# Generates an identifier based on Menu intent counter
def get_menu_intent_id() -> str:
    global menu_intent_count
    menu_intent_count = menu_intent_count + 1
    return f'menu_intent_{menu_intent_count:04d}'


# Generates an identifier based on question counter
def get_question_intent_id() -> str:
    global question_count
    question_count = question_count + 1
    return f'question_intent_{question_count:04d}'


# Adds the standard dialogs (Welcome, service feedback, formal continue asking) and its corresponding entities
def add_initial_dialog(result: Skill, header: ExcelHeader) -> (str, str):
    # Creates the welcome message dialog node to start the conversation
    welcome_dialog_node = StandardDialogNode(get_node_id(), 'Welcome', 'welcome')
    welcome_dialog_node.add_response_paragraph(header.welcome_message)
    result.dialog_nodes.append(welcome_dialog_node)

    # Creates the feedback entity to ask the user if the provided answer was useful or not
    service_feedback_entity = Entity('service_feedback_options', [
        EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, 'Not useful', ['No']),
        EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, 'Useful', ['Yes'])
    ], True)
    result.entities.append(service_feedback_entity)

    # Creates the feedback dialog node to ask the user if the provided answer was useful or not
    service_feedback_node = StandardDialogNode(get_node_id(), 'Service feedback', '')
    service_feedback_node.previous_sibling = welcome_dialog_node.dialog_node
    service_feedback_node.add_response_options("Was the answer you received useful?", [
        OptionResponse("Yes", "Useful"),
        OptionResponse("No", "Not useful")
    ])
    result.dialog_nodes.append(service_feedback_node)

    # Creates the entity with values to identify if the users wants to finish the conversation
    formal_query_entity = Entity("formal_query_entity", [
        EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, "Finish", ["Finish", "No, thank you", "That's it", "End", "Exit"])
    ], True)
    result.entities.append(formal_query_entity)

    # Creates the dialog node to ask the user if he/she wants to continue
    # It uses the condition @ServiceFeedBackEntity to react to user answering to feedback question
    formal_query_node = StandardDialogNode(get_node_id(), header.formal_offering_message,
                                           f"@{service_feedback_entity.entity}")
    formal_query_node.parent = service_feedback_node.dialog_node
    formal_query_node.add_response_options(header.formal_offering_message, [
        OptionResponse("Menu", "Menu"),
        OptionResponse("No, thank you..", "Finish")
    ])
    result.dialog_nodes.append(formal_query_node)

    # Creates the dialog node to display a final message when the user has selected to finish the conversation
    # It uses the condition @FormalQueryEntity:Finish to react to user answering to Finish the chat session.
    finish_node = StandardDialogNode(get_node_id(), "Finish", f"@{formal_query_entity.entity}:Finish")
    finish_node.parent = formal_query_node.dialog_node
    finish_node.add_response_paragraph(header.final_message)
    result.dialog_nodes.append(finish_node)

    # Returns the node for the feedback, and the last node that was created
    return service_feedback_node.dialog_node, service_feedback_node.dialog_node


# This function adds the Dialog node that IBM uses when it does not understand user input
def add_not_understanding_dialog(result: Skill, previous_sibling_id: str):
    # 'anything_else' is a default condition for IBM Watson when input is not understandable.
    not_understanding_node = StandardDialogNode(get_node_id(), "Not understanding", "anything_else")
    not_understanding_node.add_response_paragraphs([
        "I haven't understood, Please re-phrase the query.",
        "Can you use other words? I didn't got what you said",
        "Cannot understand the meaning"
    ])
    not_understanding_node.previous_sibling = previous_sibling_id
    result.dialog_nodes.append(not_understanding_node)


# This function adds the Folder Dialog node that we use to store the menu items, to logically group them.
def add_menu_folder(result: Skill, previous_sibling_id: str):
    new_folder_node = FolderDialogNode(get_node_id(), "Folder for menu dialog nodes")
    new_folder_node.previous_sibling = previous_sibling_id
    result.dialog_nodes.append(new_folder_node)
    return new_folder_node.dialog_node, new_folder_node.dialog_node


# This function creates the Main Menu intention, dialog node and entity. Finally returns the node and the
# corresponding entity, to be complemented by posterior processing steps.
def add_main_menu(result: Skill, previous_sibling_id: str, header: ExcelHeader) -> (str, DialogNode, Entity):
    main_menu_intention = Intent(get_menu_intent_id(), "Intention to view the main menu", [
        "Menu",
        "What can you do?",
        "How can you help me?"
    ])
    result.intents.append(main_menu_intention)

    # Creates the dialog node, to respond to the main menu intention we have just created
    main_menu_node = StandardDialogNode(get_node_id(), "Main Menu", f"#{main_menu_intention.intent}")
    main_menu_node.previous_sibling = previous_sibling_id
    # It creates the response of type options, but with no actual options, those will be created after during
    # the question list processing
    main_menu_node.add_response_options(header.selection_message, [])
    result.dialog_nodes.append(main_menu_node)

    # Creates the main menu options entity. with no actual values. those will be created after during the
    # questions processing
    main_menu_entity = Entity('main_menu_options', [], True)
    result.entities.append(main_menu_entity)

    return main_menu_node.dialog_node, main_menu_node, main_menu_entity


# This class allows to pack multiple options required for processing each level of recursion.
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

    # This method creates a derived context for folder creation tasks.
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

    # This method creates a derived context when the processing has achieved a level with no more sub-categories
    # and needs to start processing the questions in the current level to add them to the skill
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


# This function returns a lambda function (expression) that allows to get the current category value for a given level.
# That means that if level is 1 then it returns the Category1, and so on. When it reaches the maximum level, it returns
# a None value to signal the recursive function to stop processing more levels.
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


# This function receives a list of question rows, and then groups them using the given criteria expression (lambda)
# to build a key for a group of rows.
# Returns a dictionary with keys (from the category values) and the rows related to that category
def get_groups(questions: list[ExcelInput], criteria: Callable[[ExcelInput], str]) -> dict[str, list[ExcelInput]]:
    result = {}
    for question in questions:
        key = criteria(question)
        group_list = result.get(key, [])
        group_list.append(question)
        result[key] = group_list
    return result


# This function returns if the question list contains any question that should be included in the menu.
def has_menu_options(questions: list[ExcelInput]) -> bool:
    for question in questions:
        if not question.Show_in_menu:
            return False
    return True


# This functions create a menu given the menu name and returns the menu node and entity objects
def create_menu(result: Skill, header: ExcelHeader, menu_name: str, menu_intention: str,
                context: ProcessingContext) -> (DialogNode, Entity):
    context.menu_entity.values.append(EntityValue(ENTITY_VALUE_TYPE_SYNONYMS, menu_name, []))
    context.menu_node.add_options_to_last_response(menu_name, header.selection_continuation_message)

    menu_node = StandardDialogNode(get_node_id(), menu_name, f'#{menu_intention}')
    menu_node.parent = context.menu_node.dialog_node
    menu_node.previous_sibling = context.previous_menu_id
    menu_node.add_response_options(header.selection_message, [])
    result.dialog_nodes.append(menu_node)

    menu_entity = Entity(get_menu_id(), [])
    result.entities.append(menu_entity)

    return menu_node, menu_entity


# This function removes empty nodes (like entities without values) and then returns the clean skill
def clean_skill_empty_nodes(result: Skill) -> Skill:
    for entity in result.entities[:]:
        if len(entity.values) == 0:
            result.entities.remove(entity)
    return result


# This function processes one level of question categories, creating the corresponding data structures
# (Nodes, entities, intentions and options)
def process_level(result: Skill, questions: list[ExcelInput], header: ExcelHeader, context: ProcessingContext) -> str:
    global previous_menu_link_id
    # Obtains the criteria to be used to build the menu hierarchy, if there are criteria, then it creates new menu
    # levels, otherwise it proceed to create questions inside the last folder
    criteria = get_grouping_criteria(context.level)
    if criteria:
        # Get the questions grouped by the values in the category column corresponding to the level
        groups = get_groups(questions, criteria)
        for key, group_list in groups.items():
            if key:
                # If the group has a Key it means it is a subcategory and needs to create folder, intention,
                # dialog node and entity
                new_folder_context = context.new_folder_context(key)
                result.dialog_nodes.append(new_folder_context.parent_node)

                menu_intention = Intent(get_menu_intent_id(), key, [key])
                result.intents.append(menu_intention)

                # If required (all the questions appear in the menu), it creates the menu
                if context.menu_node and context.menu_entity and has_menu_options(group_list):
                    new_folder_context.menu_node, new_folder_context.menu_entity = create_menu(result, header, key,
                                                                                               menu_intention.intent,
                                                                                               context)
                    context.previous_menu_id = new_folder_context.menu_node.dialog_node

                link_node = StandardDialogNode(get_node_id(), key, f'#{menu_intention.intent}')
                link_node.parent = new_folder_context.menu_folder_id
                link_node.previous_sibling = previous_menu_link_id
                link_node.next_step = DialogNodeNextStep(new_folder_context.menu_node.dialog_node)
                result.dialog_nodes.append(link_node)
                previous_menu_link_id = link_node.dialog_node

                # It process the next level (using the newly generated context)
                process_level(result, group_list, header, new_folder_context)
                if new_folder_context.parent_node:
                    context.previous_sibling_id = new_folder_context.parent_node.dialog_node
            else:
                # If the group has no key, it means only needs to process the questions. It calls recursively using
                # a new finish context (this finish context uses a level 9999 to signal the next iteration as the
                # last one)
                context.previous_sibling_id = process_level(result, group_list, header, context.new_finish_context())
    else:
        # If there is no grouping criteria (for example when it is called with level = 9999), it creates the
        # questions' objects (entities, dialog nodes, intentions, etc.)
        for question in questions:
            if context.menu_node and context.menu_entity and question.Show_in_menu:
                # If the question should be in the menu, adds the menu option to the current menu node
                context.menu_node.add_options_to_last_response(question.Question, header.selection_continuation_message)

            # Creates the query intent to enable the question to be accessed directly by the user asking the questions
            question_intent = Intent(get_question_intent_id(), question.Question, [question.Question])
            result.intents.append(question_intent)

            # Creates the dialog node for displaying the answer to the question in response to detecting the intention
            answer_node = StandardDialogNode(get_node_id(), question.Question, f'#{question_intent.intent}')
            answer_node.add_response_paragraph(question.Answer)
            if context.parent_node:
                answer_node.parent = context.parent_node.dialog_node
            answer_node.previous_sibling = context.previous_sibling_id
            # Associate the feedback dialog step as next step after answering the question.
            answer_node.next_step = DialogNodeNextStep(context.formal_query_id)
            result.dialog_nodes.append(answer_node)
            context.previous_sibling_id = answer_node.dialog_node

    return context.previous_sibling_id


# This function is responsible for building the skill object containing all the
# elements (intentions, entities, dialog nodes) required to load a valid IBM Watson dialog skill JSON file
def generate_dialog_skill(questions: list[ExcelInput], header: ExcelHeader) -> Skill:
    # Creates an empty skill to be completed and returned
    result = Skill(header.name, header.description, 'en')
    # Adds the common elements to the skill
    previous_sibling_id, formal_query_id = add_initial_dialog(result, header)
    previous_sibling_id, menu_folder_id = add_menu_folder(result, previous_sibling_id)
    previous_sibling_id, main_menu_node, main_menu_entity = add_main_menu(result, previous_sibling_id, header)
    # Creates a context object used to keep the values for the current processing step, it starts on level 1 with
    # references to existing common nodes.
    initial_context = ProcessingContext(
        # Starts with the first Category level
        level=1,
        # Provides that for fist level, there is no parent node
        parent_node=None,
        # Provides relation with the previous dialog node, to start adding nodes after that node
        previous_sibling_id=previous_sibling_id,
        # Provides reference to the Menu dialog Node, to allow adding options to it
        menu_node=main_menu_node,
        # Provides reference to the Menu entity, to allow adding option values to it
        menu_entity=main_menu_entity,
        # Provides reference to the formal query Node for feedback, this node is used after answering any question
        formal_query_id=formal_query_id,
        # Provides reference to the menu folder where the nodes will be created (for logical grouping)
        menu_folder_id=menu_folder_id,
        # References the previous menu node that was created, we start with none for the first menu node.
        previous_menu_id=None
    )
    # Start processing the questions dataset recursively, starting with the whole set of questions and the first
    # category level.
    previous_sibling_id = process_level(result, questions, header, initial_context)
    # Add the final dialog element for unexpected answers
    add_not_understanding_dialog(result, previous_sibling_id)
    # Cleans empty entities and return the result
    return clean_skill_empty_nodes(result)
