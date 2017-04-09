import webapp2
import cgi
import re

# html boilerplate for header and footer
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign Up</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

class Index(webapp2.RequestHandler):
    def get(self):
        edit_header = "<h1>User Sign up </h1>"

        usernameerror = self.request.get('uerror')
        passworderror = self.request.get('perror')
        emailerror = self.request.get('emerror')
        username = self.request.get('username')
        useremail = self.request.get('useremail')

        form = """
        <form action="/welcome" method="post">
            <label>Username</label>
                <input type="text" name="username" value="{uname}" required/> <font style="color:red" pattern="">{uerror}</font>
            <br>
            <label>Password</label>
                <input type="password" name="password1" required/>
            <br>
            <label>Verify Password</label>
                <input type="password" name="password2" required/> <font style="color:red" pattern="">{perror}</font>
            <br>
            <label>Email (optional)</label>
                <input type="email" name="useremail" value="{uemail}"/> <font style="color:red" pattern="">{eerror}</font>
            <br>
            <input type="submit" value="Submit"/>
        </form>
        """.format(uname=username, uerror=usernameerror, perror=passworderror, uemail=useremail, eerror=emailerror)

        main_content = edit_header + form
        response = page_header + main_content + page_footer
        self.response.write(response)



class Welcome(webapp2.RequestHandler):

    def post(self):

        uerror = ""
        perror = ""
        emerror = ""
        username = self.request.get('username')
        password1 = self.request.get("password1")
        password2 = self.request.get('password2')
        useremail = self.request.get('useremail')

        user_re = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
        password_re = re.compile(r"^.{3,20}$")
        email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")

        # check if passwords match
        if not password1 == password2:
            perror = "Passwords don't match."
            self.redirect('/?perror={}&username={}&useremail={}'.format(cgi.escape(perror, quote=True),username,useremail))

        # check if password is valid
        if password_re.match(password1) == None:
            perror = "Invalid password, try again."
            self.redirect('/?perror={}&username={}&useremail={}'.format(cgi.escape(perror, quote=True),username,useremail))

        # check if username is valid
        if user_re.match(username) == None:
            uerror = "Invalid username, try again."
            self.redirect('/?uerror={}&useremail={}'.format(cgi.escape(uerror, quote=True),useremail))

        # check if email is valid
        if email_re.match(useremail) == None:
            emerror = "Invalid username, try again."
            self.redirect('/?username={}&emerror={}'.format(cgi.escape(emerror, quote=True),useremail))

        welcome_message = "<h1>Welcome, {0}!</h1>".format(username)

        main_content = welcome_message

        response = page_header + main_content + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)
