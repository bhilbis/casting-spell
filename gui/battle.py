# import customtkinter as ctk
# from core.battle_system import BattleSystem
# from core.enemy import Enemy

# class BattleFrame(ctk.CTkFrame):
#     def __init__(self, master, player, enemy: Enemy, app):
#         super().__init__(master)
#         self.player = player
#         self.enemy = enemy
#         self.app = app
#         self.bs = BattleSystem(player, enemy)

#         self.left = ctk.CTkFrame(self)
#         self.left.pack(side="left", fill="y", padx=8, pady=8)
#         self.right = ctk.CTkFrame(self)
#         self.right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

#         self.lbl_player = ctk.CTkLabel(self.left, text=f"{player.name}\nHP:{player.hp}/{player.max_hp}\nMP:{player.mp}/{player.max_mp}")
#         self.lbl_player.pack(pady=6)
#         self.lbl_enemy = ctk.CTkLabel(self.left, text=f"{enemy.name}\nHP:{enemy.hp}")
#         self.lbl_enemy.pack(pady=6)

#         self.log = ctk.CTkTextbox(self.right, height=300, state="disabled")
#         self.log.pack(fill="both", expand=True, padx=6, pady=6)

#         # skill buttons
#         self.skill_frame = ctk.CTkFrame(self.right)
#         self.skill_frame.pack(fill="x", padx=6, pady=6)
#         self.update_skill_buttons()

#         # end / flee
#         self.btn_flee = ctk.CTkButton(self.left, text="Flee", command=self.flee)
#         self.btn_flee.pack(pady=8)

#         self.refresh_ui()

#     def update_skill_buttons(self):
#         for w in self.skill_frame.winfo_children():
#             w.destroy()
#         if not self.player.skills:
#             lbl = ctk.CTkLabel(self.skill_frame, text="No skills learned. Buy at shop/learn first.")
#             lbl.pack()
#             return
#         for idx, s in enumerate(self.player.skills):
#             b = ctk.CTkButton(self.skill_frame, text=f"{s.name} ({s.type})", command=lambda i=idx: self.use_skill(i))
#             b.pack(side="left", padx=6, pady=4)

#     def append_log(self, text: str):
#         self.log.configure(state="normal")
#         self.log.insert("end", text + "\n")
#         self.log.configure(state="disabled")
#         self.log.see("end")

#     def use_skill(self, idx: int):
#         res, ok = self.bs.player_use_skill(idx)
#         if ok:
#             self.append_log(self.bs.log[-1])
#             # enemy turn if alive
#             if self.enemy.hp > 0:
#                 self.bs.enemy_turn()
#                 self.append_log(self.bs.log[-1])
#             self.refresh_ui()
#             if self.bs.is_over():
#                 result = self.bs.get_result()
#                 if result == "win":
#                     self.append_log(f"You defeated {self.enemy.name}! +{self.enemy.exp_reward} EXP +{self.enemy.gold_reward} Gold")
#                 else:
#                     self.append_log("You were defeated... Return to main menu.")
#                 # After battle, return to main app area
#                 self.after(1200, self.app.open_explore)
#         else:
#             self.append_log(res)

#     def refresh_ui(self):
#         self.lbl_player.configure(text=f"{self.player.name}\nHP:{max(0,self.player.hp)}/{self.player.max_hp}\nMP:{self.player.mp}/{self.player.max_mp}")
#         self.lbl_enemy.configure(text=f"{self.enemy.name}\nHP:{max(0,self.enemy.hp)}")
#         self.update_skill_buttons()

#     def flee(self):
#         import random
#         if random.random() < 0.5:
#             self.append_log("Flee successful!")
#             self.app.open_explore()
#         else:
#             self.append_log("Flee failed! Enemy attacks.")
#             self.bs.enemy_turn()
#             self.append_log(self.bs.log[-1])
#             self.refresh_ui()
#             if self.bs.is_over():
#                 result = self.bs.get_result()
#                 if result == "lose":
#                     self.append_log("You were defeated while fleeing.")
#                     self.after(1000, self.app.open_explore)

import customtkinter as ctk
from core.battle_system import BattleSystem
from core.enemy import Enemy

class BattleFrame(ctk.CTkFrame):
    def __init__(self, master, player, enemy: Enemy, app):
        super().__init__(master, fg_color="transparent")
        self.player = player
        self.enemy = enemy
        self.app = app
        self.bs = BattleSystem(player, enemy)
        self.battle_over = False
        
        self.setup_ui()
        self.refresh_ui()
        
        # Initial battle message
        self.append_log(f"⚔️ Battle started! {self.enemy.name} appears!", "danger")

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.battle_title = ctk.CTkLabel(
            header_frame,
            text="⚔️ BATTLE",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FF6B6B"
        )
        self.battle_title.pack()
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Combatants
        combatants_frame = ctk.CTkFrame(content_frame, width=300)
        combatants_frame.pack(side="left", fill="y", padx=(0, 15))
        combatants_frame.pack_propagate(False)
        
        # Player info
        player_frame = ctk.CTkFrame(combatants_frame, border_width=2, border_color="#3E7BFA")
        player_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            player_frame, 
            text="🎯 PLAYER", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))
        
        self.lbl_player = ctk.CTkLabel(
            player_frame,
            text="",
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        self.lbl_player.pack(pady=5, padx=10)
        
        # Player HP bar
        self.player_hp_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
        self.player_hp_frame.pack(fill="x", padx=10, pady=5)
        
        self.player_hp_label = ctk.CTkLabel(
            self.player_hp_frame, 
            text="HP:", 
            font=ctk.CTkFont(size=12)
        )
        self.player_hp_label.pack(anchor="w")
        
        self.player_hp_bar = ctk.CTkProgressBar(self.player_hp_frame, height=12)
        self.player_hp_bar.pack(fill="x", pady=2)
        self.player_hp_bar.set(1.0)
        
        # Player MP bar
        self.player_mp_frame = ctk.CTkFrame(player_frame, fg_color="transparent")
        self.player_mp_frame.pack(fill="x", padx=10, pady=5)
        
        self.player_mp_label = ctk.CTkLabel(
            self.player_mp_frame, 
            text="MP:", 
            font=ctk.CTkFont(size=12)
        )
        self.player_mp_label.pack(anchor="w")
        
        self.player_mp_bar = ctk.CTkProgressBar(self.player_mp_frame, height=12)
        self.player_mp_bar.pack(fill="x", pady=2)
        self.player_mp_bar.set(1.0)
        
        # Enemy info
        enemy_frame = ctk.CTkFrame(combatants_frame, border_width=2, border_color="#FF6B6B")
        enemy_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            enemy_frame, 
            text="👹 ENEMY", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(10, 5))
        
        self.lbl_enemy = ctk.CTkLabel(
            enemy_frame,
            text="",
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        self.lbl_enemy.pack(pady=5, padx=10)
        
        # Enemy HP bar
        self.enemy_hp_frame = ctk.CTkFrame(enemy_frame, fg_color="transparent")
        self.enemy_hp_frame.pack(fill="x", padx=10, pady=5)
        
        self.enemy_hp_label = ctk.CTkLabel(
            self.enemy_hp_frame, 
            text="HP:", 
            font=ctk.CTkFont(size=12)
        )
        self.enemy_hp_label.pack(anchor="w")
        
        self.enemy_hp_bar = ctk.CTkProgressBar(self.enemy_hp_frame, height=12)
        self.enemy_hp_bar.pack(fill="x", pady=2)
        self.enemy_hp_bar.set(1.0)
        
        # Battle actions frame
        actions_frame = ctk.CTkFrame(combatants_frame)
        actions_frame.pack(fill="x", padx=10, pady=10)
        
        self.btn_flee = ctk.CTkButton(
            actions_frame,
            text="🏃‍♂️ Flee Battle",
            command=self.flee,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#FF8C00",
            hover_color="#FFA500"
        )
        self.btn_flee.pack(fill="x", pady=5)
        
        # Right panel - Battle log and skills
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Battle log
        log_frame = ctk.CTkFrame(right_frame)
        log_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        ctk.CTkLabel(
            log_frame, 
            text="📜 BATTLE LOG", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.log = ctk.CTkTextbox(
            log_frame, 
            height=200,
            state="disabled",
            font=ctk.CTkFont(size=13)
        )
        self.log.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Skills section
        skills_frame = ctk.CTkFrame(right_frame)
        skills_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            skills_frame, 
            text="🎯 BATTLE ACTIONS", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.skill_container = ctk.CTkScrollableFrame(skills_frame, height=120)
        self.skill_container.pack(fill="both", padx=10, pady=(0, 10))
        
        # Status frame
        self.status_frame = ctk.CTkFrame(self, height=40)
        self.status_frame.pack(fill="x", padx=20, pady=(5, 10))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Select an action to continue...",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        self.status_label.pack(side="left", padx=10)
        items_frame = ctk.CTkFrame(right_frame)
        items_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(
            items_frame, 
            text="🎒 ITEMS", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=10)
        
        self.items_container = ctk.CTkScrollableFrame(items_frame, height=80)
        self.items_container.pack(fill="both", padx=10, pady=(0, 10))

    def update_skill_buttons(self):
        """Update the skill buttons container"""
        for widget in self.skill_container.winfo_children():
            widget.destroy()
            
        if self.battle_over:
            return
            
        if not self.player.skills:
            lbl = ctk.CTkLabel(
                self.skill_container, 
                text="No skills available. Use basic attack.",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray70")
            )
            lbl.pack(pady=10)
            return
            
        # Create skill buttons in a grid-like layout
        for idx, skill in enumerate(self.player.skills):
            skill_btn = ctk.CTkButton(
                self.skill_container,
                text=f"{skill.name}\nMP: {getattr(skill, 'mp_cost', 0)}",
                command=lambda i=idx: self.use_skill(i),
                height=50,
                font=ctk.CTkFont(size=12),
                fg_color="#2B5B84",
                hover_color="#1E3F5C"
            )
            skill_btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)
            
        # Add basic attack button
        basic_attack_btn = ctk.CTkButton(
            self.skill_container,
            text="Basic Attack\nNo Cost",
            command=self.use_basic_attack,
            height=50,
            font=ctk.CTkFont(size=12),
            fg_color="#2E8B57",
            hover_color="#3CB371"
        )
        basic_attack_btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def update_item_buttons(self):
        """Update the item buttons container"""
        for widget in self.items_container.winfo_children():
            widget.destroy()
            
        if self.battle_over:
            return
            
        available_items = self.player.get_available_items()
        
        if not available_items:
            lbl = ctk.CTkLabel(
                self.items_container, 
                text="No items available",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray70")
            )
            lbl.pack(pady=10)
            return
            
        # Create item buttons
        for item_id in available_items:
            item_name = self.get_item_display_name(item_id)
            qty = self.player.inventory[item_id]
            
            item_btn = ctk.CTkButton(
                self.items_container,
                text=f"{item_name}\nQty: {qty}",
                command=lambda i=item_id: self.use_item(i),
                height=40,
                font=ctk.CTkFont(size=11),
                fg_color="#8B4513",
                hover_color="#A0522D"
            )
            item_btn.pack(side="left", padx=5, pady=5, fill="x", expand=True)

    def get_item_display_name(self, item_id: str) -> str:
        """Get display name for items"""
        item_names = {
            "p_hp_small": "HP Potion",
            "p_mp_small": "MP Potion", 
            "p_hp_medium": "Big HP Potion",
            "p_mp_medium": "Big MP Potion",
            "p_elixir": "Elixir"
        }
        return item_names.get(item_id, item_id)

    def use_item(self, item_id: str):
        """Use item during battle"""
        if self.battle_over:
            return
            
        res, ok = self.bs.player_use_item(item_id)
        if ok:
            self.append_log(self.bs.log[-1], "success")
            self.refresh_ui()
            
            # Enemy turn only if battle continues
            if not self.bs.is_over():
                self.after(800, self.enemy_turn)
            else:
                self.end_battle()
        else:
            self.append_log(res, "warning")
    
    def append_log(self, text: str, log_type="info"):
        """Append text to battle log"""
        self.log.configure(state="normal")
        
        # Add simple formatting since CTkTextbox doesn't support tags
        prefix = ""
        if log_type == "danger":
            prefix = "💀 "
        elif log_type == "success":
            prefix = "✅ "
        elif log_type == "warning":
            prefix = "⚠️ "
        elif log_type == "info":
            prefix = "ℹ️ "
            
        self.log.insert("end", f"{prefix}{text}\n")
        self.log.configure(state="disabled")
        self.log.see("end")

    def use_basic_attack(self):
        """Use basic attack when no skills or MP"""
        if self.battle_over:
            return
            
        res, ok = self.bs.player_use_basic_attack()
        if ok:
            self.append_log(self.bs.log[-1], "info")
            self.after(800, self.enemy_turn)
        else:
            self.append_log(res, "warning")
            
        self.refresh_ui()

    def use_skill(self, idx: int):
        """Use selected skill"""
        if self.battle_over:
            return
            
        skill = self.player.skills[idx]
        mp_cost = getattr(skill, 'mp_cost', 0)
        
        if self.player.mp < mp_cost:
            self.append_log(f"Not enough MP to use {skill.name}! Need {mp_cost}, have {self.player.mp}.", "warning")
            return
            
        res, ok = self.bs.player_use_skill(idx)
        if ok:
            self.append_log(self.bs.log[-1], "info")
            self.refresh_ui()

            if self.bs.is_over():
                self.end_battle()
            else:
            # Enemy turn only if battle continues
                self.after(800, self.enemy_turn)
        else:
            self.append_log(res, "warning")

    def enemy_turn(self):
        """Process enemy turn"""
        if self.battle_over or self.enemy.hp <= 0:
            return
            
        self.bs.enemy_turn()
        self.append_log(self.bs.log[-1], "danger")
        self.refresh_ui()
        
        if self.bs.is_over():
            self.end_battle()

    def end_battle(self):
        """Handle battle end"""
        self.battle_over = True
        result = self.bs.get_result()
        
        if result == "win":
            self.append_log(f"🎉 Victory! You defeated {self.enemy.name}!", "success")
            self.append_log(f"💰 Gained {self.enemy.gold_reward} Gold and {self.enemy.exp_reward} EXP!", "success")
            # Update player stats
            self.player.gold += self.enemy.gold_reward
            # Add exp logic here if you have it
        else:
            self.append_log("💀 Defeat! You were overwhelmed...", "danger")
            
        self.status_label.configure(text="Battle ended. Returning to exploration...")
        self.btn_flee.configure(state="disabled")
        self.update_skill_buttons()  # This will clear skill buttons
        
        # Return to explore after delay
        self.after(2500, self.app.open_explore)

    def refresh_ui(self):
        """Update all UI elements"""
        # Player info
        self.lbl_player.configure(
            text=f"{self.player.name}\n"
                 f"Lvl: {self.player.level}\n"
                 f"Role: {self.player.role}"
        )
        
        # Enemy info - using safe attribute access
        enemy_level = getattr(self.enemy, 'level', '?')
        enemy_type = getattr(self.enemy, 'type', 'Unknown')
        enemy_max_hp = getattr(self.enemy, 'max_hp', self.enemy.hp)  # Fallback to current hp if max_hp not available
        
        self.lbl_enemy.configure(
            text=f"{self.enemy.name}\n"
                 f"Lvl: {enemy_level}\n"
                 f"Type: {enemy_type}"
        )
        
        # HP/MP bars
        player_hp_ratio = max(0, self.player.hp) / self.player.max_hp
        self.player_hp_bar.set(player_hp_ratio)
        self.player_hp_label.configure(text=f"HP: {max(0, self.player.hp)}/{self.player.max_hp}")
        
        player_mp_ratio = self.player.mp / self.player.max_mp if self.player.max_mp > 0 else 0
        self.player_mp_bar.set(player_mp_ratio)
        self.player_mp_label.configure(text=f"MP: {self.player.mp}/{self.player.max_mp}")
        
        enemy_hp_ratio = max(0, self.enemy.hp) / enemy_max_hp
        self.enemy_hp_bar.set(enemy_hp_ratio)
        self.enemy_hp_label.configure(text=f"HP: {max(0, self.enemy.hp)}/{enemy_max_hp}")
        
        # Update skill buttons
        self.update_skill_buttons()
        # Update item buttons
        self.update_item_buttons()
        
        # Update status
        if not self.battle_over:
            if self.enemy.hp <= 0:
                self.status_label.configure(text="Enemy defeated! Finalizing battle...")
            elif self.player.hp <= 0:
                self.status_label.configure(text="You have been defeated...")
            else:
                self.status_label.configure(text="Select your next action...")

    def flee(self):
        """Attempt to flee from battle"""
        if self.battle_over:
            return
            
        import random
        self.append_log("Attempting to flee...", "warning")
        
        if random.random() < 0.6:  # 60% success chance
            self.append_log("✅ Successfully fled from battle!", "success")
            self.battle_over = True
            self.status_label.configure(text="Fled successfully. Returning to exploration...")
            self.after(1500, self.app.open_explore)
        else:
            self.append_log("❌ Flee failed! Enemy attacks!", "danger")
            self.bs.enemy_turn()
            self.append_log(self.bs.log[-1], "danger")
            self.refresh_ui()
            
            if self.bs.is_over():
                self.end_battle()