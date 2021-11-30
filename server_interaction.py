import requests as https
import json
print("Welcome to the server interaction file,")
print("if you want to exit, press q at anypoint of time")
prefix = input("please enter the host url")
while True:
    link = str(input("please enter the link to short\n"))
    if(link=="q"):
        exit(0)
    body = json.dumps({"link":link})
    
    
    rv = https.get(prefix+'/shorten',data=body)
    print(rv._content.decode())