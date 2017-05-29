from flask import redirect, render_template, request, url_for, Blueprint 
from sqlalchemy import desc
from project.seasons.models import Season
from project.leagues.models import League
from project import db

seasons_blueprint = Blueprint(
  'seasons',
  __name__,
  template_folder='templates'
)

@seasons_blueprint.route('/')
def index():
  seasons = Season.query.order_by(Season.year.desc(), Season.name.asc()).all()
  return render_template('seasons/index.html', seasons=seasons)

@seasons_blueprint.route('/<int:id>')
def show(id):
  seasons = Season.query.order_by(Season.year.desc(), Season.name.asc()).all()
  leagues = League.query.filter_by(season_id=id).order_by(League.year.desc(), League.name.asc()).all()
  season_id = id
  return render_template('seasons/show.html', seasons=seasons, season_id=season_id, leagues=leagues)