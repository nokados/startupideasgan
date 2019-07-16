from app import db

class Idea(db.Model):

    __tablename__ = "ideas"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, default=0)
    num_rates = db.Column(db.Integer, default=0)

    # def __init__(self, text):
    #     self.text = text

    def __repr__(self):
        return '<Idea #{}: {} ({}/{}).>'.format(self.id, self.text, self.rating, self.num_rates)
