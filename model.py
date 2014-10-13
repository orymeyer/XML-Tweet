from google.appengine.ext import ndb
from google.appengine.ext.db import stats

class tweetStore(ndb.Model):
    tweet = ndb.StringProperty(required=True)
    tweet_time = ndb.DateTimeProperty(auto_now_add=True)


def add(_tweet):
    t = tweetStore(parent=ndb.Key('tweet','t'))
    t.tweet = _tweet
    t.put()

def isEmpty():
    global_stat = stats.GlobalStat.all().get()
    return global_stat is None

tkey = ndb.Key('tweet','t')

def fetch():
    r = tweetStore.query(ancestor=tkey).order(-tweetStore.tweet_time)
    res = r.fetch(1)
    if len(res) < 1:
        return False #Empty Condition
    else:
        return res
    
    




