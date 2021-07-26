import json

from dialog_skill.skill import Skill


def write_json_skill(skill: Skill, output_file: str):
    with open(output_file, "w", encoding="utf-8") as writeJsonfile:
        # json.dump(skill, writeJsonfile, default=lambda o: o.__dict__, indent=4)
        json.dump(skill, writeJsonfile,
                  default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value is not None),
                  indent=2)
