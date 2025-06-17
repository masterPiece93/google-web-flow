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


class GcpWebAuthVariables:

    GOOGLE_CLIENT_ID = env.str("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = env.str("GOOGLE_CLIENT_SECRET")


class RedisVariables:

    REDIS_HOST = env.str("REDIS_HOST")
    REDIS_PORT = env.int("REDIS_PORT")
    REDIS_CONN_STRING = f"redis://{REDIS_HOST}:{REDIS_PORT}"


class Config(
    ServerStartupVariables, 
    SecurityRelatedVariables, 
    GcpWebAuthVariables, 
    RedisVariables):
    """
    main configuration variables
    """

    DEBUG = env.bool("DEBUG")
    
    
