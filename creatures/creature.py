import numpy as np
import pygame
from creatures.genome import Genome
from config import Config

class Creature:
    """
    Représente une créature autonome dans la simulation.
    Possède un génome, un comportement et interagit avec l'environnement.
    """
    def __init__(self, grid, x, y, genome=None):
        self.grid = grid
        self.x = x  # Position x dans la grille (peut être à virgule flottante)
        self.y = y  # Position y dans la grille (peut être à virgule flottante)
        
        # Création du génome (aléatoire si non fourni)
        self.genome = genome if genome else Genome()
        
        # États et statistiques de la créature
        self.energy = 100.0        # Niveau d'énergie actuel
        self.health = 100.0        # Niveau de santé actuel
        self.age = 0               # Âge en jours
        self.max_age = np.random.randint(10, 20)  # Durée de vie maximale
        self.reproduction_cooldown = 0  # Temps avant de pouvoir se reproduire à nouveau
        
        # Variables de comportement
        self.target = None         # Cible actuelle (nourriture, partenaire...)
        self.direction = (0, 0)    # Direction de déplacement
        self.state = "exploring"   # État comportemental (exploring, hunting, fleeing...)
    
    def update(self):
        """Met à jour l'état de la créature à chaque frame."""
        # Vieillissement et consommation d'énergie
        self.age += 1 / Config.DAY_LENGTH  # Incrémenter l'âge d'une fraction de jour
        self.energy -= self.genome.get_metabolic_rate() * 0.1  # Consommation d'énergie de base
        
        # Mise à jour des cooldowns
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1
        
        # Décision du comportement
        self.decide_behavior()
        
        # Exécution du comportement actuel
        self.execute_behavior()
        
        # Vérification de la mort (âge, énergie ou santé)
        if self.is_dead():
            return False  # La créature est morte
            
        return True  # La créature est vivante
    
    def decide_behavior(self):
        """Décide du comportement de la créature en fonction de son état."""
        # Priorisation des besoins
        if self.energy < 30:
            # Besoin urgent de nourriture
            self.state = "hunting"
            self.find_food()
        elif self.is_ready_to_reproduce() and np.random.random() < 0.1:
            # Chercher un partenaire pour la reproduction
            self.state = "mating"
            # La recherche de partenaire sera implémentée plus tard
        else:
            # Exploration normale
            self.state = "exploring"
            if np.random.random() < 0.05:
                # Changer aléatoirement de direction de temps en temps
                self.set_random_direction()
    
    def execute_behavior(self):
        """Exécute le comportement actuel de la créature."""
        if self.state == "exploring":
            self.move()
        elif self.state == "hunting":
            self.move_towards_target()
            self.eat()
        elif self.state == "fleeing":
            self.flee()
        elif self.state == "mating":
            self.move_towards_target()
            # La reproduction sera traitée par la classe Population
    
    def move(self):
        """Déplace la créature dans sa direction actuelle."""
        speed = self.genome.get_speed()
        
        # Si pas de direction définie, en choisir une aléatoire
        if self.direction == (0, 0):
            self.set_random_direction()
        
        # Calcul de la nouvelle position
        new_x = self.x + self.direction[0] * speed
        new_y = self.y + self.direction[1] * speed
        
        # Vérification des limites du monde
        if 0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height:
            # Vérifier si la créature peut se déplacer dans ce type de terrain
            cell = self.grid.get_cell(int(new_x), int(new_y))
            if cell.terrain_type == "water" and not self.genome.traits["can_swim"]:
                # La créature ne peut pas nager, changer de direction
                self.set_random_direction()
            elif cell.terrain_type == "mountain" and not self.genome.traits["can_climb"]:
                # La créature ne peut pas grimper, changer de direction
                self.set_random_direction()
            else:
                # Déplacement possible
                self.x = new_x
                self.y = new_y
                
                # Consommation d'énergie liée au déplacement
                terrain_cost = {
                    "water": 0.2 if self.genome.traits["can_swim"] else 0.5,
                    "desert": 0.3,
                    "forest": 0.1,
                    "mountain": 0.3 if self.genome.traits["can_climb"] else 0.6
                }
                
                energy_cost = speed * terrain_cost.get(cell.terrain_type, 0.2)
                self.energy -= energy_cost
        else:
            # Rebondir aux limites du monde
            self.set_random_direction()
    
    def set_random_direction(self):
        """Définit une direction aléatoire pour la créature."""
        angle = np.random.random() * 2 * np.pi
        self.direction = (np.cos(angle), np.sin(angle))
    
    def find_food(self):
        """Cherche de la nourriture dans le rayon de vision."""
        vision_range = self.genome.get_vision_range()
        best_food_cell = None
        best_food_value = 0
        
        # Parcourir les cellules dans le rayon de vision
        for dx in range(-vision_range, vision_range + 1):
            for dy in range(-vision_range, vision_range + 1):
                cell_x, cell_y = int(self.x) + dx, int(self.y) + dy
                
                # Vérifier les limites de la grille
                if 0 <= cell_x < self.grid.width and 0 <= cell_y < self.grid.height:
                    cell = self.grid.get_cell(cell_x, cell_y)
                    
                    # Calculer la distance
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance > vision_range:
                        continue
                    
                    # Si la cellule contient de la nourriture
                    if cell.food > 0:
                        # Évaluer l'attractivité de cette source de nourriture
                        food_value = cell.food / (distance + 1)
                        
                        # Tenir compte de l'adaptation environnementale
                        env_fitness = self.genome.calculate_environmental_fitness(cell)
                        food_value *= env_fitness
                        
                        if food_value > best_food_value:
                            best_food_value = food_value
                            best_food_cell = (cell_x, cell_y)
        
        # Si de la nourriture a été trouvée, la définir comme cible
        if best_food_cell:
            self.target = best_food_cell
        else:
            # Pas de nourriture trouvée, continuer à explorer
            self.state = "exploring"
    
    def move_towards_target(self):
        """Déplace la créature vers sa cible actuelle."""
        if not self.target:
            return
        
        # Calculer la direction vers la cible
        dx = self.target[0] - self.x
        dy = self.target[1] - self.y
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance < 0.1:
            # Cible atteinte
            if self.state == "hunting":
                self.eat()
            return
        
        # Normaliser la direction
        self.direction = (dx / distance, dy / distance)
        
        # Se déplacer
        self.move()
    
    def eat(self):
        """Tente de manger de la nourriture à la position actuelle."""
        cell_x, cell_y = int(self.x), int(self.y)
        cell = self.grid.get_cell(cell_x, cell_y)
        
        if cell and cell.food > 0:
            # Manger la nourriture
            food_eaten = min(cell.food, 5)  # Manger au maximum 5 unités de nourriture
            cell.food -= food_eaten
            
            # Gain d'énergie
            self.energy += food_eaten * 5
            
            # Limiter l'énergie maximale
            self.energy = min(self.energy, 100)
            
            # Réinitialiser la cible
            self.target = None
            self.state = "exploring"
    
    def flee(self):
        """Fuite face à un danger."""
        if not self.target:  # Le danger est la cible dans ce cas
            return
            
        # Fuir dans la direction opposée au danger
        dx = self.x - self.target[0]
        dy = self.y - self.target[1]
        distance = np.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.direction = (dx / distance, dy / distance)
        
        # Se déplacer plus rapidement en fuyant
        speed_boost = 1.5
        speed = self.genome.get_speed() * speed_boost
        
        new_x = self.x + self.direction[0] * speed
        new_y = self.y + self.direction[1] * speed
        
        # Vérifier les limites et déplacer
        if 0 <= new_x < self.grid.width and 0 <= new_y < self.grid.height:
            self.x = new_x
            self.y = new_y
            
            # Consommation d'énergie augmentée pour la fuite
            self.energy -= speed * 0.3
    
    def is_ready_to_reproduce(self):
        """Vérifie si la créature est prête à se reproduire."""
        return (
            self.reproduction_cooldown <= 0 and
            self.energy > 70 and  # Besoin de beaucoup d'énergie pour se reproduire
            self.age > 3  # Avoir atteint un âge minimal
        )
    
    def reproduce(self, partner):
        """
        Effectue la reproduction avec un partenaire.
        Retourne un nouvel objet Creature issu du croisement des génomes.
        """
        # Création du génome de l'enfant par croisement
        child_genome = Genome.crossover(self.genome, partner.genome)
        
        # Position de l'enfant (près des parents)
        child_x = (self.x + partner.x) / 2 + np.random.uniform(-1, 1)
        child_y = (self.y + partner.y) / 2 + np.random.uniform(-1, 1)
        
        # Assurer que l'enfant est dans les limites du monde
        child_x = max(0, min(self.grid.width - 1, child_x))
        child_y = max(0, min(self.grid.height - 1, child_y))
        
        # Création de la nouvelle créature
        child = Creature(self.grid, child_x, child_y, child_genome)
        
        # Épuisement des parents après la reproduction
        self.energy -= 30
        partner.energy -= 30
        
        # Cooldown de reproduction
        self.reproduction_cooldown = int(Config.DAY_LENGTH * (1 - self.genome.traits["reproduction_rate"] / 100))
        partner.reproduction_cooldown = int(Config.DAY_LENGTH * (1 - partner.genome.traits["reproduction_rate"] / 100))
        
        return child
    
    def is_dead(self):
        """Vérifie si la créature est morte."""
        return (
            self.energy <= 0 or     # Mort de faim
            self.health <= 0 or     # Mort de blessures
            self.age >= self.max_age  # Mort de vieillesse
        )
    
    def draw(self, surface, offset_x=0, offset_y=0, cell_size=Config.CELL_SIZE):
        """Dessine la créature sur une surface pygame."""
        # Calculer la position à l'écran
        screen_x = int(self.x * cell_size) + offset_x
        screen_y = int(self.y * cell_size) + offset_y
        
        # Taille de la créature basée sur son génome
        size = int(self.genome.get_size())
        
        # Couleur de la créature basée sur son génome
        color = self.genome.get_color()
        
        # Dessiner le corps de la créature
        pygame.draw.circle(surface, color, (screen_x, screen_y), size)
        
        # Dessiner une indication de la direction
        direction_x = screen_x + int(self.direction[0] * size * 1.2)
        direction_y = screen_y + int(self.direction[1] * size * 1.2)
        pygame.draw.line(surface, (0, 0, 0), (screen_x, screen_y), (direction_x, direction_y), max(1, size // 3))
        
        # Dessiner un indicateur d'état (couleur variant selon l'état)
        state_colors = {
            "exploring": (255, 255, 255),  # Blanc
            "hunting": (255, 0, 0),        # Rouge
            "fleeing": (255, 255, 0),      # Jaune
            "mating": (255, 0, 255)        # Magenta
        }
        
        state_color = state_colors.get(self.state, (128, 128, 128))
        indicator_size = max(1, size // 3)
        pygame.draw.circle(surface, state_color, (screen_x, screen_y - size), indicator_size)
        
        # Dessiner une barre d'énergie au-dessus de la créature
        energy_width = size * 2
        energy_height = 2
        energy_x = screen_x - size
        energy_y = screen_y - size - 5
        
        # Fond de la barre d'énergie
        pygame.draw.rect(surface, (64, 64, 64), (energy_x, energy_y, energy_width, energy_height))
        
        # Barre d'énergie actuelle
        energy_fill_width = int(energy_width * (self.energy / 100))
        pygame.draw.rect(surface, (0, 255, 0), (energy_x, energy_y, energy_fill_width, energy_height))