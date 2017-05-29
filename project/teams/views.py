from flask import redirect, render_template, request, url_for, Blueprint 
from project.teams.models import Team
from project import db

teams_blueprint = Blueprint(
  'teams',
  __name__,
  template_folder='templates'
)

@teams_blueprint.route('/')
def index(id):
  return "hello"
  # return render_template('messages/new.html', form=form)