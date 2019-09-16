import json


class Response:
    def __init__(self):
        self.analysis_id = ""
        self.state = ""
        self.company_id = ''
        self.error = ""

    def getMap(self):
        custom_map = {"analysis_id": self.analysis_id, "company_id": self.company_id, "state": self.state,
                     "error": self.error}
        # return json.dumps(custom_map)
        return custom_map