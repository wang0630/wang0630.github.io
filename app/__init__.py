from flask import Flask
from flask_login import LoginManager
from .config import Config
# from flask_assets import Environment,Bundle

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)

# flask_loging setup
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

from .main import main
from .auth import auth
# register blueprint
app.register_blueprint(main)
app.register_blueprint(auth)

from . import assets