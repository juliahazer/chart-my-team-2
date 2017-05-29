from flask import redirect, render_template, request, url_for, Blueprint 
from project.teams.models import Team
from project import db

teams_blueprint = Blueprint(
  'teams',
  __name__,
  template_folder='templates'
)

@teams_blueprint.route('/')
def index():
  teams = Team.query.all()
  seasons = db.session.query(Team.season_id.distinct()).all()
  leagues = db.session.query(Team.league_id.distinct()).all()
  areas = db.session.query(Team.area.distinct()).all()
  return render_template('teams/index.html', seasons=seasons, leagues=leagues, areas=areas, teams=teams)

# @teams_blueprint.route('/<int:id>')
# def show(id):