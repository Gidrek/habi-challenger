from dataclasses import dataclass
from typing import List


@dataclass
class Property:
    """Class that models a Property in the database"""

    address: str
    city: str
    price: int
    description: str
    year: int

    def __init__(
        self,
        address: str,
        city: str,
        price: int,
        description: str,
        year: int,
    ) -> "Property":
        self.year = year
        self.city = city
        self.address = address
        self.price = price
        self.description = description
