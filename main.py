import yql,model,twitter,webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('Tweet Engine')



application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)

