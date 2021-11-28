from logging import exception
import app
import unittest
import tempfile
from service.redis_service import Redis_Service
from random import randint
from uuid import UUID, uuid4
from exceptions import custom_exceptions
class LinkShortenTest(unittest.TestCase):
    Validlinks = ["https://www.google.com/search?q=generate+random+valid+url+python&oq=generate+randon+valid+urls+&aqs=chrome.2.69i59j33i22i29i30l9.6571j0j4&sourceid=chrome&ie=UTF-8",
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
            pos = randint(0,n-1)
            url = url[:pos] +" "+url[pos+1:]
            return url
        else:
            if(randint(0,1)):
                url.replace('.','',1)
                return url
            else:
                pos = url.rindex('/')-1
                url = url[:pos-1] + '?' + url[pos:]
                return pos
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
            


if __name__=='__main__':
    unittest.main()
# from service.redis_service import Redis_Service

# r = Redis_Service()
# r.set("test","short")
# print(r.getUnshortenLink("short"))
# print(r.isShortened("test"))