"""
aho bot database binding and helper functions.
"""
from pony import orm
from aho import Config
import datetime
import random

db = orm.Database()

def bind_database(db_path):
    db.bind(provider='sqlite', filename=Config().db_path, create_db=True)

def get_or_create(cls, **kwargs):
    r = cls.get(**kwargs)
    if r is None:
        return cls(**kwargs)
    return r

