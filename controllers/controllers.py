from flask import request, redirect
import flask
from controllers.redirect_class import RedirectClass

from controllers.shorten_class import ShortenLinks
from exceptions.custom_exceptions import UnshortenLinkNF, InvalidLink, CustomException, shortLinkRedirectionError
import json

# class to maintain the return obj and convert the data into json that should be returned
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
# requests for shortening URL will go here
# parameters will be taken from body and should be in json format: {"link": url_that_needs_to_be_shortened}
def shorten():
    link = json.loads(request.get_data())
    link = link['link']
    shortenLinkObj = ShortenLinks(link)
    try: 
        # incase of the invalid Url or some unexpecteds error, return object will send custom error codes 
        # and the application will not break
        return returnObj(200,(request.base_url[:request.base_url.rfind('/')]+'/' +  shortenLinkObj.shorten())).returnObj()
    except UnshortenLinkNF as e:
        return returnObj(e.value,e.message).returnObj()
    except InvalidLink as e:
        return returnObj(e.value,e.message).returnObj()
    except Exception as e :
        return returnObj(1000,"something went wrong").returnObj()
# redirecting request will go here, i.e short url will be routed here
# so that they can be redirected to the original url
def redirect(short_id = ""):
    rc = RedirectClass(short_id)
    try:
        # in case of invalid link or error return obj well send custom error code 
        # and application will not break
        link = rc.getredicrectingLink()
        return flask.redirect(link)
    except shortLinkRedirectionError as e:
        return returnObj(e.value,e.message).returnObj()
    except Exception as e:
        print(e.__str__())
        return returnObj(1000,"something went wrong, while redirecting").returnObj()