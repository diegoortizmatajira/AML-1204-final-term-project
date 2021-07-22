import uuid
from datetime import datetime, timezone

from json_structure.workspace import Workspace


class DialogSettings:
    def __init__(self):
        self.actions: bool = True


class Skill:

    def __init__(self, name, description):
        utc_dt = datetime.now().astimezone(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        self.type: str = 'dialog'
        self.status: str = 'Available'
        self.name: str = name
        self.created: str = utc_dt
        self.updated: str = utc_dt
        self.language: str = 'en'
        self.skill_id: str = str(uuid.uuid4())
        self.workspace: Workspace = Workspace()
        self.description: str = description
        self.workspace_id: str = str(uuid.uuid4())
        self.dialog_settings: DialogSettings = DialogSettings()
