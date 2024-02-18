import requests


class PotterDB:
    def __init__(self, version="v1",) -> None:
        self.url = f"https://api.potterdb.com/{version}"
