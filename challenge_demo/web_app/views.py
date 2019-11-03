from django.views.generic.base import TemplateView
from restorant_locator.views import calculate_coord_from_address
from django.urls import reverse  # noqa
import requests

# TODO: Change to reverse
TOKEN_URL = 'http://localhost:8001/authentication/token/'
RESTAURANT_API_URL = 'http://localhost:8001/api/restaurants'


def get_token(username='guest', password='guest'):
    '''
    Function for getting token, this is for
    just for listing.
    format: {"username": "username", "password": "1234abcd"}

    TODO: Invalid credentials case

    Params:
        username (str): username for token, default guest
        password (str): password for token, default guest

    Returns:
        data_from_req (json): response from request

    '''
    data_form_req = requests.post(TOKEN_URL,
                                  data={
                                    "username": username,
                                    "password": password
                                    })

    return data_form_req.json()


def get_data_from_api(with_coordinates=None):
    '''
    Function for getting restaurants data from api, if
    coordinates provided will return distance as well

    Params:
        with_coordinates (str):     coordinates from calcuting
                                    distance to restaurants

    Returns:
        all_restaurants (json):     restaurants with and without
                                    distance

    '''
    if with_coordinates:
        restaurant_url = f'{RESTAURANT_API_URL}?{with_coordinates}'
    else:
        restaurant_url = RESTAURANT_API_URL
    headers = {'Authorization': f'Bearer {get_token().get("access_token")}'}
    all_restaurants = requests.get(restaurant_url, headers=headers)
    return all_restaurants.json()


class DemoPageView(TemplateView):
    '''
    Display all data, editing when got Access Token.
    '''
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        street = self.request.GET.get('street', None)
        # if street provided, then we can calculate distance
        if street:
            street_coord = calculate_coord_from_address(street,
                                                        just_coord=True)
            all_restaurants = get_data_from_api(with_coordinates=street_coord)
            context['search_street'] = str(street)
        else:
            # Here is all restaurants
            all_restaurants = get_data_from_api()
        context['all_restaurants'] = all_restaurants

        return context
