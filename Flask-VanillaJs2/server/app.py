import os, logging, sys
import redis
import exceptions as AppCustomExceptions
import utilities
from flask import Flask, render_template
from flask_session import Session
from src.generic_routes import generic_bp
from src.api.auth_routes import auth_bp
from src.ui import ssr_ui_bp
from typing import Final

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from commandline import parser

# including the external `client` folder so as to import `create_app` from client :
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from client.app import create_app
# from client.config import Config

# logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Line 16 debuger is working")


# app
app = Flask(__name__)
app.config.from_object('setup.config.Config')

# credentials key value
app.config["CREDENTIALS_SESSION_KEY"] = utilities.CredentialsKey()

# redis configuration
redis_connection = redis.from_url(app.config["REDIS_CONN_STRING"])
utilities.check_redis_connection(
    redis_connection, 
    on_exception_raise=AppCustomExceptions.RedisConnectionFailed,
    logger=logger
)
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis_connection
Session(app)

# Route Registration
app.register_blueprint(generic_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(ssr_ui_bp, url_prefix="/ssr-ui")

args = parser.parse_args()

if __name__ == '__main__':

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    if app.config.get("DEBUG"):
        # * Since Oauth consent screen is set for `localhost`, hence
        #   we must access the endpoints on browser using `http://localhost:<port>/...`
        logging.info(f"'\033[94m' Please access the project on \033[1m http://localhost:{app.config['PORT']}/ '\033[0m'")
    
    execution_type: str = args.execute

    if execution_type == "isolated":
        app.run(
            host=app.config["HOST"],
            port=app.config["PORT"],
            debug=app.config.get("DEBUG", False)
        )
    if execution_type == "combined":
        ui_app = create_app("client.config.Config")
        application = DispatcherMiddleware(app, {
            '/ui': ui_app
        })
        if app.config.get("DEBUG", False):
            @app.route("/")
            def root():
                return render_template('help.html')
        ui_app.config['SESSION_TYPE'] = 'redis'
        ui_app.config['SESSION_REDIS'] = redis_connection # NOTE : same redis conn : Required for Session Sharing
        ui_app.config['SECRET_KEY'] = app.config['SECRET_KEY'] # NOTE : same secret : Required for Session Sharing
        Session(ui_app)

        from werkzeug.serving import run_simple
        application.debug=app.config.get("DEBUG", False)
        run_simple(app.config["HOST"], app.config["PORT"], application, use_reloader=application.debug)
