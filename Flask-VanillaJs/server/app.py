import os
import logging
import flask
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google_scopes
from src.generic_routes import generic_bp
from src.api.auth_routes import auth_bp

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.debug("Line 16 debuger is working")

CREDENTIALS_FILE_NAME = 'credentials.json' # OAuth Client secret file provided by GCP
__base_dir__ = os.path.join(os.getcwd(), '')
__credentials_file__ = os.path.join(__base_dir__, CREDENTIALS_FILE_NAME)

SCOPES = [
    google_scopes.GenericScopes.OPENID.value,
    google_scopes.UserInfoScopes.EMAIL.value,
    google_scopes.UserInfoScopes.PROFILE.value,
    google_scopes.CalendarScopes.READONLY.value,
    google_scopes.TaskScopes.READONLY.value,
    google_scopes.DriveScopes.VIEW_MANAGE.value,
    google_scopes.DriveScopes.METADATA_READONLY.value,
    google_scopes.SheetScopes.RAEDONLY.value
]

SAMPLE_SPREADSHEET_ID = "1XZ9QFJKZKit6O1rWYcpMdpNLXgAO7mn_vnAGrRGR7qQ"
SAMPLE_RANGE_NAME = "Sheet1!A2:B3"

app = flask.Flask(__name__)
app.config.from_object('setup.config.Config')

# Route Registration
# app.register_blueprint(generic_bp)
# app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/')
def index():
  return print_index_table()

@app.route('/authorize')
def authorize():
    
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        __credentials_file__, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state

    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
  
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        __credentials_file__, scopes=SCOPES, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)
    
    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.redirect(flask.url_for('index'))


@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
        params={'token': credentials.token},
        headers = {'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.' + print_index_table())
    else:
        return('An error occurred.' + print_index_table())


@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleared.<br><br>' +
            print_index_table())

@app.route('/test')
def test_api_request():
    """
    a sample test
    """

    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    if not credentials.valid:
        return flask.redirect('authorize')
    
    service = build("drive", "v3", credentials=credentials)

    files = service.files().list().execute()

    flask.session['credentials'] = credentials_to_dict(credentials)

    return flask.jsonify(**files)

from pprint import pprint
def get_specific_sheets(sheet: object, sheet_id: str, range: str) -> list:

    result = (
          sheet.values()
          .get(spreadsheetId=sheet_id, range=range)
          .execute()
      )
    values: list = result.get("values", [])
    return values
def get_all_sheets_data(sheet: object, sheet_id: str, without_headers: bool =False) -> list:
    """
    - properties:
        - gridProperties:
            - columnCount: 26
            - rowCount: 1000
        - index: 1
        - sheetId: 546508778
        - sheetType: 'GRID'
        - title: 'Sheet2'
    """
    result = (
          sheet
          .get(spreadsheetId=SAMPLE_SPREADSHEET_ID)
          .execute()
      )
      
    sheet_metadata: list = result.get("sheets", [])
    pprint(sheet_metadata)
    values = []
    for indivisual_sheet in sheet_metadata:
        _: str = indivisual_sheet.get('properties', {}).get('sheetId')
        title: str = indivisual_sheet.get('properties', {}).get('title')
        
        _range = f"{title}"
        if without_headers == True:
            _range = _range + "!" +"A2:z999999"
        values.append(get_specific_sheets(sheet, sheet_id, range=_range))
    return values

@app.route('/test2')
def test_sheets_api_request():
    
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    if not credentials.valid:
        return flask.redirect('authorize')
    
    service = build("sheets", "v4", credentials=credentials)

    try:
      # Call the Sheets API
      sheet = service.spreadsheets()
      data: list = get_all_sheets_data(sheet, SAMPLE_SPREADSHEET_ID, without_headers=True)
      print(data)

    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")

    return flask.jsonify({"message": "check console"})

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

def print_index_table():
    return ('<table>' +
            '<tr><td><a href="/test">Test a Drive API request</a></td>' +
            '<tr><td><a href="/test2">Test a Sheet API request</a></td>'  +
            '<td>Submit an API request and see a formatted JSON response. ' +
            '    Go through the authorization flow if there are no stored ' +
            '    credentials for the user.</td></tr>' +
            '<tr><td><a href="/authorize">Test the auth flow directly</a></td>' +
            '<td>Go directly to the authorization flow. If there are stored ' +
            '    credentials, you still might not be prompted to reauthorize ' +
            '    the application.</td></tr>' +
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
            '<td>Revoke the access token associated with the current user ' +
            '    session. After revoking credentials, if you go to the test ' +
            '    page, you should see an <code>invalid_grant</code> error.' +
            '</td></tr>' +
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
            '<td>Clear the access token currently stored in the user session. ' +
            '    After clearing the token, if you <a href="/test">test the ' +
            '    API request</a> again, you should go back to the auth flow.' +
            '</td></tr>' +
            '<tr><td><a href="/run-example/1" target="_blank">Run Example - 1</a></td>' +
            '<td>This example lists all files and folders in the provided folder-id' +
            '</td></tr>' +
            '<tr><td><a href="/run-example/2" target="_blank">Run Example - 2</a></td>' +
            '<td>This example upload file to drive in the provided folder-id' +
            '</td></tr>' +
            '<tr><td><a href="/run-example/3" target="_blank">Run Example - 3</a></td>' +
            '<td>This example uploads csv file as sheet in the provided folder-id' +
            '</td></tr>' +
            '<tr><td><a href="/run-example/4" target="_blank">Run Example - 4</a></td>' +
            '<td>This example download files from drive in the downloads folder of system' +
            '</td></tr>' +
            '<tr><td><a href="/run-example/5" target="_blank">Run Example - 5</a></td>' +
            '<td>This example creates folder in drive ' +
            '</td></tr>' +
            
            '</table>'
            )
if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(
        host="0.0.0.0",
        port=app.config["PORT"]
    )
