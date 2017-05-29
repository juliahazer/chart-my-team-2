from flask import redirect, render_template, request, url_for, Blueprint 
from project.players.models import Player
from project import db

players_blueprint = Blueprint(
  'players',
  __name__,
  template_folder='templates'
)

@players_blueprint.route('/')
def index():
  return "hello"
  # return render_template('messages/new.html', form=form)