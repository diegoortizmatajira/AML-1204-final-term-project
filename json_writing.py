import json
from json_structure.skill import Skill

def write_json_skill(skill: Skill, output_file: str):
    #print(f'Saving skill to {output_file}')
    #print(skill)

    with open(output_file, "w", encoding="utf-8") as writeJsonfile:
        json.dump(skill, writeJsonfile, indent=4, default=str)
