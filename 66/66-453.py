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
    map_url: Mapped[str] = mapped_column(String(250), nullable=True)
    img_path: Mapped[str] = mapped_column(String(250), nullable=True)
    location: Mapped[str] = mapped_column(String(250), nullable=True)
    seats: Mapped[str] = mapped_column(String(250), nullable=True)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

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
            return jsonify({'message': 'No cafe found'}), 404
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
            return jsonify({'message': f'No cafe found at {location}'}), 404
        else:
            return jsonify([cafe.to_dict() for cafe in cafes]), 200


@app.route('/api/add-cafe', methods=['POST'])
def add_cafe():
    try:
        data = request.json
    except Exception as err:
        return jsonify({'message': f'Error while parsing {err}'}), 500
    else:
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        else:
            name = data.get('name', 'N/A')
            map_url = data.get('map_url', 'N/A')

            new_cafe = Cafe(
                name=name,
                map_url=map_url
            )

    try:
        db.session.add(new_cafe)
        db.session.commit()
    except Exception as db_err:
        return jsonify({'message': f'Error while posting {db_err}'}), 500
    else:
        return jsonify({'message': 'Cafe created successfully'}), 201


def main():
    pass

if __name__ == '__main__':
    app.run(debug=True)
