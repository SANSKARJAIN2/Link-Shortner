import os
from flask import Flask
from service.redis_service import Redis_Service
app = Flask(__name__)
dev = True
host = ""
port = 0000
if dev:
    host = "localhost"
    port = 6379
rs = Redis_Service(host,port)