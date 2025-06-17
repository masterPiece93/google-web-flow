from flask import (
    Flask,
    render_template,
    session
)

def create_app(config_fileref):

    app = Flask(__name__)
    app.config.from_object(config_fileref)

    @app.route("/")
    def index():
        if "id_info" in session:
            picture: str= session["id_info"]["picture"]
            email: str = session["id_info"]["email"]
            is_logged_in: bool = True
            return render_template("index.html", is_logged_in=is_logged_in, picture=picture, email=email)
        return render_template("index.html")


    return app
