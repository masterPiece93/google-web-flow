import secrets
from environs import env

env.read_env()


class ServerStartupVariables:
    """
    variables related to server startup
    """

    PORT = env.int("PORT")
    HOST = "0.0.0.0"

class SecurityRelatedVariables:

    SECRET_KEY = secrets.token_hex()

class Config(ServerStartupVariables, SecurityRelatedVariables):
    """
    main configuration variables
    """

    DEBUG = env.bool("DEBUG")
    
    
