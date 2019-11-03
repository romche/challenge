from django.urls import reverse
from rest_framework.test import APITestCase  # , APIClient
from rest_framework.views import status
from oauth2_provider.models import Application, AccessToken
from django.contrib.auth.models import User
from .models import Restaurant
from .serializers import RestaurantSerializers
import datetime
import json


class BaseViewTest(APITestCase):

    @staticmethod
    def create_restaurant(name="", address=""):
        if name != "" and address != "":
            Restaurant.objects.create(name=name, address=address)

    def setUp(self):
        # add test data
        self.test_user = User.objects.create_user('test',
                                                  'test',
                                                  'test@example.com')
        # Set Up a Test Application
        self.application = Application(
            name="Test Application",
            redirect_uris="http://localhost",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
        )
        self.application.save()

        self.tok = AccessToken.objects.create(
            user=self.test_user,
            token='1234567890',
            application=self.application,
            scope='read write',
            expires=datetime.datetime.now() + datetime.timedelta(days=1)
        )

        self.create_restaurant("Restaurant 1", "Mikonkatu 1, Helsinki")
        self.create_restaurant("Restaurant 2", "Mikonkatu 5, Helsinki")
        self.create_restaurant("Restaurant 3", "Mikonkatu 10, Helsinki")
        self.create_restaurant("Restaurant 4", "Mikonkatu 15, Helsinki")


class RestaurantsListTest(BaseViewTest):

    def test_get_all_restaurants_status_code(self):
        """
        This test ensures that endpoint is return status_code 200
        when we make a GET request to the api/restaurants endpoint
        """
        # Create A Token
        self.fetch_url = reverse("restaurant_list")

        # Set Authorization Header
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.tok.token,
        }
        # Make assertions
        # # hit the API endpoint
        response = self.client.get(self.fetch_url,
                                   format='json',
                                   **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_fail_all_restaurants(self):
        """
        This test ensures that request fails without Access Token
        when we make a GET request to the api/restaurants endpoint
        """
        # Create A Token
        self.fetch_url = reverse("restaurant_list")

        # Make assertions
        # # hit the API endpoint
        response = self.client.get(self.fetch_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_restaurant_restaraunt_list(self):
        """
        This test ensures that new restaurant can be added
        when we make a POST request to the api/restaurants endpoint
        """
        # Create A Token
        self.fetch_url = reverse("restaurant_list")

        # Set Authorization Header
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.tok.token,
        }
        # Make assertions
        # # hit the API endpoint
        response = self.client.post(self.fetch_url,
                                    data={
                                        "name": "New Restaurant",
                                        "address": "Keskuskatu 1, Helsinki"
                                        },
                                    **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_unvalid_restaurant_restaraunt_list(self):
        """
        This test ensures that new restaurant with unvalid format
        will return bad request 400 when we make a POST request to the
        api/restaurants endpoint

        """
        # Create A Token
        self.fetch_url = reverse("restaurant_list")

        # Set Authorization Header
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.tok.token,
        }
        # Make assertions
        # # hit the API endpoint
        response = self.client.post(self.fetch_url,
                                    data={
                                        "foo": "New",
                                        "bar": "New"
                                        },
                                    **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_fail_restaurants_restarant_list(self):
        """
        This test ensures that request fails without Access Token when
        we make POST request to api/restaurants endpoint
        """
        # Create A Token
        self.fetch_url = reverse("restaurant_list")

        # Make assertions
        # # hit the API endpoint
        response = self.client.post(self.fetch_url,
                                    json={
                                        'name': 'New Restaurant',
                                        'address': 'Keskuskatu 1, Helsinki'
                                        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_serializators_restarant_list(self):
        """
        This test ensures that all restaurants added in the setUp method
        exist when we make a GET request to the api/restaurants endpoint
        """
        self.fetch_url = reverse("restaurant_list")

        # Set Authorization Header
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.tok.token,
        }

        # Make assertions
        # hit the API endpoint
        response = self.client.get(self.fetch_url,
                                   format='json',
                                   **auth_headers)
        # fetch the data from db
        expected = Restaurant.objects.all()
        serialized = RestaurantSerializers(expected, many=True)
        self.assertEqual(response.data, serialized.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RestaurantsTest(BaseViewTest):

    def test_get_without_token_one_restaurant(self):
        """
        Ensure we can't get restaurant object when we make
        a GET request to pi/restaurants/<int:pk> endpoint.
        """
        url = reverse('restaurant',
                      kwargs={
                        "pk": 1
                        }
                      )
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_with_token_one_restaurant(self):
        """
        Ensure we can get restaurant object when we make
        a GET request to pi/restaurants/<int:pk> endpoint.
        """
        # TODO: change pk later...
        test_id = Restaurant.objects.all()[0].id
        url = reverse('restaurant',
                      kwargs={
                        "pk": test_id
                        }
                      )

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.tok.token,
        }
        response = self.client.get(url, format='json', **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_without_token_one_restaurant(self):
        """
        Ensure we can't get restaurant object when we make
        a PUT request to pi/restaurants/<int:pk> endpoint.
        """
        test_id = Restaurant.objects.all()[0].id
        url = reverse('restaurant',
                      kwargs={
                        "pk": test_id
                        }
                      )

        data = {
            "name": "Rest X",
            "address": "Keskuskatu 3, Helsinki"
        }

        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_with_token_one_restaurant(self):
        """
        Ensure we can get restaurant object when we make
        a PUT request to pi/restaurants/<int:pk> endpoint.
        """
        # TODO: change pk later...
        test_id = Restaurant.objects.all()[0].id

        data = {
            "name": "Rest X",
            "address": "Keskuskatu 3, Helsinki"
        }

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.tok.token,
        }
        # response = self.client.put(url, data, **auth_headers)

        response = self.client.put(
            reverse('restaurant', kwargs={'pk': test_id}),
            data=json.dumps(data),
            content_type='application/json',
            **auth_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_with_token_one_restaurant_bad_request(self):
        """
        Ensure we get BAD_REQUEST when we make it bad when we
        do a PUT request to pi/restaurants/<int:pk> endpoint.
        """
        # TODO: change pk later...
        test_id = Restaurant.objects.all()[0].id

        data = {
            "address": "Keskuskatu 3, Helsinki"
        }

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + self.tok.token,
        }
        # response = self.client.put(url, data, **auth_headers)

        response = self.client.put(
            reverse('restaurant', kwargs={'pk': test_id}),
            data=json.dumps(data),
            content_type='application/json',
            **auth_headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
