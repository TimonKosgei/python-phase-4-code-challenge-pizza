#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

class Restaurants(Resource):
    def get(self):
        resturants = []
        for restaurant in Restaurant.query.all():
            resturants.append(
                {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "address": restaurant.address
                }
            )
        return make_response(jsonify(resturants), 200)

class RestaurantsById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if not restaurant:
            return make_response(jsonify({"error":"Restaurant not found"}),404)
        if restaurant:
            return make_response(jsonify(restaurant.to_dict()),200)

    def delete(self,id):
        restaurant = Restaurant.query.filter(Restaurant.id == id).first()
        if not restaurant:
            return make_response(jsonify({"error":"Restaurant not found"}),404)
        if restaurant:
            db.session.delete(restaurant)
            db.session.commit()
            response_body = ""
            return make_response(jsonify(response_body),204)
        
class Pizzas(Resource):
    def get(self):
        pizzas = []
        for pizza in Pizza.query.all():
            pizzas.append(
                {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients}
            )
        return make_response(jsonify(pizzas), 200)

class RestaurantPizzas(Resource):
    def post(self):
        try:
            data =request.get_json()
            price = data.get("price")
            pizza_id = data.get("pizza_id")
            restaurant_id = data.get("restaurant_id")
            #new restaurant pizza
            restaurant_pizza  =RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(restaurant_pizza)
            db.session.commit()

            if restaurant_pizza:
                return make_response(jsonify(restaurant_pizza.to_dict()),201)
        except Exception as e:
            return make_response(jsonify({"errors":["validation errors"]}),400)


api.add_resource(Restaurants,"/restaurants")
api.add_resource(RestaurantsById,"/restaurants/<int:id>")
api.add_resource(Pizzas,"/pizzas")
api.add_resource(RestaurantPizzas,"/restaurant_pizzas")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
