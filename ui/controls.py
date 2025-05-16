import pygame
from config import Config

class Controls:
    """
    Gère les éléments d'interface utilisateur interactifs.
    Permet au joueur de modifier l'environnement et de contrôler la simulation.
    """
    def __init__(self, screen, grid):
        self.screen = screen
        self.grid = grid
        
        # Zone d'interface utilisateur (panneau latéral)
        self.ui_panel = pygame.Rect(
            Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH,
            0,
            Config.UI_PANEL_WIDTH,
            Config.SCREEN_HEIGHT
        )
        
        # Police pour le texte
        self.font = pygame.font.SysFont("Arial", 14)
        self.title_font = pygame.font.SysFont("Arial", 18, bold=True)
        
        # Couleurs
        self.text_color = (255, 255, 255)
        self.button_color = (80, 80, 80)
        self.button_hover_color = (100, 100, 100)
        self.button_active_color = (120, 120, 120)
        
        # Définition des boutons
        self.buttons = []
        self.init_buttons()
        
        # État actuel des contrôles
        self.active_button = None
        self.selected_terrain = "forest"
        self.edit_mode = "terrain"  # "terrain", "temperature", "humidity"
        
    def init_buttons(self):
        """Initialise tous les boutons de l'interface."""
        # Point de départ pour les boutons
        start_x = Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 20
        start_y = Config.SCREEN_HEIGHT - 100
        button_width = Config.UI_PANEL_WIDTH - 40
        button_height = 30
        button_margin = 10
        
        # Boutons de contrôle de simulation
        self.buttons.append({
            "rect": pygame.Rect(start_x, start_y, button_width, button_height),
            "text": "Pause/Reprendre",
            "action": "toggle_pause"
        })
        
        start_y += button_height + button_margin
        
        self.buttons.append({
            "rect": pygame.Rect(start_x, start_y, button_width, button_height),
            "text": "Réinitialiser",
            "action": "reset_simulation"
        })
        
        # Boutons pour les catastrophes naturelles
        start_y = Config.SCREEN_HEIGHT - 250
        button_width = (Config.UI_PANEL_WIDTH - 50) // 2
        
        self.buttons.append({
            "rect": pygame.Rect(start_x, start_y, button_width, button_height),
            "text": "Inondation",
            "action": "flood"
        })
        
        self.buttons.append({
            "rect": pygame.Rect(start_x + button_width + 10, start_y, button_width, button_height),
            "text": "Incendie",
            "action": "fire"
        })
        
        start_y += button_height + button_margin
        
        self.buttons.append({
            "rect": pygame.Rect(start_x, start_y, button_width, button_height),
            "text": "Sécheresse",
            "action": "drought"
        })
        
        self.buttons.append({
            "rect": pygame.Rect(start_x + button_width + 10, start_y, button_width, button_height),
            "text": "Météorite",
            "action": "meteor"
        })
        
        # Sélecteurs de mode d'édition
        start_y = 400
        mode_buttons_width = (Config.UI_PANEL_WIDTH - 50) // 3
        
        modes = [
            {"mode": "terrain", "text": "Terrain"},
            {"mode": "temperature", "text": "Température"},
            {"mode": "humidity", "text": "Humidité"}
        ]
        
        for i, mode in enumerate(modes):
            x_pos = start_x + i * (mode_buttons_width + 5)
            self.buttons.append({
                "rect": pygame.Rect(x_pos, start_y, mode_buttons_width, button_height),
                "text": mode["text"],
                "action": f"mode_{mode['mode']}",
                "mode": mode["mode"]
            })
        
        # Sélecteurs de terrain
        start_y = 450
        terrain_buttons_y = start_y
        terrain_button_size = 40
        
        terrains = [
            {"type": "water", "color": Config.ENVIRONMENTS["water"], "text": "Eau"},
            {"type": "desert", "color": Config.ENVIRONMENTS["desert"], "text": "Désert"},
            {"type": "forest", "color": Config.ENVIRONMENTS["forest"], "text": "Forêt"},
            {"type": "mountain", "color": Config.ENVIRONMENTS["mountain"], "text": "Montagne"}
        ]
        
        for i, terrain in enumerate(terrains):
            x_pos = start_x + i * (terrain_button_size + 10)
            self.buttons.append({
                "rect": pygame.Rect(x_pos, terrain_buttons_y, terrain_button_size, terrain_button_size),
                "color": terrain["color"],
                "text": terrain["text"],
                "action": f"select_terrain_{terrain['type']}",
                "terrain_type": terrain["type"]
            })
    
    def handle_click(self, pos):
        """Gère les clics sur l'interface utilisateur."""
        # Vérifier si le clic est dans la zone d'interface
        if not self.ui_panel.collidepoint(pos):
            return False
        
        # Vérifier si un bouton a été cliqué
        for button in self.buttons:
            if button["rect"].collidepoint(pos):
                self.active_button = button
                action = button["action"]
                
                # Traiter les actions spécifiques
                if action.startswith("select_terrain_"):
                    self.selected_terrain = button["terrain_type"]
                    return "select_terrain"
                elif action.startswith("mode_"):
                    self.edit_mode = button["mode"]
                    return "change_mode"
                
                # Retourne l'action associée au bouton
                return action
        
        return None
    
    def draw(self, game_loop):
        """Dessine tous les éléments de l'interface utilisateur."""
        # Dessiner les boutons
        for button in self.buttons:
            # Couleur du bouton
            color = button.get("color", self.button_color)
            
            # Vérifier si le bouton est actif (comme le mode d'édition ou le terrain sélectionné)
            is_active = False
            if "mode" in button and button["mode"] == self.edit_mode:
                is_active = True
            elif "terrain_type" in button and button["terrain_type"] == self.selected_terrain:
                is_active = True
            
            if is_active:
                color = self.button_active_color
            elif button["rect"].collidepoint(pygame.mouse.get_pos()):
                color = self.button_hover_color
            
            # Dessiner le fond du bouton
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, (200, 200, 200), button["rect"], 1)  # Bordure
            
            # Dessiner le texte du bouton
            if "text" in button:
                text_surface = self.font.render(button["text"], True, self.text_color)
                text_rect = text_surface.get_rect(center=button["rect"].center)
                self.screen.blit(text_surface, text_rect)
        
        # Afficher le mode d'édition actuel
        mode_text = self.title_font.render(f"Mode: {self.edit_mode.capitalize()}", True, self.text_color)
        self.screen.blit(mode_text, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 20, 350))
        
        # Afficher le terrain sélectionné en mode terrain
        if self.edit_mode == "terrain":
            terrain_text = self.font.render(f"Terrain: {self.selected_terrain.capitalize()}", True, self.text_color)
            self.screen.blit(terrain_text, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 20, 375))
    
    def get_selected_terrain(self):
        """Retourne le type de terrain actuellement sélectionné."""
        return self.selected_terrain
    
    def get_edit_mode(self):
        """Retourne le mode d'édition actuel."""
        return self.edit_mode
    
    def set_edit_mode(self, mode):
        """Change le mode d'édition."""
        if mode in ["terrain", "temperature", "humidity"]:
            self.edit_mode = mode
    
    def set_selected_terrain(self, terrain_type):
        """Change le type de terrain sélectionné."""
        if terrain_type in Config.ENVIRONMENTS:
            self.selected_terrain = terrain_type