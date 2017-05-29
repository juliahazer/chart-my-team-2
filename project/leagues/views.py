from flask import redirect, render_template, request, url_for, Blueprint 
from project.leagues.models import League
from project import db

leagues_blueprint = Blueprint(
  'leagues',
  __name__,
  template_folder='templates'
)

@leagues_blueprint.route('/')
def index():
  return render_template('leagues/index.html')