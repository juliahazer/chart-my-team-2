from flask import redirect, render_template, request, url_for, Blueprint 
from project.leagues.models import League
from project.seasons.models import Season
from project import db

leagues_blueprint = Blueprint(
  'leagues',
  __name__,
  template_folder='templates'
)

@leagues_blueprint.route('/')
def index():
  seasons = Season.query.order_by(Season.year.desc(), Season.name.asc()).all()
  leagues = League.query.order_by(League.year.desc(), League.name.asc()).all()
  return render_template('leagues/index.html', leagues=leagues, seasons=seasons)

@leagues_blueprint.route('/<int:id>')
def show(id):
  seasons = Season.query.order_by(Season.year.desc(), Season.name.asc()).all()
  # leagues = League.query.order_by(League.year.desc(), League.name.asc()).all()
  curr_league = League.query.get(int(id))
  leagues = League.query.filter_by(season_id=curr_league.season_id).order_by(League.year.desc(), League.name.asc()).all()
  return render_template('leagues/show.html', seasons=seasons, curr_league=curr_league, leagues=leagues)