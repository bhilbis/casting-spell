# import customtkinter as ctk
# import random
# from core.enemy import random_enemy_for_level

# class ExploreFrame(ctk.CTkFrame):
#     def __init__(self, master, player, app):
#         super().__init__(master)
#         self.player = player
#         self.app = app
#         self.pack_propagate(False)

#         self.lbl = ctk.CTkLabel(self, text="Explore - Find enemies and fight!")
#         self.lbl.pack(pady=8)

#         self.btn_walk = ctk.CTkButton(self, text="Walk (Random Encounter)", command=self.walk)
#         self.btn_walk.pack(pady=8)

#         self.log_box = ctk.CTkTextbox(self, height=300, state="disabled")
#         self.log_box.pack(fill="both", padx=10, pady=8, expand=True)

#         self.update_status()

#     def append_log(self, text: str):
#         self.log_box.configure(state="normal")
#         self.log_box.insert("end", text + "\n")
#         self.log_box.configure(state="disabled")
#         self.log_box.see("end")

#     def update_status(self):
#         self.lbl.configure(text=f"Exploring as {self.player.name} (Lvl {self.player.level}) - Gold: {self.player.gold}")

#     def walk(self):
#         # chance of encounter
#         if random.random() < 0.75:
#             enemy = random_enemy_for_level(self.player.level)
#             self.append_log(f"Encountered {enemy.name} (HP:{enemy.hp})! Opening battle...")
#             # open battle via main app
#             self.app.open_battle(enemy)
#         else:
#             gold = random.randint(1, 8)
#             self.player.gold += gold
#             self.append_log(f"Found {gold} gold wandering around.")
#             self.update_status()

import customtkinter as ctk
import random
from core.enemy import random_enemy_for_level

class ExploreFrame(ctk.CTkFrame):
    def __init__(self, master, player, app):
        super().__init__(master, fg_color="transparent")
        self.player = player
        self.app = app
        
        self.encounter_chance = 0.75
        self.min_gold_find = 1
        self.max_gold_find = 8
        self.exploration_count = 0
        
        self.setup_ui()
        self.update_status()

    def setup_ui(self):
        # Header section
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title and player info
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        self.lbl = ctk.CTkLabel(
            title_frame,
            text="🌲 Wilderness Explorer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl.pack(side="left")
        
        self.stats_label = ctk.CTkLabel(
            title_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70")
        )
        self.stats_label.pack(side="right")
        
        # Exploration progress
        self.progress_frame = ctk.CTkFrame(header_frame, height=8)
        self.progress_frame.pack(fill="x", pady=5)
        self.progress_frame.pack_propagate(False)
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, height=6)
        self.progress_bar.pack(fill="x", padx=2, pady=1)
        self.progress_bar.set(0)
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left panel - Actions
        action_frame = ctk.CTkFrame(content_frame, width=280)
        action_frame.pack(side="left", fill="y", padx=(0, 15))
        action_frame.pack_propagate(False)
        
        # Action buttons
        ctk.CTkLabel(
            action_frame, 
            text="Exploration Actions", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        self.btn_walk = ctk.CTkButton(
            action_frame,
            text="🚶‍♂️ Walk the Path",
            command=self.walk,
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2B5B84",
            hover_color="#1E3F5C"
        )
        self.btn_walk.pack(fill="x", padx=15, pady=8)
        
        self.btn_search = ctk.CTkButton(
            action_frame,
            text="🔍 Search Carefully",
            command=self.search_carefully,
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color="#2B5B84",
            hover_color="#1E3F5C"
        )
        self.btn_search.pack(fill="x", padx=15, pady=8)
        
        self.btn_rest = ctk.CTkButton(
            action_frame,
            text="💤 Rest & Recover",
            command=self.rest,
            height=45,
            font=ctk.CTkFont(size=14),
            fg_color="#2E8B57",
            hover_color="#3CB371"
        )
        self.btn_rest.pack(fill="x", padx=15, pady=8)
        
        # Exploration info
        info_frame = ctk.CTkFrame(action_frame)
        info_frame.pack(fill="x", padx=10, pady=15)
        
        ctk.CTkLabel(
            info_frame, 
            text="Exploration Info", 
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.info_text = ctk.CTkLabel(
            info_frame,
            text=f"• Encounter chance: {self.encounter_chance*100}%\n"
                 f"• Gold find: {self.min_gold_find}-{self.max_gold_find}\n"
                 f"• Area level: {self.player.level}",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.info_text.pack(pady=5, padx=10)
        
        # Right panel - Log
        log_frame = ctk.CTkFrame(content_frame)
        log_frame.pack(side="right", fill="both", expand=True)
        
        # Log header
        log_header = ctk.CTkFrame(log_frame, fg_color="transparent")
        log_header.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            log_header, 
            text="📜 Exploration Log", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        clear_btn = ctk.CTkButton(
            log_header,
            text="Clear Log",
            command=self.clear_log,
            width=80,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        clear_btn.pack(side="right")
        
        # Log content
        self.log_box = ctk.CTkTextbox(
            log_frame, 
            state="disabled",
            font=ctk.CTkFont(size=13, family="Consolas"),
            wrap="word"
        )
        self.log_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Status bar
        self.status_bar = ctk.CTkFrame(self, height=30)
        self.status_bar.pack(fill="x", padx=20, pady=(5, 10))
        self.status_bar.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready to explore...",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        self.status_label.pack(side="left", padx=10)

    def append_log(self, text: str, log_type="info"):
        """Append text to log with colored formatting"""
        colors = {
            "info": ("gray10", "gray90"),
            "success": ("#2E8B57", "#3CB371"),
            "warning": ("#FF8C00", "#FFA500"),
            "danger": ("#DC143C", "#FF6B6B"),
            "gold": ("#B8860B", "#FFD700")
        }
        
        self.log_box.configure(state="normal")
        
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Insert timestamp
        self.log_box.insert("end", f"[{timestamp}] ", "timestamp")
        
        # Insert colored message
        color_code = colors.get(log_type, colors["info"])[1]
        formatted_text = f"[{timestamp}] {text}\n"
        # self.log_box.insert("end", text + "\n", tag_name)
        self.log_box.insert("end", formatted_text, color_code)
        
        self.log_box.configure(state="disabled")
        self.log_box.see("end")
        
        # Update status bar
        self.status_label.configure(text=f"Last action: {text.split('.')[0]}")

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.status_label.configure(text="Log cleared")

    def update_status(self):
        self.lbl.configure(text=f"🌲 Exploring as {self.player.name}")
        self.stats_label.configure(
            text=f"Lvl {self.player.level} | "
                 f"❤️ {self.player.hp}/{self.player.max_hp} | "
                 f"💰 {self.player.gold} Gold"
        )
        
        # Update progress bar based on exploration count
        progress = min(self.exploration_count / 10, 1.0)
        self.progress_bar.set(progress)

    def walk(self):
        """Standard exploration with normal encounter chance"""
        self.exploration_count += 1
        self.append_log("You walk along the forest path...", "info")
        self.animate_exploration()
        
        self.after(1000, self._process_walk_result)

    def search_carefully(self):
        """More thorough search with higher gold chance but lower encounter chance"""
        self.exploration_count += 1
        self.append_log("You carefully search the area...", "info")
        self.animate_exploration()
        
        self.after(1000, self._process_search_result)

    def rest(self):
        """Rest to recover HP"""
        hp_needed = self.player.max_hp - self.player.hp
        mp_needed = self.player.max_mp - self.player.mp

        if hp_needed <= 0 and mp_needed <= 0:
            self.append_log("You are already at full health and mana.", "info")
            return
        
        # Calculate waiting time based on how much needs to be recovered
        # Base time + extra time based on recovery needed
        base_wait_time = 2000  # 2 seconds base
        recovery_factor = (hp_needed / self.player.max_hp) + (mp_needed / self.player.max_mp)
        wait_time = base_wait_time + int(recovery_factor * 3000)  # Up to 3 extra seconds
        
        self.append_log(f"You start resting to recover... ({(wait_time/1000):.1f}s)", "info")
        
        # Disable buttons during rest
        self.btn_walk.configure(state="disabled")
        self.btn_search.configure(state="disabled")
        self.btn_rest.configure(state="disabled")
        
        # Show progress
        self.show_rest_progress(wait_time)

    def show_rest_progress(self, total_time: int):
        """Show progress bar during resting"""
        # Create progress overlay
        self.rest_progress = ctk.CTkProgressBar(self.main_area, height=20)
        self.rest_progress.place(relx=0.5, rely=0.5, anchor="center", width=300)
        self.rest_progress.set(0)
        
        self.rest_label = ctk.CTkLabel(
            self.main_area,
            text="Resting...",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.rest_label.place(relx=0.5, rely=0.6, anchor="center")
        
        # Animate progress
        self.animate_rest_progress(0, total_time)
    
    def animate_rest_progress(self, elapsed: int, total_time: int):
        """Animate the rest progress bar"""
        progress = elapsed / total_time
        self.rest_progress.set(progress)
        
        if elapsed < total_time:
            # Continue animation
            self.after(50, lambda: self.animate_rest_progress(elapsed + 50, total_time))
        else:
            # Resting complete
            self.complete_rest()

    def complete_rest(self):
        """Complete the resting process"""
        # Remove progress elements
        self.rest_progress.destroy()
        self.rest_label.destroy()
        
        # Perform actual rest
        old_hp = self.player.hp
        old_mp = self.player.mp
        
        hp_recovered, mp_recovered = self.player.rest()
        
        if hp_recovered > 0 or mp_recovered > 0:
            message = f"You feel rested and recover {hp_recovered} HP"
            if mp_recovered > 0:
                message += f" and {mp_recovered} MP"
            message += "."
            self.append_log(message, "success")
        else:
            self.append_log("You are already at full health and mana.", "info")
        
        self.update_status()
        self.app.update_info()
        
        # Re-enable buttons
        self.btn_walk.configure(state="normal")
        self.btn_search.configure(state="normal")
        self.btn_rest.configure(state="normal")
    
    def _process_walk_result(self):
        if random.random() < self.encounter_chance:
            enemy = random_enemy_for_level(self.player.level)
            self.append_log(f"⚔️ Wild {enemy.name} appears! (HP: {enemy.hp}, Level: {enemy.level})", "danger")
            self.append_log("Opening battle interface...", "warning")
            self.app.open_battle(enemy)
        else:
            gold = random.randint(self.min_gold_find, self.max_gold_find)
            self.player.gold += gold
            self.append_log(f"💰 Found {gold} gold coins lying on the path!", "gold")
            self.update_status()
            self.app.update_info()

    def _process_search_result(self):
        if random.random() < self.encounter_chance * 0.6:  # 40% lower chance
            if random.random() < 0.3:  # Chance for rare enemy
                enemy = random_enemy_for_level(self.player.level + 1)
                self.append_log(f"💀 Rare {enemy.name} ambushes you! (HP: {enemy.hp}, Level: {enemy.level})", "danger")
            else:
                enemy = random_enemy_for_level(self.player.level)
                self.append_log(f"⚔️ {enemy.name} notices you! (HP: {enemy.hp})", "danger")
            self.append_log("Opening battle interface...", "warning")
            self.app.open_battle(enemy)
        else:
            # Higher gold reward for careful search
            gold = random.randint(self.min_gold_find + 3, self.max_gold_find + 5)
            self.player.gold += gold
            
            # Chance for bonus item or extra gold
            if random.random() < 0.2:
                bonus_gold = random.randint(5, 15)
                self.player.gold += bonus_gold
                self.append_log(f"🎯 You discover a hidden treasure chest!", "success")
                self.append_log(f"💰 Found {gold} gold coins + {bonus_gold} bonus gold!", "gold")
            else:
                self.append_log(f"💰 Carefully searching reveals {gold} gold coins!", "gold")
            
            self.update_status()
            self.app.update_info()

    def animate_exploration(self):
        """Simple animation for exploration actions"""
        original_text = self.btn_walk.cget("text")
        self.btn_walk.configure(text="Exploring...", state="disabled")
        self.btn_search.configure(state="disabled")
        self.btn_rest.configure(state="disabled")
        
        def restore_buttons():
            self.btn_walk.configure(text=original_text, state="normal")
            self.btn_search.configure(state="normal")
            self.btn_rest.configure(state="normal")
        
        self.after(1200, restore_buttons)

    def refresh(self):
        """Refresh the frame with updated player data"""
        self.update_status()
        self.append_log("Exploration interface refreshed.", "info")