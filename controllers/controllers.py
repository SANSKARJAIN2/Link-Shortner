from flask import request

def index():
    return "home page"

def shorten():
    return "shortening"

def redirect(short_id = ""):
    return short_id