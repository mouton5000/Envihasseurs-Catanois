from flask import Flask, session, redirect, url_for,request, render_template
from controllers import app
from user import *
import redis

REDIS = redis.StrictRedis()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.getUser(username)
        if user != 0 and user.hpw == getHash(request.form['password']):
            session['username'] = username
            session['joueur_num'] = user.jnum
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

def getHash(password):
  import hashlib
  return hashlib.sha1(password).hexdigest()
