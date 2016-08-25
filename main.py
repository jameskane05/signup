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

import webapp2
import pprint
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        signup_form = """
            <form method="POST">
                <label for="username">Username:</label>
                <input type="text" name="username" id="username" value="{}"><br>
                <label for="password">Password:</label>
                <input type="password" name="password" id="password" value=""><br>
                <label for="verify">Verify Password:</label>
                <input type="password" name="verify" id="verify" value=""><br>
                <label for="email">Email:</label>
                <input type="email" name="email" id="email" value="{}"><br>
                <input type="submit" name="submit" id="submit">
            </form>
        """.format(username,email)

        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>"

        self.response.write(page_header + signup_form + error_element + page_footer)

    def post(self):
        errors_exist = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        pw_re = re.compile(r"^.{3,20}$")
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        def valid_username(username):
            return user_re.match(username)
        def valid_password(password):
            return pw_re.match(password)
        def valid_email(email):
            return email_re.match(email)

        if not password or not verify:
            errors_exist = True
            error = "You did not enter your password twice!"
            self.redirect("/?username={}&error={}".format(username,error))
        else:
            if not password == verify:
                error = "Your passwords don't match."
                self.redirect("/?error={}".format(username,error))
            if valid_password(password) is None:
                errors_exist = True
                error = "This password is invalid."
                self.redirect("/?username={}&error={}".format(username,error))

        if not username:
            errors_exist = True
            error = "You did not enter a username!"
            self.redirect("/?email={}&error={}".format(email,error))
        else:
            if valid_username(username) is None:
                errors_exist = True
                error = "This username is invalid."
                self.redirect("/?error={}".format(error))

        if email:
            if valid_email(email) is None:
                errors_exist = True
                error = "This email is invalid."
                self.redirect("/?username={}&email={}&error={}".format(username,email,error))

        if not errors_exist:
            self.redirect("/welcome?username={}".format(username))

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        welcome_section = "<h1>Hello, {}</h1>".format(username)
        self.response.write(page_header + welcome_section + page_footer)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
