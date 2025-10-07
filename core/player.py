import json
from typing import List
from .skill import Skill, skill_from_dict
from core import skill

class Player:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.level = 1
        self.exp = 0
        self.gold = 150 # starting gold
        # depend on role
        base = {
            "Warrior": {"max_hp": 120, "max_mp": 20, "attack": 12, "defense": 8, "speed": 6},
            "Mage": {"max_hp": 70, "max_mp": 100, "attack": 6, "defense": 4, "speed": 8},
            "Archer": {"max_hp": 90, "max_mp": 40, "attack": 10, "defense": 5, "speed": 10},
        }.get(role, {"max_hp": 80, "max_mp": 30, "attack": 8, "defense": 5, "speed": 7})

        self.max_hp = base["max_hp"]
        self.hp = self.max_hp
        self.max_mp = base["max_mp"]
        self.mp = self.max_mp
        self.attack = base["attack"]
        self.defense = base["defense"]
        self.speed = base["speed"]

        self.skills: List[Skill] = [] # learned skills (must buy first skill)
        self.inventory = {} # item_id -> qty

    def learn_skill(self, skill: Skill) -> bool:
        if self.gold >= skill.cost:
            self.gold -= skill.cost
            self.skills.append(skill)
            return True
        return False
    
    def gain_exp(self, amount: int):
        self.exp += amount
        while self.exp >= self.required_exp():
            self.exp -= self.required_exp()
            self.level_up()

    def required_exp(self):
        return 50 + (self.level - 1) * 25

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.max_mp += 5
        self.attack += 2
        self.defense += 1
        self.hp = self.max_hp
        self.mp = self.max_mp

    def use_item(self, item_id: str) -> tuple[bool, str]:
        """Use an item from inventory"""
        if item_id not in self.inventory or self.inventory[item_id] <= 0:
            return False, "Item not found in inventory"
        
        # Define item effects
        item_effects = {
            "p_hp_small": {"hp": 30},
            "p_mp_small": {"mp": 20},
            "p_hp_medium": {"hp": 60},
            "p_mp_medium": {"mp": 40},
            "p_elixir": {"hp": 50, "mp": 30}
        }
        
        if item_id not in item_effects:
            return False, "Unknown item"
        
        effect = item_effects[item_id]
        message_parts = []
        
        # Apply HP effect
        if "hp" in effect:
            heal_amount = effect["hp"]
            old_hp = self.hp
            self.hp = min(self.max_hp, self.hp + heal_amount)
            actual_heal = self.hp - old_hp
            if actual_heal > 0:
                message_parts.append(f"healed {actual_heal} HP")
        
        # Apply MP effect
        if "mp" in effect:
            restore_amount = effect["mp"]
            old_mp = self.mp
            self.mp = min(self.max_mp, self.mp + restore_amount)
            actual_restore = self.mp - old_mp
            if actual_restore > 0:
                message_parts.append(f"restored {actual_restore} MP")
        
        # Remove item from inventory
        self.inventory[item_id] -= 1
        if self.inventory[item_id] <= 0:
            del self.inventory[item_id]
        
        if message_parts:
            return True, f"Used {item_id}: " + " and ".join(message_parts)
        else:
            return True, f"Used {item_id} (no effect - already at max)"

    def get_available_items(self) -> List[str]:
        """Get list of item IDs that player has in inventory"""
        return [item_id for item_id, qty in self.inventory.items() if qty > 0]

    def rest(self):
        """Rest to recover HP and MP"""
        hp_recovered = min(20, self.max_hp - self.hp)
        mp_recovered = min(15, self.max_mp - self.mp)
        
        self.hp += hp_recovered
        self.mp += mp_recovered
        
        return hp_recovered, mp_recovered

    def to_dict(self):
        return {
            "name": self.name, "role": self.role, "level": self.level,
            "exp": self.exp, "gold": self.gold,
            "hp": self.hp, "max_hp": self.max_hp,
            "mp": self.mp, "max_mp": self.max_mp,
            "attack": self.attack, "defense": self.defense, "speed": self.speed,
            "skills": [s.to_dict() for s in self.skills],
            "inventory": self.inventory
        }

    @staticmethod
    def from_dict(d: dict):
        p = Player(d["name"], d["role"])
        p.level = d.get("level", 1)
        p.exp = d.get("exp", 0)
        p.gold = d.get("gold", 0)
        p.hp = d.get("hp", p.max_hp)
        p.max_hp = d.get("max_hp", p.max_hp)
        p.mp = d.get("mp", p.max_mp)
        p.max_mp = d.get("max_mp", p.max_mp)
        p.attack = d.get("attack", p.attack)
        p.defense = d.get("defense", p.defense)
        p.speed = d.get("speed", p.speed)
        p.skills = [skill_from_dict(s) for s in d.get("skills", [])]
        p.inventory = d.get("inventory", {})
        return p