import os
from flask import Flask
app = Flask(__name__)
dev = True
host = ""
port = 0000
if dev:
    host = "localhost"
    port = 6379
