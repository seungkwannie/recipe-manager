from dataclasses import dataclass
from typing import List

@dataclass
class Recipe:
    id: int
    name: str
    ingredients: List[str]
    instructions: List[str]
    servings: int

    # The __init__ (constructor) is created automatically by @dataclass