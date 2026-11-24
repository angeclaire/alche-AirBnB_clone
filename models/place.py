#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """Represent a place that can be rented.

    Attributes:
        city_id (str): The id of the City the place is in.
        user_id (str): The id of the User who owns the place.
        name (str): The name of the place.
        description (str): A description of the place.
        number_rooms (int): Number of rooms.
        number_bathrooms (int): Number of bathrooms.
        max_guest (int): Maximum number of guests.
        price_by_night (int): Price for one night.
        latitude (float): Latitude of the place.
        longitude (float): Longitude of the place.
        amenity_ids (list): Ids of the Amenity objects the place offers.
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
