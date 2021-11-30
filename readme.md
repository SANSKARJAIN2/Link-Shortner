This repository is for a link shortening api which allows you to shorten a link and redirect the shortened link to the original link.

HOW TO USE:
Step 0: Install the dependencies
to install, use command ```python -m pip install -r requirements.txt```

Step 1: Install and run redis on local system.
once redis is installed, open terminal and type ``` redis-server```

Step 2: If redis is on a different host or port than paste the your host and post in ```config.py``` file
Default Dev host: "localhost"
Default Dev port: 6379

Step 3: run the server through command : ```python app.py``` & now you can send request to the api
Step 4: Either use post man or use ```server interactions.py``` file to shorten link 
    **Through server interactions file:**
    run ```python server_interaction.py``` in the terminal, then paste the host, after that u can paste the link you want to shorten
    **For postman**
    paste the ```host_url/shorten``` then, go to the body tab and select `raw` and use the body template below:
    {
        "link":you_link_here
    }
    and send a **GET** request, alternatively you can *browser* too
Step 5 for redirecting/ unshortening the link,
simply paste the short link in browser or postman and you will be redirected to the original link

**DETAILS ABOUT THE ROUTES**

HOW IT WORKS:
    ROUTES:
    1. '/' : to check if api is up or not
    2. '/shorten': this route will shorten the gievn url and provide the new short url in return
    3. '/<code>' this route will redirect the short url to original url

HOW ROUTE WORK:
    1. '/shorten': [method = GET]
    Aim: to shorten the given api and provide the new short url in return
    ***How to use:***
    call the '/shorten' route, with **raw json in body**
    json body:
    {
        "link": link_to_shorten
    }
    ***Return***
    as return the user will recieve a json or the following type:
        {
            "status_code": x where x belongs to [200,1000,1001,1002,1003,1004]
            "message" : "shortened link"
        }
        *in case of error, the status code will be between [1000,1004] and the message will be a discription of what went wrong.*
    2. '/<code>' [method = GET]
    Aim: Redirect the short url to the original url
    ***how to use*** 
    nothing special need to be done, just paste the shorturl in browser or postman and api will redirect to respective url
    ***return***
    as return, the api should redirect you to the respective url,but
    in case of invalid url, or error, the api will return a json object
    format of json object
        {
            "status_code": x where x belongs to [1000,1001,1002,1003,1004]
            "message" : description of the error
        
        }