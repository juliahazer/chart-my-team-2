from flask import redirect, render_template, request, url_for, Blueprint, jsonify 
from project.seasons.models import Season

seasons_blueprint = Blueprint(
  'seasons',
  __name__,
  template_folder='templates'
)

@seasons_blueprint.route('/json')
def json():
  seasons_list = []
  #THIS IS WHERE SET THE FILTER FOR SEASONS!
  #for s in Season.query.filter(Season.year>=2015).order_by(Season.year.desc(), Season.name.asc()).all():
  for s in Season.query.filter(Season.id==196).order_by(Season.year.desc(), Season.name.asc()).all():
    seasons_list.append({
      'id': s.id,
      'year': s.year,
      'name': s.name
    })
  return jsonify(seasons_list)

@seasons_blueprint.route('/<int:id>/json')
def leagues_json(id):
  curr_season = Season.query.get(id)
  leagues_list = []
  for l in curr_season.leagues.all():
    leagues_list.append({
      'id': l.id,
      'year': l.year,
      'name': l.name
    })
  return jsonify(leagues_list)

@seasons_blueprint.route('/<int:id>/teamsjson')
def teams_json(id):
  curr_season = Season.query.get(id)
  teams_list = []
  for t in curr_season.teams.all():
    teams_list.append({
      'id': t.id,
      'league_id': t.league_id,
      'season_id': t.season_id,
      'name': t.name,
      'area': t.area,
      'num_match_scheduled': t.num_match_scheduled,
      'num_match_played': t.num_match_played,
      'matches_won': t.matches_won,
      'matches_lost': t.matches_lost
    })
  return jsonify(teams_list)