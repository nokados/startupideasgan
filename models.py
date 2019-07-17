from app import db

class Idea(db.Model):

    __tablename__ = "ideas"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    skips = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Idea #{}: {} ({}l/{}d/{}s).>'.format(self.id, self.text, self.likes, self.dislikes, self.skips)
