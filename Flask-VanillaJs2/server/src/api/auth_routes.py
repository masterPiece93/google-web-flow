"""
This is where we will
"""

from flask import (
    Blueprint,
    request,
    jsonify,
    current_app,
    session,
    redirect,
    url_for
)
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests


auth_bp = Blueprint(
    'auth',
    __name__
)

absolute_url_for = lambda value : request.url_root.strip("/") + "/" + url_for(value).strip("/")

def get_redirect_uri() -> str:
    """
    *   Since Oauth consent screen is set for `localhost`, hence
        we must access the endpoints on browser using `http://localhost:<port>/...`
        for local environment
    *   But for production environments , we must use the hosted domain .

    Forms the google callback `redirect_uri` based on above considerations
    """
    if current_app.config.get("DEBUG"):
        port: int = current_app.config["PORT"]
        return f"http://localhost:{port}" + url_for("auth.callback")
    
    return absolute_url_for("auth.callback")

def final_redirect_uri() -> str:
    """
    *   Since Oauth consent screen is set for `localhost`, hence
        we must access the endpoints on browser using `http://localhost:<port>/...`
        for local environment
    *   But for production environments , we must use the hosted domain .

    Forms the application post login `redirect_uri` based on above considerations
    """
    if current_app.config.get("DEBUG"):
        port: int = current_app.config["PORT"]
        return f"http://localhost:{port}" + "/ui"
    
    return absolute_url_for("auth.logged_in")

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

# routes & controllers
# --------------------
@auth_bp.route('/login', methods=['GET'])
def login():
    flow = Flow.from_client_config(
        client_config={
            "web":
            {
                    "client_id": current_app.config["GOOGLE_CLIENT_ID"]
                ,   "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"]
                ,   "auth_uri":"https://accounts.google.com/o/oauth2/v2/auth"
                ,   "token_uri":"https://oauth2.googleapis.com/token"
            }
        }
        #if you need additional scopes, add them here
        ,scopes=[
            "https://www.googleapis.com/auth/userinfo.email"
            ,"https://www.googleapis.com/auth/userinfo.profile"
            ,"openid"
            ,"https://www.googleapis.com/auth/drive"
        ]      
    )

    flow.redirect_uri = get_redirect_uri()
    
    authorization_url, state = (
        flow.authorization_url(
            access_type="offline"
            ,prompt="select_account"
            ,include_granted_scopes="true"
        )
    )
    session['state'] = state
    if "final_redirect" not in session or not session["final_redirect"]:
        session['final_redirect'] = final_redirect_uri() # directs where to land after login is successful.

    return redirect(authorization_url)

@auth_bp.route('/signin-google', methods=['GET'])
def callback():
    #pull the state from the session
    session_state = session['state']
    redirect_uri = request.base_url
    #pull the authorization response
    authorization_response = request.url  
    #create our flow object similar to our initial login with the added "state" information
    flow = Flow.from_client_config(
        client_config={
            "web":
            {
                "client_id": current_app.config["GOOGLE_CLIENT_ID"]
                ,"client_secret": current_app.config["GOOGLE_CLIENT_SECRET"]
                ,"auth_uri":"https://accounts.google.com/o/oauth2/v2/auth"
                ,"token_uri":"https://oauth2.googleapis.com/token"
            }
        }
        ,scopes=[
            "https://www.googleapis.com/auth/userinfo.email"
            ,"https://www.googleapis.com/auth/userinfo.profile"
            ,"openid"
            ,"https://www.googleapis.com/auth/drive"
        ]  
        ,state=session_state    
    )  

    flow.redirect_uri = redirect_uri  
    #fetch token
    flow.fetch_token(authorization_response=authorization_response)
    #get credentials
    credentials = flow.credentials
    #verify token, while also retrieving information about the user
    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token
        ,request= requests.Request()
        ,audience= current_app.config["GOOGLE_CLIENT_ID"]
        ,clock_skew_in_seconds=5
    )
    #setting the user information to an element of the session
    #you'll generally want to do something else with this (login, store in JWT, etc)
    session["id_info"] = id_info
    session["credentials"] = credentials_to_dict(credentials)
    #redirecting to the final redirect (i.e., logged in page)
    redirect_response = redirect(session['final_redirect'])   

    return redirect_response

# --------------- Spreadsheet Blueprint --------------- #
# TODO: Cut and include in seperate blueprint file .



# --------------- Spreadsheet Blueprint --------------- #
