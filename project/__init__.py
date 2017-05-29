from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgres://localhost/chart-my-team-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "it's a secret"

modus = Modus(app)
db = SQLAlchemy(app)

from project.teams.views import teams_blueprint
from project.players.views import players_blueprint
# from project.teams.models import Team
# from project.players.models import Player

app.register_blueprint(teams_blueprint, url_prefix='/teams')
app.register_blueprint(players_blueprint, url_prefix='/players')

@app.route('/')
def root(): 
  # following = current_user.following.all()
  # following_ids = [f.id for f in following]
  # messages = Message.query.order_by("timestamp desc").filter(Message.user_id.in_(following_ids)).limit(100).all()
  return render_template('home.html') #, messages=messages)

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
