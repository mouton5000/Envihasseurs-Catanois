from flask import Flask, session, redirect, url_for,request, render_template
from controllers import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'test' and request.form['password'] == 'test':
            session['username'] = request.form['username']
            session['joueur_num'] = 1
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

