import pygame
import sys
from world.grid import Grid
from simulation.population import Population  # Correction: changement de creatures.population à simulation.population
from ui.renderer import Renderer
from ui.controls import Controls
from engine.event_handler import EventHandler
from config import Config

class GameLoop:
    """
    Gère la boucle principale du jeu et coordonne tous les composants.
    """
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        
        # Initialisation des composants principaux
        self.grid = Grid(Config.GRID_WIDTH, Config.GRID_HEIGHT)
        self.population = Population(self.grid)
        self.renderer = Renderer(self.screen, self.grid, self.population)
        self.controls = Controls(self.screen, self.grid)
        self.event_handler = EventHandler(self)
        
        # Variables de simulation
        self.paused = False
        self.step_mode = False
        self.simulation_speed = 1
        self.day_counter = 0
        self.frame_counter = 0
    
    def run(self):
        """Lance la boucle de jeu principale."""
        while self.running:
            # Gestion des événements
            self.event_handler.process_events()
            
            # Mise à jour de la logique si la simulation n'est pas en pause
            if not self.paused or self.step_mode:
                self.update()
                if self.step_mode:
                    self.paused = True
                    self.step_mode = False
            
            # Rendu
            self.render()
            
            # Limitation de la fréquence d'images
            self.clock.tick(Config.FPS * self.simulation_speed)
    
    def update(self):
        """Mise à jour de l'état de la simulation."""
        # Mise à jour de l'environnement (conditions climatiques, ressources)
        self.grid.update()
        
        # Mise à jour des créatures (déplacement, alimentation, reproduction)
        self.population.update()
        
        # Gestion du cycle jour/nuit
        self.frame_counter += 1
        if self.frame_counter >= Config.DAY_LENGTH:
            self.day_counter += 1
            self.frame_counter = 0
            self.population.end_day()  # Déclenche la reproduction, etc.
    
    def render(self):
        """Affichage de la simulation à l'écran."""
        # Effacement de l'écran
        self.screen.fill((0, 0, 0))
        
        # Rendu de la grille du monde
        self.renderer.render_grid()
        
        # Rendu des créatures
        self.renderer.render_creatures()
        
        # Rendu de l'interface utilisateur
        self.renderer.render_ui(self.day_counter, self.paused)
        
        # Mise à jour de l'affichage
        pygame.display.flip()
    
    def toggle_pause(self):
        """Mettre en pause ou reprendre la simulation."""
        self.paused = not self.paused
    
    def step_simulation(self):
        """Avancer la simulation d'un pas."""
        self.step_mode = True
        self.paused = False
    
    def adjust_speed(self, delta):
        """Ajuster la vitesse de la simulation."""
        new_speed = self.simulation_speed + delta
        if 0.25 <= new_speed <= 3:
            self.simulation_speed = new_speed