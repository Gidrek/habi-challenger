from dataclasses import dataclass
from typing import List


@dataclass
class Property:
    """Class that models a Property in the database"""

    id: int
    address: str
    city: str
    price: int
    description: str
    year: int

    def __init__(
        self,
        id: int,
        address: str,
        city: str,
        price: int,
        description: str,
        year: int,
    ) -> "Property":
        self.id = id
        self.year = year
        self.city = city
        self.address = address
        self.price = price
        self.description = description
