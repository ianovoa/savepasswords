from google.appengine.ext import ndb
import webapp2
import jinja2
import os
import time


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=["jinja2.ext.autoescape"], autoescape=True)


class Password(ndb.Model):
    name = ndb.StringProperty(required=True)
    user = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    url = ndb.StringProperty()


class PassView(webapp2.RequestHandler):
    def get(self):
        passwords = Password.query()
        template_values = {'passwords': passwords}
        template = JINJA_ENVIRONMENT.get_template("passView.html")
        self.response.write(template.render(template_values))


class LoadNewPass(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template("form.html")
        self.response.write(template.render())


class NewPass(webapp2.RequestHandler):
    def load_input(self):
        self.name = self.request.get("name", "no_name")
        self.user = self.request.get("user", "no_user")
        self.password = self.request.get("pass", "no_pass")
        self.url = self.request.get("url", "no_url")

    def post(self):
        self.load_input()
        password = Password(name=self.name, user=self.user, password=self.password, url=self.url)
        password.put()
        time.sleep(0.5)
        passwords = Password.query()
        template_values = {'passwords': passwords}
        template = JINJA_ENVIRONMENT.get_template("passView.html")
        self.response.write(template.render(template_values))


class DeletePass(webapp2.RequestHandler):
    def load_input(self):
        key = self.request.get("key", None)
        self.id=key[16:len(key)-1]


    def get(self):
        self.load_input()
        p=Password.get_by_id(int(self.id))
        p.key.delete()
        time.sleep(0.5)
        passwords = Password.query()
        template_values = {'passwords': passwords}
        template = JINJA_ENVIRONMENT.get_template("passView.html")
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/index', PassView),
    ('/loadNew', LoadNewPass),
    ('/new', NewPass),
    ('/del', DeletePass)
], debug=True)
