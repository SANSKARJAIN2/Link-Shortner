from config import rs
from exceptions.custom_exceptions import shortLinkRedirectionError
from urllib.parse import urlparse
class RedirectClass:
    __code:str
    def __init__(self, code):
        self.__code = code
    def sanitize(self,link):
        urlObj = urlparse(link)
        if(urlObj.scheme == ""):
            link =  "https://"+link
            urlObj = urlparse(link)
        return urlObj.geturl()
    def getredicrectingLink(self):
        # print(f"{self.__code} present  "+ str(rs.canBeRedirected(self.__code)))
        # print()
        if rs.canBeRedirected(self.__code)>0:
            link = rs.getUnshortenLink(self.__code)
            link = self.sanitize(link)
            return link
        else:
            raise shortLinkRedirectionError()
