from config import app
from routes.ls_bp import ls_bp
dev = True

# Setting up local dev environment
if dev:
    app.debug = True
else:
    app.debug = False
app.config.from_object('config')
app.register_blueprint(ls_bp, url_prefix="/")

@app.route('/')
def index():
    return "Running"

if __name__ == '__main__':
    app.run()
    