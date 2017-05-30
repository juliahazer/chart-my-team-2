from project import db

class League(db.Model):

  __tablename__ = 'leagues'

  id = db.Column(db.Integer, primary_key=True)
  year = db.Column(db.Integer)
  name = db.Column(db.Text)
  season_id = db.Column(db.Integer, db.ForeignKey('seasons.id'))
  teams = db.relationship('Team', order_by="Team.name", backref='league', lazy='dynamic')

  def __init__(self, year, name, season_id):
    self.year = year 
    self.name = name
    self.season_id = season_id

  def __repr__(self):
    return "#{}: year: {} - name: {} - season_id: {}".format(self.id, self.year, self.name, self.season_id)