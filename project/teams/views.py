from flask import redirect, render_template, request, url_for, Blueprint, jsonify
from project.teams.models import Team
from project.leagues.models import League
from project.seasons.models import Season
from project.rosters.models import Roster
from project import db

teams_blueprint = Blueprint(
  'teams',
  __name__,
  template_folder='templates'
)

@teams_blueprint.route('/')
def index():
  # curr_league = League.query.get(id)
  # seasons = Season.query.filter(Season.year>=2015).order_by(Season.year.desc(), Season.name.asc()).all()
  # leagues = League.query.filter_by(season_id=curr_league.season_id).order_by(League.year.desc(), League.name.asc()).all()
  # teams = Team.query.filter_by(league_id=id).order_by(Team.name.asc()).all()
  # areas = db.session.query(Team.area.distinct()).all() #NEED TO FIX THIS TO LIMIT IT!!!
  return render_template('teams/index.html')#, seasons=seasons, leagues=leagues, curr_league=curr_league, teams=teams)

@teams_blueprint.route('/<int:id>')
def show(id):
  curr_team = Team.query.get(id)
  #rosters = curr_team.rosters.all();
  #curr_league = League.query.get(curr_team.league_id)
  #seasons = Season.query.filter(Season.year>=2015).order_by(Season.year.desc(), Season.name.asc()).all()
  #leagues = League.query.filter_by(season_id=curr_league.season_id).order_by(League.year.desc(), League.name.asc()).all()
  #teams = Team.query.filter_by(league_id=curr_team.league_id).order_by(Team.name.asc()).all()
  if len(curr_team.rosters.all()) > 0:
    has_rosters = True
  else:
    has_rosters = False
  return render_template('teams/show.html', curr_team=curr_team, has_rosters=has_rosters)#seasons=seasons, leagues=leagues, curr_league=curr_league, teams=teams, curr_team =curr_team, rosters=rosters)

@teams_blueprint.route('/<int:id>/json')
def get_team_json(id):
  curr_team = Team.query.get(id)
  rosters_list = []
  for r in curr_team.rosters.all():
    rosters_list.append({
      'team_id': r.team_id,
      'player_id': r.player_id,
      'name': r.name,
      'city': r.city,
      'gender': r.gender,
      'rating': r.rating,
      'np_sw': r.np_sw,
      'expiration': r.expiration,
      'won': r.won,
      'lost': r.lost,
      'matches': r.matches,
      'defaults': r.defaults,
      'win_percent': r.win_percent,
      'singles': r.singles,
      'doubles': r.doubles,
      'team_name': curr_team.name,
      'area': curr_team.area
    })
  return jsonify(rosters_list)