import re
import sys
from flask_restful import Resource
from main.models.plate import PlateModel
from flask import request


class Plate(Resource):
    def get(self):
        return [plate.json() for plate in PlateModel.query.all()]

    def post(self):
        try:
            data = request.get_json()

            if 'plate' not in data:
                return {'message': 'Field plate is missing.'}, 400

            if not re.search(
                    r'^[A-ZäöüÄÖÜß]{1,3}-[A-ZäöüÄÖÜß]{1,2}[1-9][0-9]{1,3}$', data['plate']):
                return {'message': 'Field plate is not valid German plate.'}, 422

            plate = PlateModel(data['plate'])

            try:
                plate.save_to_db()
            except BaseException:
                return {'message': 'An error occurred inserting the item.'}, 500
            return plate.json(), 200
        except BaseException:
            e = sys.exc_info()[0]
            return str(e), 400
