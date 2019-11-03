# from django.shortcuts import render
from rest_framework import generics
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import GEOSGeometry
from .models import Restaurant
from .serializers import RestaurantSerializers
import geocoder

# Please replace with your Geocoding API Key
GOOGLE_API_KEY = '<api_key>'


def calculate_coord_from_address(address, just_coord=False):
    '''
    Function transforms address into POINT formated coordinates,
    uses geocoder library, also needed GOOGLE_API_KEY

    Params:
        address (str):          address based on what we'll ger coords
        just_coord (boolean):   if True, will return expl. lat and lng,
                                if False, will return POINT -formated
        GOOGLE_API_KEY (str):   Needed for geocoder.google

    Returns:
        points_coordinates (str/False): if coordinates ok it will return
                                        coords, otherwise will return False
    '''
    address_geo_location = geocoder.google(address, key=GOOGLE_API_KEY)
    points_coordinates = False
    # Checking if we have some reasonable data
    if address_geo_location.ok:
        latitude = address_geo_location.latlng[0]
        longitude = address_geo_location.latlng[1]
        points_coordinates = f'POINT({latitude} {longitude})'

    if just_coord:
        points_coordinates = f'lat={latitude}&lng={longitude}'

    return points_coordinates


class ListCreateRestaurants(generics.ListCreateAPIView):
    '''
    TODO: add user to model
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializers

    def perform_create(self, serializer):
        # Saving additional points to db
        address = serializer.initial_data['address']
        points_coordinates = calculate_coord_from_address(address)

        # Checking if we have some reasonable data
        if points_coordinates:
            serializer.save(location=points_coordinates)
        else:
            # if not then just skipping adding location
            serializer.save()

    def get_queryset(self):
        # Calculation distance between points.
        qs = super().get_queryset()
        latitude = self.request.query_params.get('lat', None)
        longitude = self.request.query_params.get('lng', None)

        if latitude and longitude:
            pnt = GEOSGeometry(f'POINT({latitude} {longitude})', srid=4326)
            qs = qs.annotate(
                distance=Distance('location', pnt)
                ).order_by('distance')
        return qs


class SingleRestaurantView(generics.RetrieveUpdateAPIView):
    '''

    TODO: add user to model
    '''
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializers

    def perform_update(self, serializer):
        # Saving additional points to db
        address = serializer.initial_data['address']
        points_coordinates = calculate_coord_from_address(address)

        # Checking if we have some reasonable data
        if points_coordinates:
            serializer.save(location=points_coordinates)
        else:
            # if not then just skipping adding location
            serializer.save()
