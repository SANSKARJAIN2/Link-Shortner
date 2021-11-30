from config import rs
from exceptions.custom_exceptions import shortLinkRedirectionError
from urllib.parse import urlparse
class RedirectClass:
    __code:str
    def __init__(self, code):
        self.__code = code
#function to include a scheme to the link, in case it is not present
# using urlparse lib to sheck if link is associated or not, if not then associating https to the link
    def sanitize(self,link):
        urlObj = urlparse(link)
        if(urlObj.scheme == ""):
            link =  "https://"+link
            urlObj = urlparse(link)
        return urlObj.geturl()
    def getredicrectingLink(self):
        if rs.canBeRedirected(self.__code)>0:
            link = rs.getUnshortenLink(self.__code)
            link = self.sanitize(link)
            return link
        else:
            raise shortLinkRedirectionError()
