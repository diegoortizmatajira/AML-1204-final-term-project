# This is the main application
from excel_loading import load_excel_file
from processor import generate_skill
from json_writing import write_json_skill

input_data = load_excel_file('file.xlsx')
skill_object = generate_skill(input_data)
write_json_skill(skill_object, 'output.json')