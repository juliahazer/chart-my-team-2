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
  # for scorecard in scorecards:
  #   if scorecard.home_team_id == curr_team.id:
  #     are_home = True
  #   else:
  #     are_home = False
  #   curr_matches = scorecard.matches.all()
  #   for curr_match in curr_matches:
  #     curr_match.are_home = are_home
  #   matches.append(curr_matches.all())
  # from IPython import embed; embed()

  matches = []
  for scorecard in scorecards:
    matches += scorecard.matches.all()

  for match in matches:
    if match.scorecard.team_h.id == id:
      match.are_home = True
    else:
      match.are_home = False

  return render_template('teams/matches.html', matches=matches, curr_team=curr_team)


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