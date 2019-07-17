import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from  sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import models


@app.route('/')
def index():
    """Searches the database for entries, then displays them."""
    return render_template('index.html', ideas=_get_ideas())

def _get_ideas():
    ideas = db.session.query(models.Idea).order_by(func.random()).limit(app.config['IDEAS_PER_REQUEST'])
    return [i.text for i in ideas]
    
@app.route('/get_ideas', methods=['POST'])
def get_ideas():
    """Get ideas from a database."""
    ideas = _get_ideas()
    return jsonify({'ideas': ideas})

@app.route('/rate', methods=['POST'])
def rate():
    fail = jsonify({'status': 0})
    if not 'id' in request.form or not 'field' in request.form:
        return fail
    idea_id = request.form['id']
    field = request.form['field']
    if field not in {'likes', 'dislikes', 'skips'}:
        return fail
    idea = db.session.query(models.Idea).get(idea_id)
    if idea is None:
        return fail
    setattr(idea, field, getattr(models.Idea, field) + 1)
    db.session.commit()
    return jsonify({'status': 1})

if __name__ == '__main__':
    DEBUG = True
    app.run(debug = DEBUG)
