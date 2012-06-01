from flask import Flask, session, redirect, url_for, escape, request, render_template
from controllers import app, needLogin
import re
import controllers.login
import controllers.callback
from Jeu import *
from joueurs import *
from plateau import *
from arbre_action import *

@app.route('/players/colors')
@needLogin
def getColors():

    body = '[{"red":255, "blue":0, "green":0}, {"red":0, "blue":0, "green":255}, {"red":0, "blue":255, "green":0}, {"red":100, "blue":100, "green":100}, {"red":200, "blue":200, "green":50}]'

    body = controllers.callback.addCallback(body, request)

    return body
