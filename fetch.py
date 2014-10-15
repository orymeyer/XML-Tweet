import yql,twitter,model,webapp2
from twitter import *


class init(webapp2.RequestHandler):
    def get(self):
        y = yql.Public()
        query = 'select * from xml where url="http://www.espncricinfo.com/rss/content/story/feeds/0.xml"'
        res = y.execute(query)
        #last notification
        tweet = "A small Status"
        #tweet = res.rows[0]['channel']['item'][0]['description']
        #fetch from GAE datastore
        fetched  = model.fetch()
        if not fetched:
            model.add('INITIALIZATION')
            self.response.write('INIT')
        else:            
            fetched = str(list(r.tweet for r in fetched)[0])
            self.response.write('  Fetching  ')
        
        if tweet == fetched:
            self.response.write('  Same Tweet  ')
            pass
        else:
            model.add(tweet)
            if len(tweet) >140:
                a,b = None,None
                a,b  = split(tweet)
                update(a,b)
                self.response.write('  Updated & Added  ')
            else:
                update(tweet,None)
                self.response.write('  Updated & Added  ')

                
                


def split(tweet):
    return "[1/2]"+tweet[0:135],"[2/2]"+tweet[135:len(tweet)]
    
#a,b = split(tweet)




def update(a,b):

    consumer_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 
    consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" 

    access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


    t = Twitter(
        auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))



    res={}
    if b is None:
        res = t.statuses.update(status=a)
    else:
        res[0] = t.statuses.update(status=b)
        res[1] = t.statuses.update(status=a)

#update(a,b)

application = webapp2.WSGIApplication([
    ('/fetch', init),
], debug=True)

