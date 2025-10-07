# from dataclasses import dataclass
# import random

# @dataclass
# class Enemy:
#     id: str
#     name: str
#     hp: int
#     attack: int
#     defense: int
#     speed: int
#     exp_reward: int
#     gold_reward: int

# def random_enemy_for_level(level: int) -> Enemy:
#     # simple random enemy generator scaled by level
#     base_hp = 30 + level * 10
#     return Enemy(
#         id=f"gob_{random.randint(100,999)}",
#         name=random.choice(["Goblin", "Wolf", "Bandit", "Skeleton"]),
#         hp=base_hp,
#         attack=5 + level * 2,
#         defense=2 + level,
#         speed=4 + level,
#         exp_reward=10 + level * 5,
#         gold_reward=10 + level * 5
#     )

from dataclasses import dataclass
import random
from typing import List, Dict

@dataclass
class Enemy:
    id: str
    name: str
    hp: int
    attack: int
    defense: int
    speed: int
    exp_reward: int
    gold_reward: int
    # New modern attributes (backward compatible)
    level: int = 1
    enemy_type: str = "normal"
    max_hp: int = None
    description: str = ""
    rarity: str = "common"
    
    def __post_init__(self):
        # Set max_hp to hp if not provided (for backward compatibility)
        if self.max_hp is None:
            self.max_hp = self.hp
        
        # Set level based on stats if not provided
        if not hasattr(self, 'level') or self.level == 1:
            self.level = max(1, (self.attack - 5) // 2)
    
    # Modern methods (optional usage)
    def take_damage(self, damage: int) -> int:
        """Apply damage to enemy with defense calculation"""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage
    
    def is_alive(self) -> bool:
        return self.hp > 0
    
    def get_health_percentage(self) -> float:
        return self.hp / self.max_hp if self.max_hp > 0 else 0
    
    def get_attack_variation(self) -> int:
        """Return attack with random variation (±20%)"""
        variation = random.uniform(0.8, 1.2)
        return max(1, int(self.attack * variation))

# Enemy templates for better variety
ENEMY_TEMPLATES = {
    "goblin": {
        "name": "Goblin",
        "base_hp": 25,
        "base_attack": 4,
        "base_defense": 1,
        "base_speed": 6,
        "exp_multiplier": 8,
        "gold_multiplier": 8,
        "type": "humanoid"
    },
    "wolf": {
        "name": "Wolf", 
        "base_hp": 20,
        "base_attack": 6,
        "base_defense": 0,
        "base_speed": 8,
        "exp_multiplier": 7,
        "gold_multiplier": 5,
        "type": "beast"
    },
    "bandit": {
        "name": "Bandit",
        "base_hp": 30,
        "base_attack": 5,
        "base_defense": 2,
        "base_speed": 5,
        "exp_multiplier": 10,
        "gold_multiplier": 12,
        "type": "humanoid"
    },
    "skeleton": {
        "name": "Skeleton",
        "base_hp": 22,
        "base_attack": 5,
        "base_defense": 3,
        "base_speed": 4,
        "exp_multiplier": 9,
        "gold_multiplier": 6,
        "type": "undead"
    },
    "slime": {
        "name": "Slime",
        "base_hp": 35,
        "base_attack": 3,
        "base_defense": 4,
        "base_speed": 3,
        "exp_multiplier": 6,
        "gold_multiplier": 4,
        "type": "elemental"
    },
    "spider": {
        "name": "Giant Spider",
        "base_hp": 28,
        "base_attack": 7,
        "base_defense": 1,
        "base_speed": 7,
        "exp_multiplier": 11,
        "gold_multiplier": 7,
        "type": "beast"
    }
}

def random_enemy_for_level(level: int) -> Enemy:
    """Generate random enemy scaled by level with modern game design"""
    # Choose random template
    template_key = random.choice(list(ENEMY_TEMPLATES.keys()))
    template = ENEMY_TEMPLATES[template_key]
    
    # Scale stats by level with some randomness
    hp_variation = random.uniform(0.8, 1.2)
    attack_variation = random.uniform(0.9, 1.1)
    defense_variation = random.uniform(0.8, 1.2)
    
    base_hp = template["base_hp"]
    base_attack = template["base_attack"] 
    base_defense = template["base_defense"]
    base_speed = template["base_speed"]
    
    # Scale stats with level
    scaled_hp = int(base_hp + (level * 8 * hp_variation))
    scaled_attack = int(base_attack + (level * 1.5 * attack_variation))
    scaled_defense = int(base_defense + (level * 0.8 * defense_variation))
    scaled_speed = base_speed + level
    
    # Rewards scale with level and template multipliers
    exp_reward = int(template["exp_multiplier"] + (level * 4))
    gold_reward = int(template["gold_multiplier"] + (level * 3))
    
    # Add rarity system (common, uncommon, rare)
    rarity_roll = random.random()
    if rarity_roll < 0.05:  # 5% chance for rare
        rarity = "rare"
        # Boost stats for rare enemies
        scaled_hp = int(scaled_hp * 1.3)
        scaled_attack = int(scaled_attack * 1.2)
        exp_reward = int(exp_reward * 1.5)
        gold_reward = int(gold_reward * 2.0)
    elif rarity_roll < 0.20:  # 15% chance for uncommon
        rarity = "uncommon"
        scaled_hp = int(scaled_hp * 1.1)
        scaled_attack = int(scaled_attack * 1.1)
        exp_reward = int(exp_reward * 1.2)
        gold_reward = int(gold_reward * 1.3)
    else:  # 80% chance for common
        rarity = "common"
    
    # Create enemy name with potential prefix based on rarity
    enemy_name = template["name"]
    if rarity == "uncommon":
        prefixes = ["Tough", "Angry", "Wild", "Aggressive"]
        enemy_name = f"{random.choice(prefixes)} {enemy_name}"
    elif rarity == "rare":
        prefixes = ["Elite", "Alpha", "Vicious", "Deadly"]
        enemy_name = f"{random.choice(prefixes)} {enemy_name}"
    
    return Enemy(
        id=f"{template_key}_{random.randint(1000, 9999)}",
        name=enemy_name,
        hp=scaled_hp,
        max_hp=scaled_hp,
        attack=scaled_attack,
        defense=scaled_defense,
        speed=scaled_speed,
        exp_reward=exp_reward,
        gold_reward=gold_reward,
        level=level,
        enemy_type=template["type"],
        rarity=rarity,
        description=f"A {rarity} {template['name'].lower()} that roams the area."
    )

def get_enemy_difficulty_rating(enemy: Enemy) -> str:
    """Get a descriptive difficulty rating for the enemy"""
    power_level = (enemy.attack + enemy.defense + enemy.hp // 10) / 3
    
    if power_level < 5:
        return "Very Easy"
    elif power_level < 10:
        return "Easy"
    elif power_level < 15:
        return "Medium"
    elif power_level < 20:
        return "Hard"
    else:
        return "Very Hard"

# Additional utility function for battle system
def create_boss_enemy(level: int) -> Enemy:
    """Create a special boss enemy"""
    boss_template = random.choice(["bandit", "skeleton"])  # Boss-capable templates
    template = ENEMY_TEMPLATES[boss_template]
    
    # Bosses are significantly stronger
    scaled_hp = int(template["base_hp"] + (level * 15))
    scaled_attack = int(template["base_attack"] + (level * 3))
    scaled_defense = int(template["base_defense"] + (level * 2))
    
    boss = Enemy(
        id=f"boss_{random.randint(1000, 9999)}",
        name=f"{template['name']} Chieftain",
        hp=scaled_hp,
        max_hp=scaled_hp,
        attack=scaled_attack,
        defense=scaled_defense,
        speed=template["base_speed"] + level,
        exp_reward=int((template["exp_multiplier"] + (level * 4)) * 3),
        gold_reward=int((template["gold_multiplier"] + (level * 3)) * 4),
        level=level,
        enemy_type=template["type"],
        rarity="boss",
        description=f"A powerful {template['name'].lower()} leader with enhanced abilities."
    )
    
    return boss