class UnshortenLinkNF(Exception):
    def __init__(self):
        message = "Short link not found in DataBase"
        super().__init__(message)