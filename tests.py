from logging import exception
import app
import unittest
import tempfile
from service.redis_service import Redis_Service
from random import randint
from uuid import UUID, uuid4
from exceptions import custom_exceptions
import json
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
    shortLinks = []
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
        rs = Redis_Service()
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

    def test_03_shortenInvalidLink(self):
        for link in self.invalidLinks:
            rv = self.sendShortenRequest(link)
            rvData = json.loads(rv.get_data().decode())
            self.assertTrue(rv.status_code == 200)
            self.assertTrue(rvData['status_code']>=1000)

    def requestRedirection(self,id):
        return self.app.get('/'+id)
    def redirect(self):
        for link in self.shortLinks:
            id = link.rindex('/')
            id = link[id+1:]
            self.requestRedirection(id)
        for i in range(1,10):
            id = UUID.uuid4()
            self.requestRedirection(id)
    def shortenSameLink(self):
        for link,sl in self.Validlinks,self.shortLinks:
            self.sendShortenRequest(link)

if __name__=='__main__':
    unittest.main()
# from service.redis_service import Redis_Service

# r = Redis_Service()
# r.set("test","short")
# print(r.getUnshortenLink("short"))
# print(r.isShortened("test"))