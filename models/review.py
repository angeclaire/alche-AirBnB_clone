#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Represent a review.

    Attributes:
        place_id (str): The id of the Place being reviewed.
        user_id (str): The id of the User who wrote the review.
        text (str): The content of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
