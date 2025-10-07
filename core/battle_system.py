from typing import Tuple
import random
from .player import Player
from .enemy import Enemy

class BattleSystem:
    def __init__(self, player: Player, enemy: Enemy):
        self.player = player
        self.enemy = enemy
        self.log = []
        self.battle_over = False

    def compute_damage(self, attacker_attack, target_defense, power=0) -> int:
        base = attacker_attack + power
        dmg = max(1, base - target_defense + random.randint(-2, 2))
        return dmg

    def player_use_skill(self, skill_index: int) -> Tuple[str, bool]:
        if self.battle_over:
            return "Battle is already over!", False

        if skill_index < 0 or skill_index >= len(self.player.skills):
            return "Invalid skill.", False

        skill = self.player.skills[skill_index]
        if self.player.mp < skill.mp_cost:
            return "Not enough MP!", False

        self.player.mp -= skill.mp_cost
        if skill.type == "attack":
            dmg = self.compute_damage(self.player.attack, self.enemy.defense, power=skill.power)
            self.enemy.hp -= dmg
            self.log.append(f"{self.player.name} used {skill.name} and dealt {dmg} damage.")

            # Check if enemy is defeated
            if self.enemy.hp <= 0:
                self.battle_over = True
                self.log.append(f"{self.enemy.name} is defeated!")

        elif skill.type == "heal":
            heal = skill.power
            self.player.hp = min(self.player.max_hp, self.player.hp + heal)
            self.log.append(f"{self.player.name} used {skill.name} and healed {heal} HP.")
        elif skill.type == "defense":
            # temporary small buff implemented as heal to simplify
            buff = skill.power
            self.player.defense += buff
            self.log.append(f"{self.player.name} used {skill.name} and increased defense by {buff}.")
        return "OK", True

    def player_use_item(self, item_id: str) -> Tuple[str, bool]:
        """Player uses an item during battle"""
        if self.battle_over:
            return "Battle is already over!", False
            
        success, message = self.player.use_item(item_id)
        if success:
            self.log.append(f"{self.player.name} {message}")
            return message, True
        else:
            return message, False

    def enemy_turn(self):
        if self.battle_over or self.enemy.hp <= 0:
            return

        dmg = self.compute_damage(self.enemy.attack, self.player.defense)
        self.player.hp -= dmg
        self.log.append(f"{self.enemy.name} attacked and dealt {dmg} damage.")

        # Check if player is defeated
        if self.player.hp <= 0:
            self.battle_over = True
            self.log.append(f"{self.player.name} is defeated!")

    def is_over(self):
        return self.battle_over or self.player.hp <= 0 or self.enemy.hp <= 0

    def get_result(self):
        if self.player.hp <= 0:
            return "lose"
        if self.enemy.hp <= 0:
            # rewards
            self.player.gain_exp(self.enemy.exp_reward)
            self.player.gold += self.enemy.gold_reward
            return "win"
        return "ongoing"