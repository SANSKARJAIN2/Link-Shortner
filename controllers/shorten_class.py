from uuid import UUID, uuid4
from config import rs
from service.redis_service import Redis_Service
from exceptions.custom_exceptions import InvalidLink,RedisSetError
class ShortenLinks():
    __link: str
    def __init__(self,url:str):
        self.__link = url
    def isValidLink(self):
        # a valid url should not cotain a blank space and should not be empty and should contain atleast '.' which is not at the last index
        # any sort of url is valid, unless we ar looking for a specific protcal, domain or some other parameters
        # then we could narrow down, other than that it's just a space that should not be present in a url
        if(self.__link.__len__()==0):
            return False
        if(self.__link.find(' ')!=-1):
            return False
        n = len(self.__link)
        pos = self.__link.rfind('.')
        if(pos==0 or (pos==n-1) or pos==-1):
            return False
        return True
    #function to create a unique id that will be the identifier for the link and will also be the extention for the short link
    def __createuniqueId(self):
        return str(uuid4())
    def shorten(self):
        if(self.isValidLink()==False):
            raise InvalidLink()
        # checking if the link is already shortened before
        if(rs.isShortened(self.__link)):
            return rs.getShortenedLink(self.__link)
        shortLink = self.__createuniqueId()
        if rs.set(self.__link,shortLink)==False:
            raise RedisSetError()
        else:
            return shortLink


