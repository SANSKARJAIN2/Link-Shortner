import redis
from exceptions.custom_exceptions import UnshortenLinkNF
from config import host, port
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
    def canBeRedirected(self,link):
        return self.shortToLinkDb.exists(link)
    def getUnshortenLink(self,link):
        if(self.canBeRedirected(link)):
            return self.shortToLinkDb.get(link).decode()
        else:
            #TODO: add exception here
            raise UnshortenLinkNF()
    def getShortenedLink(self,link):
        return self.linkToShortDb.get(link).decode()
    def __init__(self):
        self.linkToShortDb = redis.Redis(host,port,db = 1)
        self.shortToLinkDb = redis.Redis(host,port,db = 2)