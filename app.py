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
    ideas = db.session.query(models.Idea)
    return render_template('index.html', ideas=_get_ideas())

def _get_ideas():
    ideas = db.session.query(models.Idea).order_by(func.random()).limit(app.config['IDEAS_PER_REQUEST'])
    return [i.text for i in ideas]
    
@app.route('/get_ideas', methods=['POST'])
def get_ideas():
    """Get ideas from a database."""
    ideas = _get_ideas()
    return jsonify(ideas)

if __name__ == '__main__':
    DEBUG = True
    app.run(debug = DEBUG)
