from flask import redirect, render_template, request, url_for, Blueprint, jsonify
from project.teams.models import Team

teams_blueprint = Blueprint(
  'teams',
  __name__,
  template_folder='templates'
)

@teams_blueprint.route('/')
def index():
  # areas = db.session.query(Team.area.distinct()).all() #NEED TO FIX THIS TO LIMIT IT!!!
  return render_template('teams/index.html')

@teams_blueprint.route('/<int:id>')
def show(id):
  curr_team = Team.query.get(id)
  #seasons = Season.query.filter(Season.year>=2015).order_by(Season.year.desc(), Season.name.asc()).all()
  if len(curr_team.rosters.all()) > 0:
    has_rosters = True
  else:
    has_rosters = False
  return render_template('teams/show.html', curr_team=curr_team, has_rosters=has_rosters)

@teams_blueprint.route('/<int:id>/scorecards')
def scorecards(id):
  curr_team = Team.query.get(id)
  #n+1 query FIX LATER!!!
  scorecards_h = curr_team.h_scorecards.all()
  scorecards_v = curr_team.v_scorecards.all()
  scorecards = scorecards_h + scorecards_v
  #sort by date
  scorecards.sort(key=lambda x: x.date, reverse=False)  
  return render_template('teams/scorecards.html', scorecards=scorecards, curr_team = curr_team)

@teams_blueprint.route('/<int:id>/matches')
def matches(id):
  curr_team = Team.query.get(id)
  #n+1 query FIX LATER!!!
  scorecards_h = curr_team.h_scorecards.all()
  scorecards_v = curr_team.v_scorecards.all()
  scorecards = scorecards_h + scorecards_v
  scorecards.sort(key=lambda x: x.date, reverse=False)  

  matches = []
  for scorecard in scorecards:
    matches += scorecard.matches.all()

  for match in matches:
    if match.scorecard.team_h.id == id:
      match.are_home = True
    else:
      match.are_home = False

  return render_template('teams/matches.html', matches=matches, curr_team=curr_team)

@teams_blueprint.route('/<int:id>/matches_json')
def matches_json(id):
  curr_team = Team.query.get(id)
  #n+1 query FIX LATER!!!
  scorecards_h = curr_team.h_scorecards.all()
  scorecards_v = curr_team.v_scorecards.all()
  scorecards = scorecards_h + scorecards_v
  scorecards.sort(key=lambda x: x.date, reverse=False) 

  matches = []
  for scorecard in scorecards:
    matches += scorecard.matches.all()

  for match in matches:
    if match.scorecard.team_h.id == id:
      match.are_home = True
    else:
      match.are_home = False

  json_matches_list = []

  for m in matches:
    obj = {
      'scorecard_id': match.scorecard.id,
      'type': m.match_type,
      'line': m.line,
      'winning_score': match.winning_score
    }
    obj['date'] = match.scorecard.date.strftime('%m-%d-%y')
    if match.are_home:
      obj['location'] = 'Home'
      obj['opponent'] = match.scorecard.team_v.name
      obj['opponent_id'] = match.scorecard.team_v.id
      obj['team_player_1'] = match.h_1_player_name
      obj['team_player_1_id'] = match.h_1_player_id
      obj['opp_player_1'] = match.v_1_player_name
      obj['opp_player_1_id'] = match.v_1_player_id
      if match.match_type == 'doubles':
        obj['team_player_2'] = match.h_2_player_name
        obj['team_player_2_id'] = match.h_2_player_id
        obj['opp_player_2'] = match.v_2_player_name
        obj['opp_player_2_id'] = match.v_2_player_id
    else:
      obj['location'] = 'Away'
      obj['opponent'] = match.scorecard.team_h.name
      obj['opponent_id'] = match.scorecard.team_h.id
      obj['team_player_1'] = match.v_1_player_name
      obj['team_player_1_id'] = match.v_1_player_id
      obj['opp_player_1'] = match.h_1_player_name
      obj['opp_player_1_id'] = match.h_1_player_id
      if match.match_type == 'doubles':
        obj['team_player_2'] = match.v_2_player_name
        obj['team_player_2_id'] = match.v_2_player_id
        obj['opp_player_2'] = match.h_2_player_name
        obj['opp_player_2_id'] = match.h_2_player_id
    if match.are_home and match.winner == 'Home':
      obj['winner'] = 'Team'
    else:
      obj['winner'] = 'Opponent'

    json_matches_list.append(obj)

  return jsonify(json_matches_list)


@teams_blueprint.route('/<int:id>/json')
def team_json(id):
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