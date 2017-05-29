from project import db

class League(db.Model):

  __tablename__ = 'leagues'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Text)

  def __init__(self, name): 
    self.name = name

  def __repr__(self):
    return "#{}: name: {}".format(self.id, self.name)