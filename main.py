#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
import os
import urllib
import sys, inspect

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2
from models.core import *
from tests.gendata import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)
    name = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


# [END greeting]
def checkLogin(self):
    user = users.get_current_user()
    if not user:
        self.redirect(users.create_login_url(self.request.uri))



# [START main_page]
class MainPage(webapp2.RequestHandler):
    def get(self):
        checkLogin(self)
        entity_set = self.request.get('entity_set', 'Consumer')

        entity_class=globals()[entity_set]
        entity_query=entity_class.query()
        entities = entity_query.fetch(100)
 
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        model_classes = inspect.getmembers(sys.modules[__name__], inspect.isclass)

        template_values = {
            'user': user,
            'greetings': entities,
            'entity_set': entity_set,
            'url': url,
            'url_linktext': url_linktext,
            'model_classes': model_classes
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


# [END main_page]


# [START guestbook]
class Guestbook(webapp2.RequestHandler):
    def post(self):
        entity_set = self.request.get('entity_set', 'Consumer')
        query_params = {'entity_set': entity_set}
        self.redirect('/?' + urllib.urlencode(query_params))


# [END guestbook]
class GendataHandler(webapp2.RequestHandler):
    def post(self):
        entity_set = self.request.get('entity_set', 'Consumer')
        t = Gendata()
        create_fun=getattr(t,'create_'+entity_set.lower())
        create_fun()

        query_params = {'entity_set': entity_set}
        self.redirect('/?' + urllib.urlencode(query_params))

class EmptyKindHandler(webapp2.RequestHandler):
    def post(self):
        entity_set = self.request.get('entity_set', 'Consumer')
        g = Gendata()
        g.empty_table(entity_set)

        query_params = {'entity_set': entity_set}
        self.redirect('/?' + urllib.urlencode(query_params))


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/gendata', GendataHandler),
    ('/emptykind', EmptyKindHandler)
], debug=True)
# [END app]
