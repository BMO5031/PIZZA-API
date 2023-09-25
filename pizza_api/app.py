from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)





class Restaurants(db.Model):
    id = db.Column(db.Integer,primary_key=True) 
    name = db.Column(db.String(50))
    address = db.Column(db.String(500))
      # Define the one-to-many relationship with Pizza
    pizzas = db.relationship('Pizzas', backref='restaurant', lazy=True)

class Pizzas(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    ingredients = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Define the foreign key to link Pizza to Restaurant
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

class Restaurant_pizzas(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    pizza_id = db.Column(db.Integer,db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer,db.ForeignKey("restaurants.id"))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

def insert_dummy_data():
    # Create and insert sample Restaurants
    restaurant1 = Restaurants(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
    restaurant2 = Restaurants(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")
    db.session.add_all([restaurant1, restaurant2])

    # Create and insert sample Pizzas
    pizza1 = Pizzas(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pizza2 = Pizzas(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    db.session.add_all([pizza1, pizza2])

    # Create and insert sample Restaurant_pizzas associations
    restaurant_pizza1 = Restaurant_pizzas(price=10, pizza_id=pizza1.id, restaurant_id=restaurant1.id)
    restaurant_pizza2 = Restaurant_pizzas(price=12, pizza_id=pizza2.id, restaurant_id=restaurant2.id)
    db.session.add_all([restaurant_pizza1, restaurant_pizza2])

    db.session.commit()



with app.app_context():
    # Create the database tables
    db.create_all()
    # Insert dummy data
    insert_dummy_data()




@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurants.query.all()
    restaurant_list = [
        {'id': restaurant.id, 'name': restaurant.name, 'address': restaurant.address}
        for restaurant in restaurants
    ]
    return jsonify(restaurant_list)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurants.query.get(id)
    if restaurant:
        pizzas = [{'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}
                  for pizza in restaurant.pizzas]
        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': pizzas
        }
        return jsonify(restaurant_data)
    return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurants.query.get(id)
    if restaurant:
        try:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'RestaurantPizza records are associated with this restaurant'}), 400
    return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizzas.query.all()
    pizza_list = [
        {'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients}
        for pizza in pizzas
    ]
    return jsonify(pizza_list)

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not all([price, pizza_id, restaurant_id]):
        return jsonify({'errors': ['Validation errors']}), 400

    restaurant_pizza = Restaurant_pizzas(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
    db.session.add(restaurant_pizza)
    try:
        db.session.commit()
        pizza = Pizzas.query.get(pizza_id)
        return jsonify({'id': pizza.id, 'name': pizza.name, 'ingredients': pizza.ingredients})
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['Validation errors']}), 400

if __name__ == '__main__':
    app.run(debug=True)
    
