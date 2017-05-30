from project import db

class Player(db.Model):

  __tablename__ = 'players'

  id = db.Column(db.Integer, primary_key=True)
  player_id = db.Column(db.Integer)
  name = db.Column(db.Text)
  city = db.Column(db.Text)
  gender = db.Column(db.Text)
  rating = db.Column(db.Text)
  np_sw = db.Column(db.Text)
  expiration = db.Column(db.Text)
  won = db.Column(db.Integer)
  lost = db.Column(db.Integer)
  matches = db.Column(db.Integer)
  defaults = db.Column(db.Integer)
  win_percent = db.Column(db.Integer)
  singles = db.Column(db.Integer)
  doubles = db.Column(db.Integer)
  team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

  #should team ID be a separate thing - can I init with it?
  def __init__(self, name, rating):
    self.name = name
    self.rating = rating

  def __repr__(self):
    return "#{}: name: {} - rating: {}".format(self.id, self.name, self.rating)