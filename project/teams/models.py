from project import db

class Team(db.Model):

  __tablename__ = 'teams'

  id = db.Column(db.Integer, primary_key=True)
  league_id = db.Column(db.Integer)
  season_id = db.Column(db.Integer)
  name = db.Column(db.Text)
  area = db.Column(db.Text)
  num_match_scheduled = db.Column(db.Integer)
  num_match_played = db.Column(db.Integer)
  matches_won = db.Column(db.Integer)
  matches_lost = db.Column(db.Integer)

  #should team ID be a separate thing - can I init with it?
  def __init__(self, season_id, name, area):
    self.season_id = season_id
    self.name = name
    self.area = area

  def __repr__(self):
    return "#{}: name: {} - area: {}".format(self.id, self.name, self.area)