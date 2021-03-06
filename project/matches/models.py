from project import db

class Match(db.Model):

  __tablename__ = 'matches'

  id = db.Column(db.Integer, primary_key=True)
  scorecard_id = db.Column(db.Integer, db.ForeignKey('scorecards.id'))
  match_type = db.Column(db.Text)
  line = db.Column(db.Integer)
  h_1_player_id = db.Column(db.Integer)
  h_1_player_name = db.Column(db.Text)
  h_2_player_id = db.Column(db.Integer)
  h_2_player_name = db.Column(db.Text)
  v_1_player_id = db.Column(db.Integer)
  v_1_player_name = db.Column(db.Text)
  v_2_player_id = db.Column(db.Integer)
  v_2_player_name = db.Column(db.Text)
  winning_score = db.Column(db.Text)
  winner = db.Column(db.Text)

  #I use this in displaying the matches for a team to highlight if
  #the current team is home or visitor (which is based on scoredcard table data)
  are_home = None

  def __repr__(self):
    return "#{}: scorecard_id: {} - match_type: {} - line: {}".format(self.id, self.scorecard_id, self.match_type, self.line)