from flask import Flask, session, redirect, url_for, escape, request, render_template
import functools
import re

app = Flask(__name__)

# set the secret key.  keep this really secret:
app.secret_key = 'd\xb6\xab#\x80\x97<E\x83\x85\xcb\x18\xe6\x9fs\xd6\x94Tr\x9e\xeb\xfe\xb5\xbe'

def needLogin(f):
    @functools.wraps(f)
    def helper(*args,**kwargs):
        if 'username' in session:
            return f(*args,**kwargs)
        else:
            return '{"error":"login"}'           
 
    return helper


@app.route('/')
def index():
    if 'username' in session:
        return render_template('logoutForm.html')
    else:
        return render_template('login.html')

import controllers.ressources
