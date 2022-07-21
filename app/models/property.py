from dataclasses import dataclass
from typing import List


@dataclass
class Property:
    """Class that models a Property in the database"""

    id: int
    name: str
    status: str
    year: int
    state: str
    city: str
    address: str
    price: int
    description: str

    def __init__(
        self,
        id: int,
        name: str,
        status: str,
        year: int,
        state: str,
        city: str,
        address: str,
        price: int,
        description: str,
    ) -> "Property":
        self.id = id
        self.name = name
        self.status = status
        self.year = year
        self.state = state
        self.city = city
        self.address = address
        self.price = price
        self.description = description
