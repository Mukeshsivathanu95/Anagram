from google.appengine.ext import ndb
from google.appengine.api import users
class MyList(ndb.Model):
    strings = ndb.StringProperty(repeated=True)
    lexographical = ndb.StringProperty()
    email = ndb.StringProperty()
    wordcount=ndb.IntegerProperty()
    lettercount=ndb.IntegerProperty()
