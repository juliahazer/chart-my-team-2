from flask import redirect, render_template, request, url_for, Blueprint, jsonify
from project.leagues.models import League

leagues_blueprint = Blueprint(
  'leagues',
  __name__,
  template_folder='templates'
)

@leagues_blueprint.route('/json')
def json():
  # leagues_list_2 = []
  # leagues_sub = League.query.filter(League.year>=2015).order_by(League.id.desc()).all()
  # for l in leagues_sub:
  #   leagues_list_2.append(l.id)
  # print(len(leagues_list_2))
  # print(leagues_list_2)

  leagues_list = []
  for l in League.query.order_by(League.year.desc(), League.name.asc()).all():
    leagues_list.append({
      'id': l.id,
      'year': l.year,
      'name': l.name,
      'season_id': l.season_id
    })
  return jsonify(leagues_list)

@leagues_blueprint.route('/<int:id>/json')
def teams_json(id):
  curr_league = League.query.get(id)
  teams_list = []
  # teams_id_list = []
  for t in curr_league.teams.all():
    # teams_id_list.append(t.id)
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
  # print(teams_id_list)
  return jsonify(teams_list)