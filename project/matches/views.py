from flask import redirect, render_template, request, url_for, Blueprint, jsonify
from project.matches.models import Match
from project import db

matches_blueprint = Blueprint(
  'matches',
  __name__,
  template_folder='templates'
)

@matches_blueprint.route('/')
def index():
  matches = Match.query.all()
  return "hello"
  # return render_template('matches/index.html', matches=matches)