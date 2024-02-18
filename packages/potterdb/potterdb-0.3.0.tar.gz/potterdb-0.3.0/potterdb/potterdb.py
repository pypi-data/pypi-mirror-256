import requests


class PotterDB:
    def __init__(
        self,
        version="v1",
    ) -> None:
        self.url = f"https://api.potterdb.com/{version}"

    def getbooks(self):
        resp = requests.get(f"{self.url}/books").json()
        length_data = len(resp["data"])
        print()
        data = []
        for book in range(0, length_data):
            title = resp["data"][book]["attributes"]["title"]
            author = resp["data"][book]["attributes"]["author"]
            cover = resp["data"][book]["attributes"]["cover"]
            data.append([[title], [author], [cover]])
        return data

    def getbooksbyid(self):
        pass


# if __name__ == "__main__":
#    obj = PotterDB()
#    data = obj.getbooks()
#    for book in data:
#        print(book)
