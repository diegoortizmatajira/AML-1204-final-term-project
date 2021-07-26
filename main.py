# This is the main application
from dialog_processor import generate_dialog_skill
from excel_loading import load_excel_file
from json_writing import write_json_skill

input_data, header_data = load_excel_file('PlantillaQA.xlsx')
skill_object = generate_dialog_skill(input_data, header_data)
write_json_skill(skill_object, 'output.json')
