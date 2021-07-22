import json

from excel_loading import ExcelHeader
from processor import generate_skill

skill_object = generate_skill([], ExcelHeader())
print(json.dumps(skill_object, default=lambda o: o.__dict__, indent=4))
