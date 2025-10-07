from dataclasses import dataclass

@dataclass
class Item:
    id: str
    name: str
    description: str
    effect: dict # e.g. {"hp": +50} or {"attack": +5}
    price: int