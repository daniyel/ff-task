from flask import Flask
from flask_restful import Api
from main.db import db
from main.resources.plate import Plate
from main.resources.search_plate import SearchPlate
from main.config import SQLITE_CONFIG


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_CONFIG
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


api.add_resource(Plate, '/plate')
api.add_resource(SearchPlate, '/search-plate')

if __name__ == '__main__':
    app.run(debug=True)
