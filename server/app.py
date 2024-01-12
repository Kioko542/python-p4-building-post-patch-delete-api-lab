#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

# Existing routes (bakeries, bakery_by_id, baked_goods_by_price, most_expensive_baked_good)

# POST route for creating a new BakedGood
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get("name"),
        price=data.get("price"),
        bakery_id=data.get("bakery_id")
    )

    db.session.add(new_baked_good)
    db.session.commit()

    response = make_response(new_baked_good.to_dict(), 201)
    return response

# PATCH route for updating the name of a Bakery
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery_name(id):
    data = request.form
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery:
        bakery.name = data.get("name", bakery.name)
        db.session.commit()

        response = make_response(bakery.to_dict(), 200)
    else:
        response = make_response({"error": "Bakery not found"}, 404)

    return response

# DELETE route for deleting a BakedGood
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.filter_by(id=id).first()

    if baked_good:
        db.session.delete(baked_good)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Baked Good deleted."
        }
        response = make_response(response_body, 200)
    else:
        response = make_response({"error": "Baked Good not found"}, 404)

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
