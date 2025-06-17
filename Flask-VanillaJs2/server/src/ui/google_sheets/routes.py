from flask import ( 
    Blueprint, 
    render_template, 
    session, 
    redirect, 
    current_app, 
    jsonify,
    url_for
)
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError

import src.ui.google_sheets.utils as google_sheet_utils
from pprint import pprint
google_sheets_ui_bp = Blueprint('google-sheets', __name__, template_folder='templates')

SAMPLE_SPREADSHEET_ID = "1XZ9QFJKZKit6O1rWYcpMdpNLXgAO7mn_vnAGrRGR7qQ"
SAMPLE_RANGE_NAME = "Sheet1!A2:B3"

__title__ = "Google Sheets Demonstrations"

@google_sheets_ui_bp.route('/')
def index():
    return render_template('google_sheets/landing.page.html', title=__title__)

@google_sheets_ui_bp.route('/list-all-sheets-data')
def all_sheets_data_api_request():
    
    credentials_session_key = current_app.config["CREDENTIALS_SESSION_KEY"]

    if credentials_session_key.value not in session:
        session['final_redirect'] = url_for('ssr_ui.google-sheets.all_sheets_data_api_request')
        return redirect(url_for('auth.login'))

    # Load credentials from the session.
    credentials = Credentials(
        **session[credentials_session_key.value])

    if not credentials.valid:
        session['final_redirect'] = url_for('ssr_ui.google-sheets.all_sheets_data_api_request')
        return redirect(url_for('auth.login'))
    
    service = build("sheets", "v4", credentials=credentials)

    try:
      # Call the Sheets API
      sheet = service.spreadsheets()
      data: list = google_sheet_utils.get_all_sheets_data(sheet, SAMPLE_SPREADSHEET_ID, without_headers=False)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
    except RefreshError:
        session['final_redirect'] = url_for('ssr_ui.google-sheets.all_sheets_data_api_request')
        return redirect(url_for('auth.login'))
    
    return render_template("google_sheets/all_gsheet_data.page.html", data=data, title=__title__)
