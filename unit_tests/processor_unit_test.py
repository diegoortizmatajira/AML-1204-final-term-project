import json

from excel_loading import ExcelHeader
from processor import generate_skill

skill_object = generate_skill([], ExcelHeader())
print(json.dumps(skill_object,
                 default=lambda o: dict((key, value) for key, value in o.__dict__.items() if value),
                 indent=4))
