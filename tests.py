from logging import exception
import app
import unittest
import tempfile
from service.redis_service import Redis_Service
from random import randint
from uuid import UUID, uuid4
from exceptions import custom_exceptions
import json
from config import host,port
from urllib.parse import urlparse
class LinkShortenTest(unittest.TestCase):
    Validlinks = ["https://www.w3schools.com/action_page.php?page=1&category=Mobiles%20&%20Accessories",
                    "https://atcoder.jp/contests/abc229/tasks/abc229_e",
                    "https://codeforces.com/contest/1614/problem/C",
                    "https://www.linkedin.com/feed/",
                    "https://www.codechef.com/",
                    "http://codinggame.com/",
                    "https://www.youtube.com/watch?v=TUVcZfQe-Kw",
                    "yelp.com/search?cflt=locksmiths&find_loc=San+Francisco%2C+CA"
                    "yelp.com/",
                    "indiegogo.com"
                    ]
    invalidLinks = []
    shortLinks = {}
    def __createInvalidLink(self,url :str):
        n = len(url)
        if(randint(0,1)):
            pos = randint(0,n-2)
            url = url[:pos] +" "+url[pos+1:]
            return url
        else:
            if(randint(0,1)):
                url = url.replace('.','r',-1)
                return url
            else:
                if url.find('.')==-1:
                    url = "." + url
                    return url
                else:
                    pos = url.rfind('.')-1
                    url = url[:pos-1] + ' ' + url[pos:]
                return url
    def setUp(self):
        self.app = app.app.test_client()
        for link in self.Validlinks:
            url = self.__createInvalidLink(link)
            self.invalidLinks.append(url)
# Redis Check: Basic tests to check if redis is functional
# or not and the set, get, canbeRedisrected, isShortened function are working properly or not
    def test_01_redisCheck(self):
        rs = Redis_Service(host,port)
        key = self.Validlinks[0]
        value = str(uuid4())
        self.assertTrue(rs.set(key, value))
        # checking an already shortened link. Expected to return true
        self.assertTrue(rs.isShortened(key))
        # checking if a shortened link can be redirected or not i.e the link is in redis db or not
        # expected to return true
        self.assertTrue(rs.canBeRedirected(value))
        # getting a unshortened link, expected value should be same as key variable
        self.assertTrue(rs.getUnshortenLink(value)==key)
        
        link = self.Validlinks[1]
        value = str(uuid4())
        # checking if a new link is already shortened or not, expected to return false
        self.assertFalse(rs.isShortened(value))
        # checking if a new link can be redirected or not, expected to return false
        self.assertFalse(rs.canBeRedirected(value))
        # checking if a new link is already shortened or not, expected to raise UnshortenLinkNF()
        try:
            rs.getUnshortenLink(value)
        except custom_exceptions.UnshortenLinkNF:
            self.assertTrue(True)
        except Exception as e:
            self.assertTrue(False)
            

    def sendShortenRequest(self,link):
        PARAM = json.dumps( {"link":link})
        return self.app.get('/shorten',data=PARAM)
    # sending request to shorten for all valid link, expected status code 200,data = {status_code:200,message: shortened link}
    def test_02_shortenValidLink(self):
        for link in self.Validlinks:
            rv = self.sendShortenRequest(link)
            self.assertTrue(rv.status_code == 200)
            rvData = json.loads(rv.get_data())
            self.assertTrue(rvData['status_code'] ==200)
            # d = dict(link,rvData['message'])
            self.shortLinks.update({link : rvData['message']})

# calling api for all invalid link, expectid behavious, status code 200, body:{status_code:>=1000, message: an error message}
    def test_03_shortenInvalidLink(self):
        for link in self.invalidLinks:
            rv = self.sendShortenRequest(link)
            rvData = json.loads(rv.get_data().decode())
            self.assertTrue(rv.status_code == 200)
            self.assertTrue(rvData['status_code']>=1000)
# Testing redirection
# simple function to send request for redirection, follow_redirects are False in order to check if the link is redirected or not
    def requestRedirection(self,link):
        return self.app.get(link,follow_redirects=False)
#function to include a scheme to the link, in case it is not present
# using urlparse lib to sheck if link is associated or not, if not then associating https to the link
    def sanitize(self,link):
        urlObj = urlparse(link)
        if(urlObj.scheme == ""):
            link =  "https://"+link
            urlObj = urlparse(link)
        return urlObj.geturl()
# checking if a valid shortened link is redirected or not
# link fed are those which are already shortened (when test for shortening valid link was run, we stored the response)
# expected status code 302, link should be same as the link that was shortened when tests were run for valid link shortening
    def test_04_valid_redirect(self):
        for link,short in self.shortLinks.items():
            rv = self.requestRedirection(short)
            link = self.sanitize(link)
            self.assertTrue(rv.status_code==302)
            self.assertTrue(rv.location == link)
# checking if an invalid shortened link is redirected or not
# randomly creating new ids and converting them into link so that they hit the respective route
# expected status code 200, data should consist of {"status_code": 1004, "message": "short link not found in database"}
    def test_05_invalid_redirect(self):
        self.assertTrue(len(self.shortLinks)>0)
        prefix = list(self.shortLinks.values())[0]
        pos = prefix.rfind('/')
        prefix = prefix[:pos]+'/'
        for i in range(1,10):
            id = str(uuid4())
            rv = self.requestRedirection(prefix+id)
            self.assertTrue(rv.status_code == 200)
            rvData = json.loads(rv.get_data().decode())
            self.assertTrue(rvData['status_code'] ==1004)

if __name__=='__main__':
    unittest.main()