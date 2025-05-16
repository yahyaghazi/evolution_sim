import pygame
import numpy as np
from config import Config

class Renderer:
    """
    Gère le rendu graphique de la simulation.
    Dessine la grille du monde, les créatures et l'interface utilisateur.
    """
    def __init__(self, screen, grid, population):
        self.screen = screen
        self.grid = grid
        self.population = population
        
        # Couleurs
        self.background_color = (0, 0, 0)
        self.ui_background_color = (30, 30, 30)
        self.text_color = (255, 255, 255)
        self.grid_line_color = (40, 40, 40)
        
        # Police pour le texte
        self.font = pygame.font.SysFont("Arial", 14)
        self.title_font = pygame.font.SysFont("Arial", 18, bold=True)
        
        # Instancier les contrôles UI
        from ui.controls import Controls
        self.controls = Controls(screen, grid)
        
        # Statistiques à afficher
        self.show_stats = True
        self.show_grid_lines = False
    
    def render_grid(self):
        """Dessine la grille du monde."""
        cell_size = Config.CELL_SIZE
        
        # Dessiner chaque cellule
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell(x, y)
                
                # Position et dimensions de la cellule
                rect = pygame.Rect(
                    x * cell_size,
                    y * cell_size,
                    cell_size,
                    cell_size
                )
                
                # Dessiner le fond de la cellule avec sa couleur de terrain
                pygame.draw.rect(self.screen, cell.color, rect)
                
                # Indicateur de nourriture (points verts)
                if cell.food > 0:
                    food_radius = min(cell_size // 4, int(cell.food))
                    pygame.draw.circle(
                        self.screen,
                        (0, 255, 0),
                        (x * cell_size + cell_size // 2, y * cell_size + cell_size // 2),
                        food_radius
                    )
                
                # Indicateur d'eau (teinte bleue)
                if cell.water > 0:
                    water_alpha = min(200, int(cell.water * 50))
                    water_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
                    water_surface.fill((0, 0, 255, water_alpha))
                    self.screen.blit(water_surface, rect)
                
                # Indicateurs d'états spéciaux
                if cell.special_state == "burning":
                    pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)
                elif cell.special_state == "flooded":
                    pygame.draw.rect(self.screen, (0, 0, 255), rect, 2)
                elif cell.special_state == "drought":
                    pygame.draw.rect(self.screen, (139, 69, 19), rect, 2)
        
        # Dessiner les lignes de la grille si activé
        if self.show_grid_lines:
            for x in range(self.grid.width + 1):
                pygame.draw.line(
                    self.screen,
                    self.grid_line_color,
                    (x * cell_size, 0),
                    (x * cell_size, self.grid.height * cell_size)
                )
            
            for y in range(self.grid.height + 1):
                pygame.draw.line(
                    self.screen,
                    self.grid_line_color,
                    (0, y * cell_size),
                    (self.grid.width * cell_size, y * cell_size)
                )
    
    def render_creatures(self):
        """Dessine toutes les créatures."""
        # Dessiner chaque créature à sa position
        for creature in self.population.creatures:
            creature.draw(self.screen)
    
    def render_ui(self, day_counter, paused):
        """Dessine l'interface utilisateur et les statistiques."""
        # Dessiner le panneau latéral
        panel_rect = pygame.Rect(
            Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH,
            0,
            Config.UI_PANEL_WIDTH,
            Config.SCREEN_HEIGHT
        )
        pygame.draw.rect(self.screen, self.ui_background_color, panel_rect)
        
        # Dessiner la barre de titre
        title_rect = pygame.Rect(
            Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH,
            0,
            Config.UI_PANEL_WIDTH,
            40
        )
        pygame.draw.rect(self.screen, (50, 50, 50), title_rect)
        
        # Titre de la simulation
        title_text = self.title_font.render("Simulation d'Évolution", True, self.text_color)
        self.screen.blit(
            title_text,
            (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, 10)
        )
        
        # Informations sur la simulation
        y_pos = 50
        
        # État de la simulation
        status_text = "PAUSE" if paused else "EN COURS"
        status_color = (255, 200, 0) if paused else (0, 255, 0)
        
        day_info = self.font.render(f"Jour: {day_counter}", True, self.text_color)
        status_info = self.font.render(f"État: {status_text}", True, status_color)
        
        self.screen.blit(day_info, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 20
        self.screen.blit(status_info, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 30
        
        # Statistiques de population
        pop_title = self.title_font.render("Population", True, self.text_color)
        self.screen.blit(pop_title, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 25
        
        # Nombre de créatures
        count_text = self.font.render(f"Créatures: {len(self.population.creatures)}", True, self.text_color)
        self.screen.blit(count_text, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 20
        
        # Génération actuelle
        gen_text = self.font.render(f"Génération: {self.population.generation}", True, self.text_color)
        self.screen.blit(gen_text, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 30
        
        # Conditions environnementales
        env_title = self.title_font.render("Environnement", True, self.text_color)
        self.screen.blit(env_title, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 25
        
        # Température et humidité moyennes
        avg_temp = 0
        avg_humidity = 0
        
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell(x, y)
                avg_temp += cell.temperature
                avg_humidity += cell.humidity
        
        avg_temp /= (self.grid.width * self.grid.height)
        avg_humidity /= (self.grid.width * self.grid.height)
        
        temp_text = self.font.render(f"Température: {avg_temp:.1f}°C", True, self.text_color)
        humid_text = self.font.render(f"Humidité: {avg_humidity:.1f}%", True, self.text_color)
        
        self.screen.blit(temp_text, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 20
        self.screen.blit(humid_text, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
        y_pos += 30
        
        # Résumé des statistiques d'évolution
        if self.show_stats:
            stats_title = self.title_font.render("Statistiques d'Évolution", True, self.text_color)
            self.screen.blit(stats_title, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
            y_pos += 25
            
            # Récupérer les statistiques de la population
            stats_summary = self.population.get_statistics()
            
            # Afficher le résumé des statistiques
            # Découper le texte en lignes
            stats_lines = stats_summary.split('\n')
            for line in stats_lines:
                if line.strip():  # Ignorer les lignes vides
                    stat_text = self.font.render(line, True, self.text_color)
                    self.screen.blit(stat_text, (Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH + 10, y_pos))
                    y_pos += 20
            
            y_pos += 10
        
        # Dessiner les contrôles de l'interface utilisateur (boutons, etc.)
        self.controls.draw(None)  # Le game_loop sera accédé via les événements
    
    def render_overlay_info(self, mouse_pos):
        """
        Affiche des informations contextuelles sur la cellule
        sous le curseur de la souris.
        """
        # Vérifier si la souris est sur la grille
        if mouse_pos[0] >= Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH:
            return
        
        # Convertir la position de la souris en coordonnées de grille
        grid_x = mouse_pos[0] // Config.CELL_SIZE
        grid_y = mouse_pos[1] // Config.CELL_SIZE
        
        # Vérifier que les coordonnées sont valides
        if 0 <= grid_x < self.grid.width and 0 <= grid_y < self.grid.height:
            cell = self.grid.get_cell(grid_x, grid_y)
            
            # Préparer les informations à afficher
            info_lines = [
                f"Position: ({grid_x}, {grid_y})",
                f"Terrain: {cell.terrain_type.capitalize()}",
                f"Température: {cell.temperature:.1f}°C",
                f"Humidité: {cell.humidity:.1f}%",
                f"Nourriture: {cell.food:.1f}",
                f"Eau: {cell.water:.1f}"
            ]
            
            if cell.special_state:
                info_lines.append(f"État: {cell.special_state.capitalize()} ({cell.state_duration})")
            
            # Créer une surface semi-transparente
            info_width = 180
            info_height = len(info_lines) * 20 + 10
            
            # Positionner l'info-bulle près de la souris, mais sans sortir de l'écran
            info_x = min(mouse_pos[0] + 10, Config.SCREEN_WIDTH - Config.UI_PANEL_WIDTH - info_width)
            info_y = min(mouse_pos[1] + 10, Config.SCREEN_HEIGHT - info_height)
            
            info_surface = pygame.Surface((info_width, info_height), pygame.SRCALPHA)
            info_surface.fill((0, 0, 0, 180))
            
            # Dessiner le cadre
            pygame.draw.rect(info_surface, (200, 200, 200), pygame.Rect(0, 0, info_width, info_height), 1)
            
            # Ajouter les lignes d'information
            for i, line in enumerate(info_lines):
                text = self.font.render(line, True, (255, 255, 255))
                info_surface.blit(text, (5, 5 + i * 20))
            
            # Afficher la surface
            self.screen.blit(info_surface, (info_x, info_y))
    
    def toggle_grid_lines(self):
        """Active ou désactive l'affichage des lignes de la grille."""
        self.show_grid_lines = not self.show_grid_lines
    
    def toggle_statistics(self):
        """Active ou désactive l'affichage des statistiques détaillées."""
        self.show_stats = not self.show_stats
    
    def render_help_overlay(self):
        """
        Affiche une aide contextuelle expliquant les contrôles
        et fonctionnalités du jeu.
        """
        # Créer une surface semi-transparente couvrant toute la fenêtre
        help_surface = pygame.Surface((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.SRCALPHA)
        help_surface.fill((0, 0, 0, 200))
        
        # Titre de l'aide
        title = self.title_font.render("AIDE - CONTRÔLES DU JEU", True, (255, 255, 255))
        title_pos = (Config.SCREEN_WIDTH // 2 - title.get_width() // 2, 30)
        
        # Sections d'aide
        sections = [
            {
                "title": "CONTRÔLES GÉNÉRAUX",
                "items": [
                    "ESPACE: Pause/Reprendre la simulation",
                    "S: Avancer d'un pas (en pause)",
                    "+/-: Ajuster la vitesse de simulation",
                    "H: Afficher/Masquer cette aide"
                ]
            },
            {
                "title": "ÉDITION DU MONDE",
                "items": [
                    "1: Mode Terrain (modifier le type de terrain)",
                    "2: Mode Température (modifier la température)",
                    "3: Mode Humidité (modifier l'humidité)",
                    "W/D/F/M: Sélectionner Eau/Désert/Forêt/Montagne",
                    "Clic gauche/droit: Augmenter/Diminuer la valeur",
                    "G: Afficher/Masquer les lignes de la grille"
                ]
            },
            {
                "title": "CATASTROPHES NATURELLES",
                "items": [
                    "F1: Déclencher une inondation",
                    "F2: Déclencher un incendie",
                    "F3: Déclencher une sécheresse"
                ]
            },
            {
                "title": "STATISTIQUES",
                "items": [
                    "TAB: Afficher/Masquer les statistiques détaillées",
                    "Survolez une cellule pour voir ses propriétés"
                ]
            }
        ]
        
        # Afficher le titre
        help_surface.blit(title, title_pos)
        
        # Afficher chaque section
        y_offset = 80
        for section in sections:
            # Titre de la section
            section_title = self.title_font.render(section["title"], True, (255, 200, 100))
            help_surface.blit(section_title, (Config.SCREEN_WIDTH // 4, y_offset))
            y_offset += 30
            
            # Éléments de la section
            for item in section["items"]:
                item_text = self.font.render(item, True, (220, 220, 220))
                help_surface.blit(item_text, (Config.SCREEN_WIDTH // 4 + 20, y_offset))
                y_offset += 20
            
            y_offset += 20
        
        # Message de fermeture
        close_text = self.font.render("Appuyez sur H pour fermer cette aide", True, (255, 255, 255))
        close_pos = (Config.SCREEN_WIDTH // 2 - close_text.get_width() // 2, Config.SCREEN_HEIGHT - 40)
        help_surface.blit(close_text, close_pos)
        
        # Afficher la surface d'aide
        self.screen.blit(help_surface, (0, 0))
    
    def render_debug_info(self, fps):
        """
        Affiche des informations de débogage, comme la fréquence d'images
        et les performances.
        """
        debug_text = self.font.render(f"FPS: {fps:.1f}", True, (255, 255, 0))
        self.screen.blit(debug_text, (10, 10))
        
        # Nombre de créatures
        creature_count = len(self.population.creatures)
        count_text = self.font.render(f"Créatures: {creature_count}", True, (255, 255, 0))
        self.screen.blit(count_text, (10, 30))