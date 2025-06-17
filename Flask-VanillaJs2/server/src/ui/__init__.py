from typing import Final
from flask import Blueprint, render_template
from src.ui.google_sheets.routes import google_sheets_ui_bp

ssr_ui_bp = Blueprint('ssr_ui', __name__, template_folder='templates')

registered_demos: Final[tuple] = tuple()

@ssr_ui_bp.route('/')
def index():
    return render_template('index.html', title="Demonstration Catalog", registered_demos=registered_demos)

ssr_ui_bp.register_blueprint(google_sheets_ui_bp, url_prefix="/google-sheets")
registered_demos += ('/google-sheets',)
