from json_structure.step_output import StepOutput


class StepResolver:
    def __init__(self):
        self.type: str = None


class Step:
    def __init__(self, step):
        self.step: str = step
        self.output: StepOutput = StepOutput()
        self.handlers = []
        self.resolver: StepResolver = StepResolver()
        self.variable: str = step
        self.question = None

    def add_default_option_settings(self, entity: str):
        not_found = {
            "type": "not_found",
            "title": "validation_not_found_handler",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "I didn't catch that. Select a valid option:"
                            }
                        ],
                        "response_type": "text"
                    }
                ]
            },
            "handler": "validation_not_found_handler",
            "resolver": {
                "type": "prompt_again"
            },
            "next_handler": "validation_not_found_max_tries_handler"
        }
        max_tries = {
            "type": "not_found_max_tries",
            "title": "validation_not_found_max_tries_handler",
            "output": {
                "generic": [
                    {
                        "values": [
                            {
                                "text": "I'm afraid I don't understand. Let me see if I can help another way."
                            }
                        ],
                        "response_type": "text"
                    }
                ]
            },
            "handler": "validation_not_found_max_tries_handler",
            "resolver": {
                "type": "end_action"
            }
        }
        self.handlers = [not_found, max_tries]
        self.question = {
            "entity": entity,
            "max_tries": 3,
            "only_populate_when_prompted": False
        }
