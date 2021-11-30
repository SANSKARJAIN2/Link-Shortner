from flask import request, redirect
import flask
from controllers.redirect_class import RedirectClass

from controllers.shorten_class import ShortenLinks
from exceptions.custom_exceptions import UnshortenLinkNF, InvalidLink, CustomException, shortLinkRedirectionError
import json
from urllib.parse import urlparse

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
    rc = RedirectClass(short_id)
    try:
        link = rc.getredicrectingLink()
        return flask.redirect(link)
    except shortLinkRedirectionError as e:
        return returnObj(e.value,e.message).returnObj()
    except Exception as e:
        print(e.__str__())
        return returnObj(1000,"something went wrong, while redirecting").returnObj()