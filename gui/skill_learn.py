import customtkinter as ctk
import json
from core.skill import skill_from_dict

class SkillLearnFrame(ctk.CTkFrame):
    def __init__(self, master, player, app):
        super().__init__(master, fg_color="transparent")
        self.player = player
        self.app = app
        
        # Load skills data
        with open("data/skills.json", "r", encoding="utf-8") as f:
            self.skills_db = json.load(f)
        
        self.available_skills = []
        self.selected_skill = None
        
        self.setup_ui()
        self.populate_skills()

    def setup_ui(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.lbl = ctk.CTkLabel(
            header_frame, 
            text="🎓 Skill Academy", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl.pack(side="left")
        
        # Player gold info
        self.gold_label = ctk.CTkLabel(
            header_frame,
            text=f"💰 Gold: {self.player.gold}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#FFD700"
        )
        self.gold_label.pack(side="right")
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Skills list frame
        skills_frame = ctk.CTkFrame(content_frame)
        skills_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Skills list header
        list_header = ctk.CTkFrame(skills_frame, fg_color="transparent")
        list_header.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(list_header, text="Available Skills", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        ctk.CTkLabel(list_header, text=f"Class: {self.player.role}", font=ctk.CTkFont(size=14)).pack(side="right")
        
        # Skills scrollable frame
        self.skills_container = ctk.CTkScrollableFrame(
            skills_frame, 
            height=300,
            fg_color=("gray85", "gray17")
        )
        self.skills_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Skill details frame
        self.details_frame = ctk.CTkFrame(content_frame, height=120)
        self.details_frame.pack(fill="x", pady=(0, 15))
        self.details_frame.pack_propagate(False)
        
        self.details_label = ctk.CTkLabel(
            self.details_frame, 
            text="Select a skill to view details...",
            font=ctk.CTkFont(size=14),
            text_color=("gray40", "gray60"),
            justify="left",
            wraplength=600
        )
        self.details_label.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Action buttons frame
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=10)
        
        self.btn_buy = ctk.CTkButton(
            button_frame, 
            text="🎯 Learn Selected Skill", 
            command=self.buy_selected,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2E8B57",
            hover_color="#3CB371",
            state="disabled"
        )
        self.btn_buy.pack(fill="x", pady=5)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            button_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        self.status_label.pack(pady=5)

    def populate_skills(self):
        # Clear existing skills
        for widget in self.skills_container.winfo_children():
            widget.destroy()
        
        self.available_skills.clear()
        
        # Filter skills by player class
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
            self.available_skills.append(skill)
            
            # Check if already learned
            already_learned = any(skill.id == sk.id for sk in self.player.skills)
            can_afford = self.player.gold >= skill.cost
            
            # Create skill card
            skill_card = self.create_skill_card(skill, already_learned, can_afford)
            skill_card.pack(fill="x", padx=5, pady=5)

    def create_skill_card(self, skill, already_learned, can_afford):
        card = ctk.CTkFrame(
            self.skills_container, 
            border_width=2,
            border_color=("#3E7BFA", "#2B5B84")
        )
        
        # Configure grid for card layout
        card.grid_columnconfigure(1, weight=1)
        
        # Skill icon/type indicator
        type_icon = "⚔️" if skill.type == "Physical" else "🔮" if skill.type == "Magic" else "✨"
        icon_label = ctk.CTkLabel(card, text=type_icon, font=ctk.CTkFont(size=16))
        icon_label.grid(row=0, column=0, rowspan=2, padx=15, pady=10, sticky="n")
        
        # Skill name and basic info
        name_frame = ctk.CTkFrame(card, fg_color="transparent")
        name_frame.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=(10, 0))
        name_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(
            name_frame, 
            text=skill.name,
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        # Cost and MP
        cost_label = ctk.CTkLabel(
            name_frame,
            text=f"💰 {skill.cost} Gold | 🔵 {getattr(skill, 'mp_cost', 0)} MP",
            font=ctk.CTkFont(size=12),
            text_color="#FFD700",
            anchor="e"
        )
        cost_label.grid(row=0, column=1, sticky="e")
        
        # Skill type and power
        info_label = ctk.CTkLabel(
            card,
            text=f"Type: {skill.type} | Power: {getattr(skill, 'power', 'N/A')}",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70"),
            anchor="w"
        )
        info_label.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 10))
        
        # Status indicator
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
            # Select button for affordable, unlearned skills
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

    def select_skill(self, skill):
        self.selected_skill = skill
        self.update_skill_details(skill)
        self.btn_buy.configure(state="normal")
        
        # Highlight selected skill (you could add visual feedback here)

    def update_skill_details(self, skill):
        details = (
            f"🎯 {skill.name}\n"
            f"📖 {getattr(skill, 'description', 'No description available.')}\n"
            f"⚔️ Type: {skill.type} | 💪 Power: {getattr(skill, 'power', 'N/A')}\n"
            f"💰 Cost: {skill.cost} Gold | 🔵 MP Cost: {getattr(skill, 'mp_cost', 0)}\n"
            f"🎯 Accuracy: {getattr(skill, 'accuracy', 'N/A')}%"
        )
        
        self.details_label.configure(
            text=details,
            text_color=("gray10", "gray90")
        )

    def buy_selected(self):
        if not self.selected_skill:
            self.show_status("Please select a skill first!", "error")
            return
            
        skill = self.selected_skill
        
        # Check if already learned
        if any(skill.id == sk.id for sk in self.player.skills):
            self.show_status(f"You have already learned {skill.name}!", "error")
            return
            
        # Check if player can afford
        if self.player.gold < skill.cost:
            self.show_status(f"Not enough gold! Need {skill.cost}, have {self.player.gold}.", "error")
            return
            
        # Learn the skill
        self.player.learn_skill(skill)
        self.show_status(f"🎉 Successfully learned {skill.name}!", "success")
        
        # Update UI
        self.update_gold_display()
        self.populate_skills()
        self.app.update_info()
        
        # Reset selection
        self.selected_skill = None
        self.btn_buy.configure(state="disabled")
        self.details_label.configure(
            text="Select a skill to view details...",
            text_color=("gray40", "gray60")
        )

    def show_status(self, message, message_type="info"):
        colors = {
            "success": "#2E8B57",
            "error": "#FF6B6B", 
            "info": "#3E7BFA",
            "warning": "#FFA500"
        }
        
        self.status_label.configure(
            text=message,
            text_color=colors.get(message_type, "#3E7BFA")
        )
        
        # Clear status after 3 seconds
        self.after(3000, lambda: self.status_label.configure(text=""))

    def update_gold_display(self):
        self.gold_label.configure(text=f"💰 Gold: {self.player.gold}")

    def refresh(self):
        """Refresh the frame with updated player data"""
        self.update_gold_display()
        self.populate_skills()
        self.selected_skill = None
        self.btn_buy.configure(state="disabled")
        self.details_label.configure(
            text="Select a skill to view details...",
            text_color=("gray40", "gray60")
        )
        self.status_label.configure(text="")