from flask import Flask, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgres://localhost/chart-my-team-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "it's a secret"

modus = Modus(app)
db = SQLAlchemy(app)

from project.teams.views import teams_blueprint
from project.rosters.views import rosters_blueprint
from project.seasons.views import seasons_blueprint
from project.leagues.views import leagues_blueprint
from project.scorecards.views import scorecards_blueprint
from project.matches.views import matches_blueprint

from project.scorecards.models import Scorecard
from project.matches.models import Match

app.register_blueprint(teams_blueprint, url_prefix='/teams')
app.register_blueprint(seasons_blueprint, url_prefix='/seasons')
app.register_blueprint(leagues_blueprint, url_prefix='/leagues')
app.register_blueprint(scorecards_blueprint, url_prefix='/scorecards') #url_prefix='/teams/<int:id>/scorecards')
app.register_blueprint(matches_blueprint, url_prefix='/matches')
app.register_blueprint(rosters_blueprint, url_prefix='/rosters')

@app.route('/')
def root(): 
  return render_template('/index.html')

@app.route('/about')
def about():
    return render_template('/about.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
