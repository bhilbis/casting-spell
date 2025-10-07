# import customtkinter as ctk
# from core.player import Player
# from core.save_load import save_player, load_player
# from gui.explore import ExploreFrame
# from gui.shop import ShopFrame
# from gui.skill_learn import SkillLearnFrame
# from gui.battle import BattleFrame

# class MainApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("RPG Adventure - Mini")
#         self.geometry("900x600")
#         ctk.set_appearance_mode("dark")
#         ctk.set_default_color_theme("blue")

#         self.player = None  # type: Player|None

#         # left panel: player info / menu
#         self.left_frame = ctk.CTkFrame(master=self, width=240)
#         self.left_frame.pack(side="left", fill="y", padx=8, pady=8)

#         self.info_label = ctk.CTkLabel(self.left_frame, text="No player", justify="left")
#         self.info_label.pack(pady=10)

#         self.btn_new = ctk.CTkButton(self.left_frame, text="New Game", command=self.new_game_dialog)
#         self.btn_new.pack(fill="x", padx=10, pady=6)
#         self.btn_load = ctk.CTkButton(self.left_frame, text="Load Game", command=self.load_game)
#         self.btn_load.pack(fill="x", padx=10, pady=6)
#         self.btn_save = ctk.CTkButton(self.left_frame, text="Save Game", command=self.save_game)
#         self.btn_save.pack(fill="x", padx=10, pady=6)

#         # action buttons
#         self.btn_explore = ctk.CTkButton(self.left_frame, text="Explore", command=self.open_explore)
#         self.btn_shop = ctk.CTkButton(self.left_frame, text="Shop", command=self.open_shop)
#         self.btn_skills = ctk.CTkButton(self.left_frame, text="Learn Skill", command=self.open_skill_learn)

#         self.btn_explore.pack(fill="x", padx=10, pady=6)
#         self.btn_shop.pack(fill="x", padx=10, pady=6)
#         self.btn_skills.pack(fill="x", padx=10, pady=6)

#         # main area
#         self.main_area = ctk.CTkFrame(master=self)
#         self.main_area.pack(side="right", fill="both", expand=True, padx=8, pady=8)

#         self.current_frame = None

#         self.update_info()

#     def new_game_dialog(self):
#         # Simple dialog to create player
#         import tkinter as tk
#         from tkinter import simpledialog
#         root = tk.Toplevel(self)
#         root.title("Create Character")
#         root.geometry("300x220")
#         tk.Label(root, text="Name:").pack(pady=4)
#         name_entry = tk.Entry(root); name_entry.pack(pady=4)
#         tk.Label(root, text="Role:").pack(pady=4)
#         role_var = tk.StringVar(value="Warrior")
#         tk.OptionMenu(root, role_var, "Warrior", "Mage", "Archer").pack(pady=4)

#         def create():
#             name = name_entry.get().strip() or "Hero"
#             role = role_var.get()
#             self.player = Player(name, role)
#             self.update_info()
#             root.destroy()

#         tk.Button(root, text="Create", command=create).pack(pady=10)

#     def load_game(self):
#         p = load_player()
#         if p:
#             self.player = p
#         self.update_info()

#     def save_game(self):
#         if self.player:
#             save_player(self.player)
#         self.update_info()

#     def update_info(self):
#         if self.player:
#             s = (f"Name: {self.player.name}\nRole: {self.player.role}\nLevel: {self.player.level}\n"
#                  f"HP: {self.player.hp}/{self.player.max_hp}\nMP: {self.player.mp}/{self.player.max_mp}\nGold: {self.player.gold}\n"
#                  f"Skills: {len(self.player.skills)}")
#         else:
#             s = "No player\nStart a new game or load."
#         self.info_label.configure(text=s)

#     def clear_main(self):
#         if self.current_frame:
#             self.current_frame.pack_forget()
#             self.current_frame.destroy()
#             self.current_frame = None

#     def open_explore(self):
#         if not self.player:
#             self.show_message("Create or load a player first.")
#             return
#         self.clear_main()
#         self.current_frame = ExploreFrame(self.main_area, self.player, self)
#         self.current_frame.pack(fill="both", expand=True)

#     def open_shop(self):
#         if not self.player:
#             self.show_message("Create or load a player first.")
#             return
#         self.clear_main()
#         self.current_frame = ShopFrame(self.main_area, self.player, self)
#         self.current_frame.pack(fill="both", expand=True)

#     def open_skill_learn(self):
#         if not self.player:
#             self.show_message("Create or load a player first.")
#             return
#         self.clear_main()
#         self.current_frame = SkillLearnFrame(self.main_area, self.player, self)
#         self.current_frame.pack(fill="both", expand=True)

#     def open_battle(self, enemy):
#         # battle frame for direct start
#         self.clear_main()
#         self.current_frame = BattleFrame(self.main_area, self.player, enemy, self)
#         self.current_frame.pack(fill="both", expand=True)

#     def show_message(self, text: str):
#         import tkinter.messagebox as mb
#         mb.showinfo("Info", text)
import customtkinter as ctk
from core.player import Player
from core.save_load import save_player, load_player
from gui.explore import ExploreFrame
from gui.shop import ShopFrame
from gui.skill_learn import SkillLearnFrame
from gui.battle import BattleFrame

class ModernMainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("RPG Adventure - Mini")
        self.geometry("1920x1080")
        self.minsize(1200, 700)
        
        # Modern theme configuration
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.player = None

        # Create sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        # App logo/title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="RPG Adventure", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Player info frame with modern styling
        self.info_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.info_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.info_label = ctk.CTkLabel(
            self.info_frame, 
            text="No player data\n\nStart a new game\nor load existing", 
            justify="left",
            font=ctk.CTkFont(size=14),
            wraplength=200
        )
        self.info_label.pack(fill="both", padx=10, pady=15)

        # Game management buttons
        self.btn_new = ctk.CTkButton(
            self.sidebar_frame, 
            text="New Game", 
            command=self.new_game_dialog,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.btn_new.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.btn_load = ctk.CTkButton(
            self.sidebar_frame, 
            text="Load Game", 
            command=self.load_game,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_load.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")

        self.btn_save = ctk.CTkButton(
            self.sidebar_frame, 
            text="Save Game", 
            command=self.save_game,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_save.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Action section label
        self.actions_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="ACTIONS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.actions_label.grid(row=5, column=0, padx=20, pady=(10, 15))

        # self.btn_battle = ctk.CTkButton(
        # self.sidebar_frame, 
        # text="⚔️  Battle Arena", 
        # command=self.open_battle_arena,
        # height=45,
        # font=ctk.CTkFont(size=15),
        # fg_color="#FF6B6B",
        # hover_color="#FF8C8C"
        # )
        # self.btn_battle.grid(row=9, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Action buttons with icons (using text icons for simplicity)
        self.btn_explore = ctk.CTkButton(
            self.sidebar_frame, 
            text="🗺️  Explore", 
            command=self.open_explore,
            height=45,
            font=ctk.CTkFont(size=15),
            fg_color="#2B5B84",
            hover_color="#1E3F5C"
        )
        self.btn_explore.grid(row=6, column=0, padx=20, pady=(0, 12), sticky="ew")

        self.btn_shop = ctk.CTkButton(
            self.sidebar_frame, 
            text="🛒  Shop", 
            command=self.open_shop,
            height=45,
            font=ctk.CTkFont(size=15),
            fg_color="#2B5B84",
            hover_color="#1E3F5C"
        )
        self.btn_shop.grid(row=7, column=0, padx=20, pady=(0, 12), sticky="ew")

        self.btn_skills = ctk.CTkButton(
            self.sidebar_frame, 
            text="📚  Learn Skills", 
            command=self.open_skill_learn,
            height=45,
            font=ctk.CTkFont(size=15),
            fg_color="#2B5B84",
            hover_color="#1E3F5C"
        )
        self.btn_skills.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="ew")

        # Main content area with gradient-like background
        self.main_area = ctk.CTkFrame(
            self, 
            fg_color=("gray90", "gray13")  # Slightly different background for contrast
        )
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=(0, 8), pady=8)
        
        # Welcome message in main area
        self.welcome_label = ctk.CTkLabel(
            self.main_area,
            text="Welcome to RPG Adventure!\n\nCreate a new character or load an existing one to begin your journey.",
            font=ctk.CTkFont(size=18),
            text_color=("gray40", "gray60"),
            justify="center"
        )
        self.welcome_label.place(relx=0.5, rely=0.5, anchor="center")

        self.current_frame = None
        self.update_info()

    def new_game_dialog(self):
        # Modern dialog using CTk
        dialog = ctk.CTkToplevel(self)
        dialog.title("Create Character")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Dialog content
        title_label = ctk.CTkLabel(
            dialog, 
            text="Create New Character", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        # Name input
        name_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        name_frame.pack(fill="x", padx=40, pady=(15, 5))
        
        ctk.CTkLabel(name_frame, text="Character Name:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        name_entry = ctk.CTkEntry(
            name_frame, 
            placeholder_text="Enter your character name",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        name_entry.pack(fill="x", pady=(5, 0))
        name_entry.focus()

        # Role selection
        role_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        role_frame.pack(fill="x", padx=40, pady=(15, 5))
        
        ctk.CTkLabel(role_frame, text="Choose Role:", font=ctk.CTkFont(size=14)).pack(anchor="w")
        role_var = ctk.StringVar(value="Warrior")
        role_menu = ctk.CTkOptionMenu(
            role_frame,
            values=["Warrior", "Mage", "Archer"],
            variable=role_var,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        role_menu.pack(fill="x", pady=(5, 0))

        def create():
            name = name_entry.get().strip() or "Hero"
            role = role_var.get()
            self.player = Player(name, role)
            self.update_info()
            dialog.destroy()
            
            # Remove welcome message
            self.welcome_label.place_forget()

        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=40, pady=20)
        
        ctk.CTkButton(
            button_frame, 
            text="Create Character", 
            command=create,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(fill="x", pady=(0, 10))
        
        ctk.CTkButton(
            button_frame, 
            text="Cancel", 
            command=dialog.destroy,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "gray90")
        ).pack(fill="x")

    def load_game(self):
        p = load_player()
        if p:
            self.player = p
            self.update_info()
            self.welcome_label.place_forget()  # Remove welcome message
            self.show_modern_message("Game loaded successfully!", "Success")
        else:
            self.show_modern_message("No saved game found!", "Error")

    def save_game(self):
        if self.player:
            save_player(self.player)
            self.show_modern_message("Game saved successfully!", "Success")
        else:
            self.show_modern_message("No player data to save!", "Error")
        self.update_info()

    def update_info(self):
        if self.player:
            info_text = (
                f"👤 {self.player.name}\n"
                f"⚔️  {self.player.role}\n"
                f"⭐ Level {self.player.level}\n"
                f"❤️  {self.player.hp}/{self.player.max_hp} HP\n"
                f"🔵 {self.player.mp}/{self.player.max_mp} MP\n"
                f"💰 {self.player.gold} Gold\n"
                f"📚 {len(self.player.skills)} Skills"
            )
            # Update button states
            for btn in [self.btn_explore, self.btn_shop, self.btn_skills]:
                btn.configure(state="normal")
        else:
            info_text = "No player data\n\nStart a new game\nor load existing"
            # Disable action buttons when no player
            for btn in [self.btn_explore, self.btn_shop, self.btn_skills]:
                btn.configure(state="disabled")
                
        self.info_label.configure(text=info_text)

    def clear_main(self):
        if self.current_frame:
            self.current_frame.pack_forget()
            self.current_frame.destroy()
            self.current_frame = None

    def open_explore(self):
        if not self.player:
            self.show_modern_message("Create or load a player first!", "Warning")
            return
        self.clear_main()
        self.current_frame = ExploreFrame(self.main_area, self.player, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def open_shop(self):
        if not self.player:
            self.show_modern_message("Create or load a player first!", "Warning")
            return
        self.clear_main()
        self.current_frame = ShopFrame(self.main_area, self.player, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def open_skill_learn(self):
        if not self.player:
            self.show_modern_message("Create or load a player first!", "Warning")
            return
        self.clear_main()
        self.current_frame = SkillLearnFrame(self.main_area, self.player, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Add this to your main_menu.py in the sidebar
    def update_info(self):
        if self.player:
            # Basic info
            info_text = (
                f"👤 {self.player.name}\n"
                f"⚔️ {self.player.role}\n" 
                f"⭐ Level {self.player.level}\n"
                f"❤️ {self.player.hp}/{self.player.max_hp} HP\n"
                f"🔵 {self.player.mp}/{self.player.max_mp} MP\n"
                f"💰 {self.player.gold} Gold\n"
                f"📚 {len(self.player.skills)} Skills"
            )
            
            # Add inventory info
            if self.player.inventory:
                inventory_text = "\n🎒 Inventory:"
                for item_id, qty in self.player.inventory.items():
                    item_name = self.get_item_name(item_id)
                    inventory_text += f"\n  {item_name} x{qty}"
                info_text += inventory_text
            
            self.info_label.configure(text=info_text)
            
            # Update button states
            for btn in [self.btn_explore, self.btn_shop, self.btn_skills]:
                btn.configure(state="normal")
        else:
            info_text = "No player data\n\nStart a new game\nor load existing"
            # Disable action buttons when no player
            for btn in [self.btn_explore, self.btn_shop, self.btn_skills]:
                btn.configure(state="disabled")
                
        self.info_label.configure(text=info_text)

    def get_item_name(self, item_id: str) -> str:
        """Get display name for items"""
        item_names = {
            "p_hp_small": "HP Potion",
            "p_mp_small": "MP Potion",
            "p_hp_medium": "Big HP Potion", 
            "p_mp_medium": "Big MP Potion",
            "p_elixir": "Elixir"
        }
        return item_names.get(item_id, item_id)
    # def open_battle_arena(self):
    #     if not self.player:
    #         self.show_modern_message("Create or load a player first!", "Warning")
    #         return
    #     # Create a test enemy for direct battle
    #     from core.enemy import random_enemy_for_level
    #     enemy = random_enemy_for_level(self.player.level)
    #     self.open_battle(enemy)

    def open_battle(self, enemy):
        self.clear_main()
        self.current_frame = BattleFrame(self.main_area, self.player, enemy, self)
        self.current_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_modern_message(self, text: str, title: str = "Info"):
        # Create a modern toast-like message
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        # Icon based on title
        icon = "ℹ️"
        if "Error" in title:
            icon = "❌"
        elif "Success" in title:
            icon = "✅"
        elif "Warning" in title:
            icon = "⚠️"

        ctk.CTkLabel(
            dialog, 
            text=f"{icon}\n{text}", 
            font=ctk.CTkFont(size=15),
            justify="center"
        ).pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkButton(
            dialog, 
            text="OK", 
            command=dialog.destroy,
            height=40
        ).pack(pady=(0, 20))

    def show_message(self, text: str):
        # Fallback to modern message
        self.show_modern_message(text)

# Replace the original class name for easy integration
MainApp = ModernMainApp