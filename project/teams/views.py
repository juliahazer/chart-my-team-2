from flask import redirect, render_template, request, url_for, Blueprint 
from project.teams.models import Team
from project.leagues.models import League
from project.seasons.models import Season
from project import db

teams_blueprint = Blueprint(
  'teams',
  __name__,
  template_folder='templates'
)

@teams_blueprint.route('/')
def index(id):
  id = int(id)
  curr_league = League.query.get(id)
  seasons = Season.query.order_by(Season.year.desc(), Season.name.asc()).all()
  leagues = League.query.filter_by(season_id=curr_league.season_id).order_by(League.year.desc(), League.name.asc()).all()
  teams = Team.query.filter_by(league_id=id).order_by(Team.name.asc()).all()
  # areas = db.session.query(Team.area.distinct()).all() #NEED TO FIX THIS TO LIMIT IT!!!
  return render_template('teams/index.html', seasons=seasons, leagues=leagues, curr_league=curr_league, teams=teams)

@teams_blueprint.route('/<int:team_id>')
def show(id, team_id):
  curr_team = Team.query.get(team_id)
  curr_league = League.query.get(id)
  seasons = Season.query.order_by(Season.year.desc(), Season.name.asc()).all()
  leagues = League.query.filter_by(season_id=curr_league.season_id).order_by(League.year.desc(), League.name.asc()).all()
  teams = Team.query.filter_by(league_id=id).order_by(Team.name.asc()).all()
  return render_template('teams/show.html', seasons=seasons, leagues=leagues, curr_league=curr_league, teams=teams, curr_team =curr_team)