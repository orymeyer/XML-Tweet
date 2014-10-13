import yql,tweepy,model,webapp2
import oauth_example.handlers

class init(webapp2.RequestHandler):
    def get(self):
        y = yql.Public()
        query = 'select * from xml where url="http://www.espncricinfo.com/rss/content/story/feeds/0.xml"'
        res = y.execute(query)
        #last notification
        tweet = res.rows[0]['channel']['item'][0]['description']
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
            a,b  = split(tweet)
            update(a,b)
            self.response.write('  Updated & Added  ')
                
                


def split(tweet):
    if len(tweet) > 60:
        return "[1/2]"+tweet[0:135],"[2/2]"+tweet[135:len(tweet)]
    else:
        return tweet

#a,b = split(tweet)




def update(a,b):

    consumer_key = "XXXXXXXXXXXXXXXXXX" 
    consumer_secret = "XXXXXXXXXXXXXXXXXX" 

    access_token = "XXXXXXXXXXXXXXXXXX"
    access_token_secret = "XXXXXXXXXXXXXXXXXX" 


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)



    res={}
    if len(b) < 1:
        res = api.update_status(a)
    else:
        res[0] = api.update_status(b)
        res[1] = api.update_status(a)

#update(a,b)

application = webapp2.WSGIApplication([
    ('/fetch', init),
], debug=True)

