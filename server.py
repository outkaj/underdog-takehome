import os
import flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless
import psycopg2

POSTGRES = {
    'user': 'postgres',
    'pw': os.environ['POSTGRES_PASSWORD'],
    'db': 'candidates',
    'host': 'localhost',
    'port': '5432',
}

# Create the Flask application and the Flask-SQLAlchemy object.
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""Connect the database to Flask app."""
# Configure to use PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)

class Candidate(db.Model):
    __tablename__ = 'candidates'
    #id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.Unicode)
    last_name = db.Column(db.Unicode)
    expertise = db.Column(db.Unicode, primary_key=True)
    location = db.Column(db.Unicode)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in list(self._to_dict().items())
        })

    def to_json(self):
        """
                Define a base way to jsonify models
        """
        return {
            'type': 'candidate_list',
            'data': [{
                'first_name': self.first_name,
                'last_name': self.last_name,
                'expertise': self.expertise,
                'location': self.location
            }]
        }

try:
    conn = psycopg2.connect(database=POSTGRES['db'], user=POSTGRES['user'],
                            password=POSTGRES['pw'], host=POSTGRES['host'], port=POSTGRES['port'])
except:
    print("I am unable to connect to the database")
cur = conn.cursor()
f = open('candidate_data.csv')
cur.copy_from(f, "candidates", columns=(
    "first_name", "last_name", "expertise", "location"), sep=",")
conn.commit()
conn.close()
db.create_all()

# Create the Flask-Restless API manager.
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Candidate, methods=['GET'])

if __name__ == '__main__':
    app.run()
