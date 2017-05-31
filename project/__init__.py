from flask import Flask, redirect, url_for
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
from project.players.views import players_blueprint
from project.seasons.views import seasons_blueprint
from project.leagues.views import leagues_blueprint

from project.scorecards.models import Scorecard
from project.matches.models import Match

app.register_blueprint(teams_blueprint, url_prefix='/teams')
app.register_blueprint(players_blueprint, url_prefix='/leagues/<int:id>/teams/<int:t_id>/players')
app.register_blueprint(seasons_blueprint, url_prefix='/seasons')
app.register_blueprint(leagues_blueprint, url_prefix='/leagues')

@app.route('/')
def root(): 
  return redirect(url_for('teams.index'))

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
