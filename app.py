from config import app
from routes.ls_bp import ls_bp
from flask import request
dev = True

# Setting up local dev environment
if dev:
    app.debug = True
else:
    app.debug = False
app.config.from_object('config')
app.register_blueprint(ls_bp, url_prefix="/")

# this route won't do anything as this route is defined in the controller
@app.route('/')
def index():
    return "Running"

if __name__ == '__main__':
    app.run()
    