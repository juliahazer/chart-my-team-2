from flask import redirect, render_template, request, url_for, Blueprint 
from project.rosters.models import Roster
from project import db

rosters_blueprint = Blueprint(
  'rosters',
  __name__,
  template_folder='templates'
)

@rosters_blueprint.route('/')
def index():
  return "hello"
  # return render_template('messages/new.html', form=form)