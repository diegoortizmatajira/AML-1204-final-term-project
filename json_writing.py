import json
from json_structure.skill import Skill


def write_json_skill(skill: Skill, output_file: str):
    with open(output_file, "w", encoding="utf-8") as writeJsonfile:
        json.dump(skill, writeJsonfile, default=lambda o: o.__dict__, indent=4)
