class SystemSettings:
    def __init__(self):
        self.off_topic = {
            "enabled": True
        }

        self.disambiguation = {
                                  "prompt": "Did you mean:",
                                  "enabled": True,
                                  "randomize": True,
                                  "max_suggestions": 5,
                                  "suggestion_text_policy": "title",
                                  "none_of_the_above_prompt": "None of the above"
                              },
        self.intent_classification = {
                                         "training_backend_version": "v2"
                                     },

        self.spelling_auto_correct = True
