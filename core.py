from google.appengine.ext import ndb
from google.appengine.ext.db import Model


class Password(Model):
    name = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    url = ndb.StringProperty()
