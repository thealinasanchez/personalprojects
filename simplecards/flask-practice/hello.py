from flask import Flask
'''
instance of the Flask class will be our WSGI application
WSGI app - Web server Gateway Interface. Specification for 
simple/universal interface between web servers and Python web
app/frameworks. WSGI allows diff web servers and web apps to communicate
w/ each other in a standard way
''' 

app = Flask(__name__)
'''
parameter in Flask is for the name of the application's module or package.
__name__ is a convenient shortcut for this. Needed so Flask knows where to
look for resources such as templates and static files
'''

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
'''
route() decorator used to tell Flask what URL should trigger our function
The default content type for these functions is HTML.

If you want the server to be accessible from other computers you can make
the server publicly available by adding --host=0.0.0.0. For ex:
flask run --host=0.0.0.0

If you enable debug mode, the the server will automatically reload if code
changes & will show interactive debugger in browser for errors during a
request. Ex: flask --app hello run --debug.

"When returning HTML (the default response type in Flask), any
user-provided values rendered in the output must be escaped to protect from
injection attacks"
- injection attack - occurs when an attacker is able to inject malicious
    code into a program or system. 
- escaping - converting special characters in the user-provided content 
    into special sequences of characters. By converting these characters
    into their HTML entity (ex: < is &lt), the browser interprets them as 
    plain text and not as executable code so attacker's can't attack.
'''
