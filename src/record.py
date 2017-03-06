from src.zone import Zone


class Record:
    def __init__(self, data: dict, zone: Zone):
        self.id = data.get("id")
        self.type = data.get("type")
        self.name = data.get("name")
        self.content = data.get("content")
        self.proxied = data.get("proxied")
        self.ttl = data.get("ttl")
        self.zone = zone

