from project import db

class Season(db.Model):

  __tablename__ = 'seasons'

  id = db.Column(db.Integer, primary_key=True)
  year = db.Column(db.Integer)
  name = db.Column(db.Text)
  leagues = db.relationship('League', backref='season', lazy='dynamic')
  teams = db.relationship('Team', backref='season', lazy='dynamic')

  def __init__(self, year, name):
    self.year = year 
    self.name = name

  def __repr__(self):
    return "#{}: year: {} - name: {}".format(self.id, self.year, self.name)