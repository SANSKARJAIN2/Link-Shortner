class CustomException(Exception):
    
    pass
class UnshortenLinkNF(Exception):
    def __init__(self):
        self.message = "Short link not found in DataBase"
        self.value = 1001
    def __str__(self):
        return self.customMessage

class InvalidLink(Exception):
    def __init__(self):
        self.message = "Invalid link, please provide a valid link"
        self.value = 1002
    def __str__(self):
        return self.customMessage
class RedisSetError(Exception):

    def __init__(self,m=""):
        self.message = "unable to save link in redis db"
        self.value = 1003
    def __str__(self):
        return self.customMessage