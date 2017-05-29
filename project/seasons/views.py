from flask import redirect, render_template, request, url_for, Blueprint 
from project.seasons.models import Season
from project import db

seasons_blueprint = Blueprint(
  'seasons',
  __name__,
  template_folder='templates'
)

@seasons_blueprint.route('/')
def index():
  return render_template('seasons/index.html')

# @teams_blueprint.route('/<int:id>')
# def show(id):