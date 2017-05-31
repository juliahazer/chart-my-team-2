from flask import redirect, render_template, request, url_for, Blueprint, jsonify
from project.scorecards.models import Scorecard
from project import db

scorecards_blueprint = Blueprint(
  'scorecards',
  __name__,
  template_folder='templates'
)

@scorecards_blueprint.route('/')
def index(id):
  scorecards = Scorecard.query.filter((Scorecard.home_team_id==id)|(Scorecard.visitor_team_id==id)).order_by(Scorecard.date.asc()).all()

  # for scorecard in scorecards:
  #   from IPython import embed; embed()
  return render_template('scorecards/index.html', scorecards=scorecards)