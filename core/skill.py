from dataclasses import dataclass
from typing import Dict

@dataclass
class Skill:
    id: str
    name: str
    type: str # "attack", "heal", "defense"
    power: int
    cost: int # gold price to learn
    mp_cost: int

    def to_dict(self) -> Dict:
        return {
            "id": self.id, "name": self.name, "type": self.type,
            "power": self.power, "cost": self.cost, "mp_cost": self.mp_cost
        }

def skill_from_dict(d: Dict) -> Skill:
    return Skill(
        id=d["id"], name=d["name"], type=d["type"],
        power=d["power"], cost=d["cost"], mp_cost=d.get("mp_cost", 0)
    )
