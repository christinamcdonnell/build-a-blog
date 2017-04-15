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

class MainHandler(webapp2.RequestHandler):
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 5")
        #self.render('front.html', posts = posts)
        t = jinja_env.get_template("post.html")
        content = t.render(posts = posts)
        self.response.write(content)

# Post class defines the entity-fields and ???
class Post(db.Model): # my Table is called 'Post' = the class name
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class NewPost(webapp2.RequestHandler):
#
    def get(self):
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content: # ASK ASK ASK about if stuff???
            p = Post( subject = subject, content = content) #create and assign an instance of the db entity
            p.put()
            self.redirect('/blog/%s' %str(p.key().id())) # lookup p.key().id() - do i need to provide the id ???
                                                         # Had a question about this can't remember it
        else:
            error = "Ahem...subject and content, please!"
            #self.render("newpost.html", subject=subject, content=content, error=error)
            t = jinja_env.get_template("newpost.html")
            content = t.render(subject=subject, content=content, error=error)
            self.response.write(content)

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        retrieved_model_post_instance = Post.get_by_id(int(id))
        #self.response.write(retrieved_model_post_instance.id) #write the key to use for testing, delete later

        if not retrieved_model_post_instance:  # if we can't find the post, reject.
            self.renderError(400)
            return

        # render post on page
        t = jinja_env.get_template("permalink.html")
        content = t.render(subject=retrieved_model_post_instance.subject, content=retrieved_model_post_instance.content)
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/blog', MainHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
    #('/blog/([0-9]+)', PostPage),
    ('/newpost', NewPost),
], debug=True)
