import redis
from exceptions.custom_exceptions import UnshortenLinkNF
class Redis_Service():
    linkToShortDb = redis.Redis()
    shortToLinkDb = redis.Redis()
    def set(self,key = "", value = ""):
        try:
            self.linkToShortDb.set(key, value)
            self.shortToLinkDb.set(value, key)
            return True
        except Exception as e:
            print(e)
            return False
    def isShortened(self,link):
        return self.linkToShortDb.exists(link)
    def canBeRedirected(self,code):
        return self.shortToLinkDb.exists(code)
    def getUnshortenLink(self,code):
        if(self.canBeRedirected(code)):
            return self.shortToLinkDb.get(code).decode()
        else:
            raise UnshortenLinkNF()
    def getShortenedLink(self,link):
        return self.linkToShortDb.get(link).decode()
    def __init__(self,host,port):
        self.linkToShortDb = redis.Redis(host,port,db = 1)
        self.shortToLinkDb = redis.Redis(host,port,db = 2)