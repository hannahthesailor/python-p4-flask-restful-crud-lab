#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class PlantByID(Resource):

    def get(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)
        return make_response(jsonify(plant.to_dict()), 200)

    def put(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        data = request.get_json()
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()

        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        data = request.get_json()
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']

        db.session.commit()

        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        db.session.delete(plant)
        db.session.commit()

        return '', 204





api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
