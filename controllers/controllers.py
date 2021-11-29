from flask import request

from controllers.shorten_class import ShortenLinks
from exceptions.custom_exceptions import UnshortenLinkNF, InvalidLink, CustomException
import json

class returnObj:
    status_code:int
    message:str
    def __init__(self,code,message):
        self.status_code = code
        self.message = message
    def returnObj(self):
        return json.dumps({"status_code":self.status_code,
        "message":self.message})


def index():
    return "home page"

def shorten():
    link = json.loads(request.get_data())
    link = link['link']
    shortenLinkObj = ShortenLinks(link)
    try: 
        
        return returnObj(200,(request.base_url[:request.base_url.rfind('/')]+'/' +  shortenLinkObj.shorten())).returnObj()
    except UnshortenLinkNF as e:
        return returnObj(e.value,e.message).returnObj()
    except InvalidLink as e:
        return returnObj(e.value,e.message).returnObj()
    except Exception as e :
        return returnObj(1000,"something went wrong").returnObj()

def redirect(short_id = ""):
    return short_id