from odmantic import Model


class BookModel(Model):
    keyword: str
    publisher: str
    price: str
    image: str

    class Config:
        collection = "books"
