#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#import os
#from string import letters
import webapp2
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

#def render_str(template, **params):
#    t = jinja_env.get_template(template)
#    return t.render(params)

#class BlogHandler(webapp2.RequestHandler):
#    def write(self, *a, **kw):
#        self.response.write(*a, **kw)
#
#    def render_str(self, template, **params):
#        t = jinja_env.get_template(template)
#        return t.render(params)
#
#    def render(self, template, **kw):
#        self.write(self.render_str(template, **kw))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        #self.render('front.html', posts = posts)
        t = jinja_env.get_template("front.html")
        content = t.render(posts = posts)
        self.response.write(content)
        #self.response.write('Hello world!')
        #unwatched_movies = db.GqlQuery("SELECT * FROM Movie where watched = False")
        #t = jinja_env.get_template("frontpage.html")
        #content = t.render(
        #                movies = unwatched_movies,
        #                error = self.request.get("error"))
        #self.response.write(content)

#def blog_key(name = 'default'):
#    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)


#class BlogFront(BlogHandler):
#    def get(self):
#        posts = db.GqlQuery("select * from Post order by created desc limit 10")
#        self.render('front.html', posts = posts)

class PostPage(webapp2.RequestHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)

        if not post:
            self.error(404)
            return

        #self.render("permalink.html", post = post)
        t = jinja_env.get_template("permalink.html")
        content = t.render(post = post)
        self.response.write(content)


class NewPost(webapp2.RequestHandler):
#class AddMovie(Handler): ###########FIX FIX FIX FIX
    def get(self):
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post( subject = subject, content = content)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "Ahem...subject and content, please!"
            #self.render("newpost.html", subject=subject, content=content, error=error)
            t = jinja_env.get_template("newpost.html")
            content = t.render(subject=subject, content=content, error=error)
            self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog/([0-9]+)', PostPage),
    ('/newpost', NewPost),
], debug=True)
