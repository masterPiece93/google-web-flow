"""README
This is where we start writing our api's


- You may rename the variables according to your needs .
    for e.g :
        you may rename `sample_api_v1_bp` to `module_v1`

- In case you don't require versioning altogether , you may move out
    this file & delete the `/v1` folder altogether
    - consequently , you'll just have to modify the import statement in `app.py` file .

NOTE : remove this comment ( in triple quotes ) after you have read and understood . 
"""

from flask import Blueprint, url_for, current_app, jsonify

generic_bp = Blueprint(
    'generic',
    __name__,
    url_prefix=''
)

@generic_bp.route('/')
def root():
    heading: str = "Google Sheets Processing"
    sub_heading: str = "This is a PoC demonstration of google sheets access and processing"
    return f"""
    <h>{heading}</h>
    <p>{sub_heading}</p>
    """

@generic_bp.route('/health')
def health():
    """Indicates Server Health"""
    # add logic to check / ping server components
    return {"status": "OK"}

@generic_bp.route('/ping')
def ping():
    """server ping"""
    return "pong"

def _has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@generic_bp.route("/api-index")
def site_map():
    """Lists all the registered routes"""
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and _has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return jsonify({"data": links})

# add more routes ( as per your needs ) here ...