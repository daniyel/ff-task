import re
from flask_restful import Resource, reqparse, inputs
from main.models.plate import PlateModel
from main.utils.levenshtein import levenshteinDistance


class SearchPlate(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'key',
        type=inputs.regex('^[0-9A-Z]+$'),
        required=True,
        location='args',
        help='This query cannot be left blank')
    parser.add_argument(
        'levenshtein',
        type=int,
        required=True,
        location='args',
        help='This query cannot be left blank')

    def get(self):
        data = SearchPlate.parser.parse_args()
        key = data['key']
        levenshtein = int(data['levenshtein'])
        matches = []

        for plate in PlateModel.query.all():
            match = re.search(
                r'(^[A-ZäöüÄÖÜß]{1,3})-([A-ZäöüÄÖÜß]{1,2}[1-9][0-9]{1,3})$',
                plate.plate)
            token2 = match.group(1) + match.group(2)
            distance = levenshteinDistance(key, token2)
            plate.plate = token2

            if distance <= levenshtein:
                matches.append(plate.json())

        return {key: matches}, 200
