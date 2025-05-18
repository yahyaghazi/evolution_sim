import pygame
import sys
from config import Config

class EventHandler:
    """
    Gère les événements d'entrée (clavier, souris) dans le jeu.
    """
    def __init__(self, game_loop):
        self.game_loop = game_loop
        self.grid = game_loop.grid
        self.controls = game_loop.controls
        
        # État de la souris
        self.mouse_pressed = False
        self.last_mouse_pos = (0, 0)
        
        # Mode d'édition actuel
        self.edit_mode = "terrain"  # "terrain", "temperature", "humidity"
        self.selected_terrain = "forest"
        
    def process_events(self):
        """Traite tous les événements pygame."""
        for event in pygame.event.get():
            # Quitter le jeu
            if event.type == pygame.QUIT:
                self.game_loop.running = False
                
            # Événements clavier
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
                
            # Événements souris
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pressed = True
                self.handle_mouse_down(event)
                
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed = False
                
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    self.handle_mouse_drag(event)
                self.last_mouse_pos = event.pos
        
    def handle_keydown(self, event):
        """Gère les événements de touche pressée."""
        # Contrôles de simulation
        if event.key == pygame.K_SPACE:
            self.game_loop.toggle_pause()
        elif event.key == pygame.K_s:
            self.game_loop.step_simulation()
        elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
            self.game_loop.adjust_speed(1)
        elif event.key == pygame.K_MINUS:
            self.game_loop.adjust_speed(-1)
            
        # Sélection du mode d'édition
        elif event.key == pygame.K_1:
            self.edit_mode = "terrain"
        elif event.key == pygame.K_2:
            self.edit_mode = "temperature"
        elif event.key == pygame.K_3:
            self.edit_mode = "humidity"
            
        # Sélection du type de terrain
        elif event.key == pygame.K_w:
            self.selected_terrain = "water"
        elif event.key == pygame.K_d:
            self.selected_terrain = "desert"
        elif event.key == pygame.K_f:
            self.selected_terrain = "forest"
        elif event.key == pygame.K_m:
            self.selected_terrain = "mountain"
            
        # Catastrophes naturelles
        elif event.key == pygame.K_F1:
            # Déclencher une inondation
            self.trigger_disaster("flood")
        elif event.key == pygame.K_F2:
            # Déclencher un incendie
            self.trigger_disaster("fire")
        elif event.key == pygame.K_F3:
            # Déclencher une sécheresse
            self.trigger_disaster("drought")
    
    def handle_mouse_down(self, event):
        """Gère les clics de souris."""
        # Vérifier si le clic est dans la zone d'interface utilisateur
        if event.pos[0] > Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH:
            self.controls.handle_click(event.pos)
        else:
            # Modifier le monde en fonction du mode d'édition actuel
            self.modify_world_at_position(event.pos)
    
    def handle_mouse_drag(self, event):
        """Gère les événements de glissement de souris."""
        # Ne pas modifier le monde si on est dans la zone d'interface
        if event.pos[0] <= Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH:
            self.modify_world_at_position(event.pos)
    
    def modify_world_at_position(self, pos):
        """Modifie le monde à la position donnée en fonction du mode d'édition."""
        # Convertir la position de l'écran en position de grille
        grid_x = pos[0] // Config.CELL_SIZE
        grid_y = pos[1] // Config.CELL_SIZE
        
        # Vérifier que la position est dans les limites de la grille
        if 0 <= grid_x < Config.GRID_WIDTH and 0 <= grid_y < Config.GRID_HEIGHT:
            if self.edit_mode == "terrain":
                self.grid.set_cell_type(grid_x, grid_y, self.selected_terrain)
            elif self.edit_mode == "temperature":
                # Augmenter la température en cliquant, la diminuer avec le bouton droit
                delta = 5 if pygame.mouse.get_pressed()[0] else -5
                self.grid.adjust_temperature(grid_x, grid_y, delta)
            elif self.edit_mode == "humidity":
                # Augmenter l'humidité en cliquant, la diminuer avec le bouton droit
                delta = 5 if pygame.mouse.get_pressed()[0] else -5
                self.grid.adjust_humidity(grid_x, grid_y, delta)
    
    def trigger_disaster(self, disaster_type):
        """Déclenche une catastrophe naturelle sur la carte."""
        # Implémentation de base des catastrophes
        if disaster_type == "flood":
            self.grid.trigger_flood()
        elif disaster_type == "fire":
            self.grid.trigger_fire()
        elif disaster_type == "drought":
            self.grid.trigger_drought()