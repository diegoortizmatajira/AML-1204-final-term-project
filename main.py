# This is the main application
from dialog_processor import generate_dialog_skill
from excel_loading import load_excel_file
from json_writing import write_json_skill
import sys

# Reads files from the command line
input_file = (sys.argv[1] if len(sys.argv) >= 2 else None) or 'PlantillaQA.xlsx'
output_file = (sys.argv[2] if len(sys.argv) >= 3 else None) or 'output.json'

# Displays usage info
print('Dialog generator - Tool to transform an Excel file to a IBM Watson Assistant dialog skill')
print(f'Usage: python .\\main.py [input file] [output file]\n')
# Reads the input file
print(f' - Processing input file: {input_file}')
input_data, header_data = load_excel_file(input_file)
# Processes the questions read from the input file
print(f' - Processing {len(input_data)} questions to generate dialog skill')
skill_object = generate_dialog_skill(input_data, header_data)
# Write the resulting skill to the output file
print(f' - Generating output file: {output_file}')
write_json_skill(skill_object, output_file)
print('\nProcess complete')
