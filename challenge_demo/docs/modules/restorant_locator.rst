#################
Restorant_locator
#################

API for restaurants
Idea behind that API is that we have Restaurant model, which have these fields
    * name
    * address
    * location
    * created
    * modifed

This is how it goes, when you got Access Token from endppoint of users app. User
can submit POST to /api/restaurants with token and data. Data should have name and address,
after that based on address it will get coordinates from google and will saved them in
POINT (lan lng) -format to location fields.

After that we can calculate distance if user submit address (converting address to lan, lng as well). 

Endpoints for testing (need Access Token, more on users module)
================================================================
* GET  /api/restaurants - all restaraunts
* POST /api/restaurants - add restaurant

* GET  /api/restaurants?lat=60.1704534&lng=24.9386902 - return restaurants with distance in meters

* GET /api/restaurants/<int:pk> - return one restaurant
* PUT /api/restaurants/<int:pk> - will update restaurant

data = {"name": "Restarant name", "address": "Some Address"}
