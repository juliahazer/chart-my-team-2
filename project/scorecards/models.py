from project import db

class Scorecard(db.Model):

  __tablename__ = 'scorecards'

  id = db.Column(db.Integer, primary_key=True)
  home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
  visitor_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
  date = db.Column(db.DateTime)
  league_id = db.Column(db.Integer, db.ForeignKey('leagues.id'))
  matches = db.relationship('Match', backref='scorecard', lazy='dynamic')

  def __init__(self, date, home_team_id, visitor_team_id):
    self.date = date 
    self.home_team_id = home_team_id
    self.visitor_team_id = visitor_team_id

  def __repr__(self):
    return "#{}: date: {} - home_team_id: {} - visitor_team_id: {}".format(self.id, self.date, self.home_team_id, self.visitor_team_id)