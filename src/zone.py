class Zone:
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.name = data.get("name")
        self.records = {}