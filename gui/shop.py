# import customtkinter as ctk
# import json
# from core.skill import skill_from_dict

# SHOP_ITEMS = [
#     {"id":"p_hp_small","name":"Small Potion","desc":"Restore 30 HP","effect":{"hp":30},"price":20},
#     {"id":"p_mp_small","name":"Small MP","desc":"Restore 20 MP","effect":{"mp":20},"price":15}
# ]

# class ShopFrame(ctk.CTkFrame):
#     def __init__(self, master, player, app):
#         super().__init__(master)
#         self.player = player
#         self.app = app

#         self.left = ctk.CTkFrame(self, width=300)
#         self.left.pack(side="left", fill="y", padx=8, pady=8)
#         self.right = ctk.CTkFrame(self)
#         self.right.pack(side="right", fill="both", expand=True, padx=8, pady=8)

#         self.lbl = ctk.CTkLabel(self.left, text="Shop")
#         self.lbl.pack(pady=6)
#         self.gold_lbl = ctk.CTkLabel(self.left, text=f"Gold: {self.player.gold}")
#         self.gold_lbl.pack(pady=4)

#         # load skills data for shop selling skills as well
#         with open("data/skills.json","r",encoding="utf-8") as f:
#             self.skills_db = json.load(f)

#         self.skill_listbox = ctk.CTkTextbox(self.right, height=200, state="disabled")
#         self.skill_listbox.pack(fill="x", padx=8, pady=6)
#         self.populate_skills()

#         self.btn_buy_skill = ctk.CTkButton(self.left, text="Buy Selected Skill", command=self.buy_skill)
#         self.btn_buy_skill.pack(pady=6)
#         self.btn_buy_item = ctk.CTkButton(self.left, text="Buy Potion", command=self.buy_potion)
#         self.btn_buy_item.pack(pady=6)

#         self.msg = ctk.CTkLabel(self.left, text="")
#         self.msg.pack(pady=4)

#     def populate_skills(self):
#         self.skill_listbox.configure(state="normal")
#         self.skill_listbox.delete("1.0","end")
#         # show only player's class skills
#         cls = self.player.role
#         for s in self.skills_db:
#             if s.get("class") == cls:
#                 self.skill_listbox.insert("end", f"{s['id']} - {s['name']} ({s['type']}) Price: {s['cost']} MPcost:{s.get('mp_cost',0)}\n")
#         self.skill_listbox.configure(state="disabled")

#     def buy_skill(self):
#         # naive: buy first available for class
#         cls = self.player.role
#         for s in self.skills_db:
#             if s.get("class") == cls:
#                 skill = skill_from_dict(s)
#                 if any(skill.id == sk.id for sk in self.player.skills):
#                     self.msg.configure(text="Already learned this skill.")
#                     return
#                 if self.player.gold >= skill.cost:
#                     self.player.learn_skill(skill)
#                     self.msg.configure(text=f"Bought skill {skill.name}")
#                     self.gold_lbl.configure(text=f"Gold: {self.player.gold}")
#                     return
#                 else:
#                     self.msg.configure(text="Not enough gold.")
#                     return
#         self.msg.configure(text="No skill found.")

#     def buy_potion(self):
#         item = SHOP_ITEMS[0]
#         if self.player.gold >= item["price"]:
#             self.player.gold -= item["price"]
#             self.player.inventory[item["id"]] = self.player.inventory.get(item["id"],0) + 1
#             self.gold_lbl.configure(text=f"Gold: {self.player.gold}")
#             self.msg.configure(text=f"Bought {item['name']}")
#         else:
#             self.msg.configure(text="Not enough gold.")

import customtkinter as ctk
import json
from core.skill import skill_from_dict

SHOP_ITEMS = [
    {"id": "p_hp_small", "name": "Small Health Potion", "desc": "Restore 30 HP", "effect": {"hp": 30}, "price": 20, "icon": "❤️"},
    {"id": "p_mp_small", "name": "Small Mana Potion", "desc": "Restore 20 MP", "effect": {"mp": 20}, "price": 15, "icon": "🔵"},
    {"id": "p_hp_medium", "name": "Health Potion", "desc": "Restore 60 HP", "effect": {"hp": 60}, "price": 35, "icon": "❤️"},
    {"id": "p_mp_medium", "name": "Mana Potion", "desc": "Restore 40 MP", "effect": {"mp": 40}, "price": 25, "icon": "🔵"},
    {"id": "p_antidote", "name": "Antidote", "desc": "Cure poison status", "effect": {"status": "cure_poison"}, "price": 30, "icon": "🧪"},
    {"id": "p_elixir", "name": "Elixir", "desc": "Restore 50 HP and 30 MP", "effect": {"hp": 50, "mp": 30}, "price": 50, "icon": "✨"}
]

class ShopFrame(ctk.CTkFrame):
    def __init__(self, master, player, app):
        super().__init__(master, fg_color="transparent")
        self.player = player
        self.app = app
        self.selected_item = None
        self.selected_skill = None
        
        # Load skills data
        with open("data/skills.json", "r", encoding="utf-8") as f:
            self.skills_db = json.load(f)
        
        self.setup_ui()
        self.populate_items()
        self.populate_skills()

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title and gold display
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))
        
        self.lbl = ctk.CTkLabel(
            title_frame,
            text="🛒 Merchant's Shop",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl.pack(side="left")
        
        self.gold_lbl = ctk.CTkLabel(
            title_frame,
            text=f"💰 {self.player.gold} Gold",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#FFD700"
        )
        self.gold_lbl.pack(side="right")
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Items section
        items_frame = ctk.CTkFrame(content_frame)
        items_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Items header
        items_header = ctk.CTkFrame(items_frame, fg_color="transparent")
        items_header.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            items_header, 
            text="🛍️ Consumables", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        # Items scrollable frame
        self.items_container = ctk.CTkScrollableFrame(items_frame, height=200)
        self.items_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Skills section
        skills_frame = ctk.CTkFrame(content_frame)
        skills_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Skills header
        skills_header = ctk.CTkFrame(skills_frame, fg_color="transparent")
        skills_header.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            skills_header, 
            text="📚 Skills & Abilities", 
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")
        
        ctk.CTkLabel(
            skills_header,
            text=f"Class: {self.player.role}",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        ).pack(side="right")
        
        # Skills scrollable frame
        self.skills_container = ctk.CTkScrollableFrame(skills_frame, height=200)
        self.skills_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Details and actions panel
        action_frame = ctk.CTkFrame(self)
        action_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Details display
        self.details_frame = ctk.CTkFrame(action_frame, height=80)
        self.details_frame.pack(fill="x", pady=(0, 10))
        self.details_frame.pack_propagate(False)
        
        self.details_label = ctk.CTkLabel(
            self.details_frame,
            text="Select an item or skill to view details...",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60"),
            justify="left",
            wraplength=800
        )
        self.details_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Action buttons
        button_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=5)
        
        self.btn_buy_item = ctk.CTkButton(
            button_frame,
            text="🛒 Buy Selected Item",
            command=self.buy_selected_item,
            height=45,
            font=ctk.CTkFont(size=15),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            state="disabled"
        )
        self.btn_buy_item.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        self.btn_buy_skill = ctk.CTkButton(
            button_frame,
            text="📚 Learn Selected Skill",
            command=self.buy_selected_skill,
            height=45,
            font=ctk.CTkFont(size=15),
            fg_color="#2B5B84",
            hover_color="#1E3F5C",
            state="disabled"
        )
        self.btn_buy_skill.pack(side="right", fill="x", expand=True, padx=(5, 0))
        
        # Status message
        self.msg = ctk.CTkLabel(
            action_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        self.msg.pack(pady=5)

    def populate_items(self):
        """Populate the items section with available consumables"""
        for widget in self.items_container.winfo_children():
            widget.destroy()
        
        for item in SHOP_ITEMS:
            item_card = self.create_item_card(item)
            item_card.pack(fill="x", padx=5, pady=5)

    def create_item_card(self, item):
        """Create a card for an item"""
        card = ctk.CTkFrame(
            self.items_container,
            border_width=2,
            border_color=("#3E7BFA", "#2B5B84")
        )
        
        card.grid_columnconfigure(1, weight=1)
        
        # Item icon
        icon_label = ctk.CTkLabel(card, text=item["icon"], font=ctk.CTkFont(size=16))
        icon_label.grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky="n")
        
        # Item info
        name_frame = ctk.CTkFrame(card, fg_color="transparent")
        name_frame.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(10, 0))
        name_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=item["name"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        price_label = ctk.CTkLabel(
            name_frame,
            text=f"💰 {item['price']} Gold",
            font=ctk.CTkFont(size=12),
            text_color="#FFD700",
            anchor="e"
        )
        price_label.grid(row=0, column=1, sticky="e")
        
        # Item description
        desc_label = ctk.CTkLabel(
            card,
            text=item["desc"],
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70"),
            anchor="w"
        )
        desc_label.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 10))
        
        # Select button
        select_btn = ctk.CTkButton(
            card,
            text="Select",
            command=lambda i=item: self.select_item(i),
            width=80,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        select_btn.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        
        return card

    def populate_skills(self):
        """Populate the skills section with class-appropriate skills"""
        for widget in self.skills_container.winfo_children():
            widget.destroy()
        
        class_skills = [s for s in self.skills_db if s.get("class") == self.player.role]
        
        if not class_skills:
            empty_label = ctk.CTkLabel(
                self.skills_container,
                text="No skills available for your class.",
                font=ctk.CTkFont(size=14),
                text_color=("gray50", "gray70")
            )
            empty_label.pack(pady=20)
            return
        
        for skill_data in class_skills:
            skill = skill_from_dict(skill_data)
            skill_card = self.create_skill_card(skill, skill_data)
            skill_card.pack(fill="x", padx=5, pady=5)

    def create_skill_card(self, skill, skill_data):
        """Create a card for a skill"""
        already_learned = any(skill.id == sk.id for sk in self.player.skills)
        can_afford = self.player.gold >= skill.cost
        
        card = ctk.CTkFrame(
            self.skills_container,
            border_width=2,
            border_color=("#3E7BFA", "#2B5B84")
        )
        
        card.grid_columnconfigure(1, weight=1)
        
        # Skill type icon
        type_icon = "⚔️" if skill.type == "Physical" else "🔮" if skill.type == "Magic" else "✨"
        icon_label = ctk.CTkLabel(card, text=type_icon, font=ctk.CTkFont(size=16))
        icon_label.grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky="n")
        
        # Skill info
        name_frame = ctk.CTkFrame(card, fg_color="transparent")
        name_frame.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(10, 0))
        name_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(
            name_frame,
            text=skill.name,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        price_label = ctk.CTkLabel(
            name_frame,
            text=f"💰 {skill.cost} Gold",
            font=ctk.CTkFont(size=12),
            text_color="#FFD700" if can_afford else "#FF6B6B",
            anchor="e"
        )
        price_label.grid(row=0, column=1, sticky="e")
        
        # Skill stats
        stats_text = f"Type: {skill.type} | MP: {skill_data.get('mp_cost', 0)} | Power: {skill_data.get('power', 'N/A')}"
        stats_label = ctk.CTkLabel(
            card,
            text=stats_text,
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70"),
            anchor="w"
        )
        stats_label.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 10))
        
        # Status/Select button
        status_frame = ctk.CTkFrame(card, fg_color="transparent")
        status_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        
        if already_learned:
            status_label = ctk.CTkLabel(
                status_frame,
                text="✅ Learned",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#2E8B57"
            )
            status_label.pack()
        elif not can_afford:
            status_label = ctk.CTkLabel(
                status_frame,
                text="❌ Too Expensive",
                font=ctk.CTkFont(size=12),
                text_color="#FF6B6B"
            )
            status_label.pack()
        else:
            select_btn = ctk.CTkButton(
                status_frame,
                text="Select",
                command=lambda s=skill: self.select_skill(s),
                width=80,
                height=30,
                font=ctk.CTkFont(size=12)
            )
            select_btn.pack()
        
        return card

    def select_item(self, item):
        """Select an item for purchase"""
        self.selected_item = item
        self.selected_skill = None
        self.update_details()
        self.btn_buy_item.configure(state="normal")
        self.btn_buy_skill.configure(state="disabled")

    def select_skill(self, skill):
        """Select a skill for purchase"""
        self.selected_skill = skill
        self.selected_item = None
        self.update_details()
        self.btn_buy_skill.configure(state="normal")
        self.btn_buy_item.configure(state="disabled")

    def update_details(self):
        """Update the details display based on selection"""
        if self.selected_item:
            item = self.selected_item
            details = (
                f"🛍️ {item['name']}\n"
                f"📖 {item['desc']}\n"
                f"💰 Price: {item['price']} Gold\n"
                f"🎯 Effect: {self.get_effect_description(item['effect'])}"
            )
        elif self.selected_skill:
            skill = self.selected_skill
            details = (
                f"📚 {skill.name}\n"
                f"⚔️ Type: {skill.type} | 💪 Power: {getattr(skill, 'power', 'N/A')}\n"
                f"💰 Cost: {skill.cost} Gold | 🔵 MP Cost: {getattr(skill, 'mp_cost', 0)}\n"
                f"🎯 {getattr(skill, 'description', 'No description available.')}"
            )
        else:
            details = "Select an item or skill to view details..."
        
        self.details_label.configure(
            text=details,
            text_color=("gray10", "gray90")
        )

    def get_effect_description(self, effect):
        """Convert effect dict to readable description"""
        descriptions = []
        if "hp" in effect:
            descriptions.append(f"Restore {effect['hp']} HP")
        if "mp" in effect:
            descriptions.append(f"Restore {effect['mp']} MP")
        if "status" in effect:
            descriptions.append(f"Cure {effect['status']}")
        return " + ".join(descriptions) if descriptions else "Unknown effect"

    def buy_selected_item(self):
        """Buy the selected item"""
        if not self.selected_item:
            self.show_message("Please select an item first!", "error")
            return
        
        item = self.selected_item
        
        if self.player.gold < item["price"]:
            self.show_message(f"Not enough gold! Need {item['price']}, have {self.player.gold}.", "error")
            return
        
        # Process purchase
        self.player.gold -= item["price"]
        self.player.inventory[item["id"]] = self.player.inventory.get(item["id"], 0) + 1
        
        self.show_message(f"✅ Purchased {item['name']}!", "success")
        self.update_gold_display()
        self.app.update_info()

    def buy_selected_skill(self):
        """Buy the selected skill"""
        if not self.selected_skill:
            self.show_message("Please select a skill first!", "error")
            return
        
        skill = self.selected_skill
        
        # Check if already learned
        if any(skill.id == sk.id for sk in self.player.skills):
            self.show_message(f"You have already learned {skill.name}!", "error")
            return
        
        if self.player.gold < skill.cost:
            self.show_message(f"Not enough gold! Need {skill.cost}, have {self.player.gold}.", "error")
            return
        
        # Learn the skill
        self.player.learn_skill(skill)
        self.show_message(f"🎉 Successfully learned {skill.name}!", "success")
        
        self.update_gold_display()
        self.populate_skills()  # Refresh skills display
        self.app.update_info()
        
        # Reset selection
        self.selected_skill = None
        self.btn_buy_skill.configure(state="disabled")
        self.update_details()

    def show_message(self, message, message_type="info"):
        """Show status message with color coding"""
        colors = {
            "success": "#2E8B57",
            "error": "#FF6B6B", 
            "info": "#3E7BFA",
            "warning": "#FFA500"
        }
        
        self.msg.configure(
            text=message,
            text_color=colors.get(message_type, "#3E7BFA")
        )
        
        # Clear message after 3 seconds
        self.after(3000, lambda: self.msg.configure(text=""))

    def update_gold_display(self):
        """Update the gold display"""
        self.gold_lbl.configure(text=f"💰 {self.player.gold} Gold")

    def refresh(self):
        """Refresh the shop interface"""
        self.update_gold_display()
        self.populate_items()
        self.populate_skills()
        self.selected_item = None
        self.selected_skill = None
        self.btn_buy_item.configure(state="disabled")
        self.btn_buy_skill.configure(state="disabled")
        self.details_label.configure(
            text="Select an item or skill to view details...",
            text_color=("gray40", "gray60")
        )
        self.msg.configure(text="")