from app import db
from models import Idea

ideas = []
with open('ideas.txt') as f:
    for line in f:
        ideas.append(Idea(text=line.strip()))

s = db.session
s.bulk_save_objects(ideas)
s.commit()