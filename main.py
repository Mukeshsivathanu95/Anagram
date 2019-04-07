from itertools import groupby
import webapp2
import jinja2
from google.appengine.api import users
import os
from mylist import MyList
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        my_list = None
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            key = ndb.Key('MyList', user.user_id())
            my_list = key.get()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        template_values = {'url' : url,'url_string' : url_string,'user' : user,'welcome' : welcome,'my_list' : my_list}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
            self.response.headers['Content-Type'] = 'text/html'
            user = users.get_current_user()
            string = self.request.get('input')
            string_sort=''.join(k for k, g in groupby(sorted(string)))
            emailsample=users.get_current_user().email()
            key = ndb.Key('MyList', string_sort+emailsample)
            my_list = key.get()
            if my_list==None:
                my_list=MyList(id=string_sort+emailsample)
                my_list.put()
            key = ndb.Key('MyList', string_sort+emailsample)
            my_list = key.get()
            action=self.request.get('button')
            if action == 'add':
                string = self.request.get('input')
                if string == None or string == '':
                    self.redirect('/')
                    return
                my_list.strings.append(string)
                my_list.lexographical=string_sort
                my_list.wordcount=len(my_list.strings)
                my_list.lettercount=len(my_list.lexographical)
                my_list.email=emailsample
            my_list.put()
            self.redirect('/add')

class AddItem(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("""<form method="post" action="/">
        Word:<input type="text" name="input" pattern="[a-zA-Z]+" required/><br/>
        <input type="submit" name="button" value="add"/>
        </form>""")
        self.response.out.write("<b><p><a href='/'>Home</a></p></b>")
        self.response.out.write("</body></html>")



class SearchItem(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        email=users.get_current_user().email()
        string = self.request.get('input')
        string_sort=''.join(k for k, g in groupby(sorted(string)))
        key = ndb.Key('MyList', string_sort+email)
        my_list = key.get()
        template_values = {'my_list':my_list}
        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.redirect('/show')

class Anagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user=users.get_current_user().email()
        query=MyList.query(MyList.email==users.get_current_user().email())
        template_values = {'query':query}
        template = JINJA_ENVIRONMENT.get_template('uanagram.html')
        self.response.write(template.render(template_values))

class ShowDetails(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        email=users.get_current_user().email()
        query=MyList.query(MyList.email==users.get_current_user().email())
        template_values = {'query':query}
        template = JINJA_ENVIRONMENT.get_template('show.html')
        self.response.write(template.render(template_values))













app = webapp2.WSGIApplication([('/', MainPage),('/add',AddItem),('/search',SearchItem),('/uanagram',Anagram),('/show',ShowDetails)], debug=True)
