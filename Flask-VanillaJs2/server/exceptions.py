"""
Custom Exceptions
=================

* exceptions that represent a application faulty state .
* exceptions that are wrapper to some direct/indirect fault of
    third party software , api calls or dependency packages .
* REST api exceptions .

NOTE : these exceptions are global to the application . Can be
        used by any of the modules / sub-modules .
"""


class RedisConnectionFailed(Exception):
    """Not able to connect to Redis"""