# gui/inventory.py
import customtkinter as ctk
from typing import Callable

class InventoryFrame(ctk.CTkFrame):
    def __init__(self, master, player, app):
        super().__init__(master, fg_color="transparent")
        self.player = player
        self.app = app
        
        self.setup_ui()
        self.refresh_inventory()

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="🎒 Inventory",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(side="left")
        
        # Player stats
        self.stats_label = ctk.CTkLabel(
            header_frame,
            text=f"❤️ {self.player.hp}/{self.player.max_hp} HP | 🔵 {self.player.mp}/{self.player.max_mp} MP",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray70")
        )
        self.stats_label.pack(side="right")
        
        # Inventory grid
        self.inventory_frame = ctk.CTkScrollableFrame(self)
        self.inventory_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid for items
        self.inventory_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="Select an item to use it",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        self.status_label.pack(pady=10)

    def refresh_inventory(self):
        """Refresh the inventory display"""
        # Clear existing items
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()
        
        # Update stats
        self.stats_label.configure(
            text=f"❤️ {self.player.hp}/{self.player.max_hp} HP | 🔵 {self.player.mp}/{self.player.max_mp} MP"
        )
        
        available_items = self.player.get_available_items()
        
        if not available_items:
            empty_label = ctk.CTkLabel(
                self.inventory_frame,
                text="Your inventory is empty.\nVisit the shop to buy items!",
                font=ctk.CTkFont(size=16),
                text_color=("gray50", "gray70"),
                justify="center"
            )
            empty_label.grid(row=0, column=0, columnspan=4, pady=50)
            return
        
        # Display items in grid
        for idx, item_id in enumerate(available_items):
            row = idx // 4
            col = idx % 4
            
            self.create_item_card(item_id, row, col)

    def create_item_card(self, item_id: str, row: int, col: int):
        """Create an item card in the inventory grid"""
        item_name = self.get_item_display_name(item_id)
        item_icon = self.get_item_icon(item_id)
        qty = self.player.inventory[item_id]
        
        card = ctk.CTkFrame(
            self.inventory_frame,
            border_width=2,
            border_color=("#3E7BFA", "#2B5B84"),
            corner_radius=10
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Item icon and name
        ctk.CTkLabel(
            card,
            text=item_icon,
            font=ctk.CTkFont(size=24)
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            card,
            text=item_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            wraplength=120
        ).pack(pady=5)
        
        # Quantity
        ctk.CTkLabel(
            card,
            text=f"Qty: {qty}",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        ).pack(pady=5)
        
        # Use button
        use_btn = ctk.CTkButton(
            card,
            text="Use",
            command=lambda i=item_id: self.use_item(i),
            height=30,
            font=ctk.CTkFont(size=12)
        )
        use_btn.pack(pady=10, padx=10, fill="x")

    def get_item_display_name(self, item_id: str) -> str:
        """Get display name for items"""
        item_names = {
            "p_hp_small": "Small HP Potion",
            "p_mp_small": "Small MP Potion",
            "p_hp_medium": "HP Potion", 
            "p_mp_medium": "MP Potion",
            "p_elixir": "Elixir"
        }
        return item_names.get(item_id, item_id)

    def get_item_icon(self, item_id: str) -> str:
        """Get icon for items"""
        item_icons = {
            "p_hp_small": "❤️",
            "p_mp_small": "🔵",
            "p_hp_medium": "❤️", 
            "p_mp_medium": "🔵",
            "p_elixir": "✨"
        }
        return item_icons.get(item_id, "📦")

    def use_item(self, item_id: str):
        """Use the selected item"""
        success, message = self.player.use_item(item_id)
        
        if success:
            self.status_label.configure(
                text=f"✅ {message}",
                text_color="#2E8B57"
            )
            self.refresh_inventory()
            self.app.update_info()
        else:
            self.status_label.configure(
                text=f"❌ {message}",
                text_color="#FF6B6B"
            )
        
        # Clear status after 3 seconds
        self.after(3000, lambda: self.status_label.configure(
            text="Select an item to use it",
            text_color=("gray50", "gray70")
        ))