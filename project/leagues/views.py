from flask import redirect, render_template, request, url_for, Blueprint, jsonify
from project.leagues.models import League
from project.seasons.models import Season
from project.teams.models import Team
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
  seasons = Season.query.filter(Season.year>=2015).order_by(Season.year.desc(), Season.name.asc()).all()
  curr_league = League.query.get(int(id))
  leagues = League.query.filter_by(season_id=curr_league.season_id).order_by(League.year.desc(), League.name.asc()).all()
  teams = Team.query.filter_by(league_id=id).order_by(Team.name.asc()).all()
  return render_template('leagues/show.html', seasons=seasons, curr_league=curr_league, leagues=leagues, teams=teams)

@leagues_blueprint.route('/json')
def json():
  leagues_dict = {}
  for l in League.query.all():
    leagues_dict[l.id] = {
      'year': l.year,
      'name': l.name,
      'season_id': l.season_id
    }
  return jsonify(leagues_dict)

@leagues_blueprint.route('/<int:id>/json')
def teams_json(id):
  curr_league = League.query.get(id)
  teams_dict = {}
  for t in curr_league.teams.all():
    teams_dict[t.id] = {
      'league_id': t.league_id,
      'season_id': t.season_id,
      'name': t.name,
      'area': t.area,
      'num_match_scheduled': t.num_match_scheduled,
      'num_match_played': t.num_match_played,
      'matches_won': t.matches_won,
      'matches_lost': t.matches_lost
    }
  return jsonify(teams_dict)