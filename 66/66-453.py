import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config["UPLOAD_FOLDER"] = "static/uploads"


class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(250), nullable=True, default='Not Available')
    img_path: Mapped[str] = mapped_column(String(250), nullable=True, default='Not Available')
    location: Mapped[str] = mapped_column(String(250), nullable=True, default='Not Available')
    seats: Mapped[str] = mapped_column(String(250), nullable=True, default='Not Available')
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True, default='Not Available')

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/api/random")
def get_random_cafe():
    try:
        cafes = Cafe.query.all()
    except Exception as e:
        return jsonify({"message": f'Database error: {str(e)}'}), 500
    else:
        if not cafes:
            return jsonify({'message': f'No cafe found'}), 404
        else:
            rand_cafe = random.choice(cafes)
            return jsonify(rand_cafe.to_dict()), 200


@app.route("/api/all-cafe")
def get_all_cafe():
    try:
        cafes = Cafe.query.all()
    except Exception as e:
        return jsonify({"message": f'Database error: {str(e)}'}), 500
    else:
        if not cafes:
            return jsonify({'message': 'No cafe found'}), 204
        else:
            return jsonify([cafe.to_dict() for cafe in cafes]), 200


@app.route("/api/search-cafe/<location>")
def get_search_cafe(location: str):
    try:
        cafes = Cafe.query.filter_by(location=location).all()
    except Exception as err:
        return jsonify({'message': f'Database error {str(err)}'}), 500
    else:
        if not cafes:
            return jsonify({'message': f'No cafe found at {location}'}), 204
        else:
            return jsonify([cafe.to_dict() for cafe in cafes]), 200


@app.route('/api/add-cafe', methods=['POST'])
def add_cafe():
    required_fields = {
        'name',
        'has_toilet',
        'has_wifi',
        'has_sockets',
        'can_take_calls'
    }

    try:
        data = request.json
    except Exception as err:
        return jsonify({'message': f'Error while parsing {err}'}), 500
    else:
        missing_fields = required_fields - data.keys()

        if missing_fields:
            return jsonify({'message': f'Missing fields {" ,".join(missing_fields)}'}), 400
        else:
            new_cafe = Cafe(
                name=data['name'],
                map_url=data.get('map_url'),
                img_path=data.get('img_path'),
                location=data.get('location'),
                seats=data.get('seats'),
                has_toilet=data['has_toilet'],
                has_wifi=data['has_wifi'],
                has_sockets=data['has_sockets'],
                can_take_calls=data['can_take_calls'],
                coffee_price=data.get('coffee_price')
            )

    try:
        db.session.add(new_cafe)
        db.session.commit()
    except Exception as db_err:
        db.session.rollback()
        return jsonify({'message': f'Error while saving {db_err}'}), 500
    else:
        return jsonify({'message': 'Cafe created successfully'}), 201


@app.route('/api/update-cafe/<int:id>', methods=['PUT', 'PATCH'])
def update_cafe(id: int):
    restricted_fields = {'id', 'name'}

    try:
        data = request.json
    except Exception as err:
        return jsonify({'message': f'Error parsing request: {err}'}), 500
    else:
        if not data:
            return jsonify({'message': f'No data provided'}), 400
        else:
            cafe = Cafe.query.get_or_404(id)

            for key, value in data.items():
                if key not in restricted_fields and hasattr(cafe, key):
                    setattr(cafe, key, value)

            try:
                db.session.commit()
            except Exception as db_err:
                db.session.rollback()
                return jsonify({'message': f'Error updating cafe: {db_err}'}), 500
            else:
                return jsonify({'message': 'Cafe updated successfully'}), 200


@app.route('/api/delete-cafe/<int:id>', methods=['DELETE'])
def delete_cafe(id: int):
    try:
        cafe = Cafe.query.get_or_404(id)
    except Exception as err:
        return jsonify({'message': f'Unexpected error {err}'})
    else:
        try:
            db.session.delete(cafe)
            db.session.commit()
        except Exception as db_err:
            db.session.rollback()
            return jsonify({'message': f'Database error: {db_err}'}), 500
        else:
            return jsonify({'message': 'Cafe deleted successfully'}), 200


def main():
    pass


if __name__ == '__main__':
    app.run(debug=True)
