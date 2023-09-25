# PIZZA-API
# Week 1 Code Challenge - Pizza Restaurants

--This Flask-based API project is designed for the Week 1 Code Challenge. The goal of this challenge is to build a fully functional API for a Pizza Restaurant domain. The project provides endpoints to manage restaurants, pizzas, and the associations between them.

# Models
# Relationships

- A Restaurant has many Pizzas through RestaurantPizza.
- A Pizza has many Restaurants through RestaurantPizza.
- A RestaurantPizza belongs to a Restaurant and belongs to a Pizza.

- The project starts by creating the necessary models and migrations for the following database tables:

* DataBase Schema

# Validations

# RestaurantPizza Model Validations:
- Must have a price between 1 and 30.

# Restaurant Model Validations:
- Must have a name less than 50 characters in length.
- Must have a unique name.

# Routes

- The API offers the following routes to interact with the data. Each route returns JSON data in the specified format and utilizes the appropriate HTTP verb.

# 1. GET /restaurants

# Description: Retrieve a list of all restaurants.

# Response Format:

json

[
{
"id": 1,
"name": "Dominion Pizza",
"address": "Good Italian, Ngong Road, 5th Avenue"
},
{
"id": 2,
"name": "Pizza Hut",
"address": "Westgate Mall, Mwanzi Road, Nrb 100"
}
]

# 2. GET /restaurants/:id

# Description: Retrieve a specific restaurant by its ID.

# Response Format:

- If the restaurant exists:

json

{
"id": 1,
"name": "Dominion Pizza",
"address": "Good Italian, Ngong Road, 5th Avenue",
"pizzas": [
{
"id": 1,
"name": "Cheese",
"ingredients": "Dough, Tomato Sauce, Cheese"
},
{
"id": 2,
"name": "Pepperoni",
"ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
}
]
}

- If the restaurant does not exist, the response is:

json

{
"error": "Restaurant not found"
}

# 3. DELETE /restaurants/:id

- Description: Delete a specific restaurant by its ID, along with its associated RestaurantPizzas.

# Response Format:

- If the restaurant is successfully deleted:

Empty response body with an appropriate HTTP status code.

- If the restaurant does not exist, the response is:

json

{
"error": "Restaurant not found"
}

# 4. GET /pizzas

# Description: Retrieve a list of all pizzas.

# Response Format:

json

[
{
"id": 1,
"name": "Cheese",
"ingredients": "Dough, Tomato Sauce, Cheese"
},
{
"id": 2,
"name": "Pepperoni",
"ingredients": "Dough, Tomato Sauce, Cheese, Pepperoni"
}
]

# 5. POST /restaurant_pizzas

- Description: Create a new RestaurantPizza associated with an existing Pizza and Restaurant.

# Request Body Format:

json

{
"price": 5,
"pizza_id": 1,
"restaurant_id": 3
}

# Response Format:

- If the RestaurantPizza is created successfully:

json

{
"id": 1,
"name": "Cheese",
"ingredients": "Dough, Tomato Sauce, Cheese"
}

- If the RestaurantPizza is not created successfully, the response is:

json

{
"errors": ["Validation errors"]
}

# License

- This project is licensed under the MIT License - see the LICENSE.md file for details.

# AUTHOR:
BRIAN MARTIN ODHIAMBO

