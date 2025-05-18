import numpy as np
from config import Config
from world.cell import Cell

class Grid:
    """
    Représente la grille 2D du monde de la simulation.
    Gère l'état environnemental de chaque cellule.
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = np.empty((width, height), dtype=object)
        
        # Initialisation des cellules
        self.initialize_cells()
        
        # Création de l'environnement initial
        self.generate_world()
        
        # Variables pour les conditions environnementales globales
        self.global_temperature = 20  # En degrés Celsius
        self.global_humidity = 50     # Pourcentage
        self.day_night_cycle = 0      # 0 = jour complet, 1 = nuit complète
    
    def initialize_cells(self):
        """Initialise chaque cellule de la grille."""
        for x in range(self.width):
            for y in range(self.height):
                self.cells[x, y] = Cell(x, y)
    
    def generate_world(self):
        """Génère une carte du monde aléatoire mais cohérente."""
        # Utilisation de bruit de Perlin pour générer un terrain naturel
        # Pour simplifier, j'utilise juste un générateur aléatoire de base ici
        for x in range(self.width):
            for y in range(self.height):
                # Distribution aléatoire pour cet exemple
                rand_val = np.random.random()
                
                if rand_val < 0.25:
                    terrain_type = "water"
                elif rand_val < 0.55:
                    terrain_type = "desert"
                elif rand_val < 0.85:
                    terrain_type = "forest"
                else:
                    terrain_type = "mountain"
                
                self.cells[x, y].terrain_type = terrain_type
                self.cells[x, y].color = Config.ENVIRONMENTS[terrain_type]
                
                # Définition de la température et l'humidité en fonction du terrain
                if terrain_type == "water":
                    temp = np.random.randint(15, 25)
                    humidity = np.random.randint(80, 100)
                elif terrain_type == "desert":
                    temp = np.random.randint(30, 45)
                    humidity = np.random.randint(5, 20)
                elif terrain_type == "forest":
                    temp = np.random.randint(20, 30)
                    humidity = np.random.randint(60, 80)
                else:  # mountain
                    temp = np.random.randint(0, 15)
                    humidity = np.random.randint(30, 60)
                
                self.cells[x, y].temperature = temp
                self.cells[x, y].humidity = humidity
    
    def update(self):
        """Met à jour l'état de la grille à chaque frame."""
        # Mise à jour des ressources (nourriture, etc.)
        self.update_resources()
        
        # Diffusion des conditions environnementales
        self.diffuse_environment()
        
        # Mise à jour du cycle jour/nuit
        self.update_day_night_cycle()

        # Dégradation des ressources
        self.degrade_resources()
    
    def update_resources(self):
        """Met à jour les ressources de chaque cellule."""
        for x in range(self.width):
            for y in range(self.height):
                # Probabilité de génération de nourriture basée sur le type de terrain
                cell = self.cells[x, y]
                
                # Régénération de nourriture basée sur le type de terrain
                if np.random.random() < Config.FOOD_SPAWN_RATE:
                    if cell.terrain_type == "water":
                        cell.food += np.random.randint(1, 3)
                    elif cell.terrain_type == "desert":
                        cell.food += np.random.randint(0, 2)
                    elif cell.terrain_type == "forest":
                        cell.food += np.random.randint(2, 5)
                    elif cell.terrain_type == "mountain":
                        cell.food += np.random.randint(0, 2)
                
                # Limiter la quantité maximale de nourriture par cellule
                cell.food = min(cell.food, 10)
    
    def diffuse_environment(self):
        """Diffuse les conditions environnementales entre cellules voisines."""
        # Pour une version simple, nous allons juste stabiliser légèrement
        # vers la moyenne des cellules voisines
        temp_grid = np.zeros((self.width, self.height))
        humidity_grid = np.zeros((self.width, self.height))
        
        # Calcul des moyennes
        for x in range(self.width):
            for y in range(self.height):
                neighbors_temp = []
                neighbors_humidity = []
                
                # Vérification des 8 cellules voisines
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            neighbors_temp.append(self.cells[nx, ny].temperature)
                            neighbors_humidity.append(self.cells[nx, ny].humidity)
                
                # Calculer les moyennes
                temp_grid[x, y] = np.mean(neighbors_temp)
                humidity_grid[x, y] = np.mean(neighbors_humidity)
        
        # Application des changements avec lissage
        diffusion_rate = 0.1  # Taux de diffusion (0-1)
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x, y]
                cell.temperature = cell.temperature * (1 - diffusion_rate) + temp_grid[x, y] * diffusion_rate
                cell.humidity = cell.humidity * (1 - diffusion_rate) + humidity_grid[x, y] * diffusion_rate
    
    def update_day_night_cycle(self):
        """Met à jour le cycle jour/nuit."""
        # Incrémentation simple pour cet exemple
        self.day_night_cycle = (self.day_night_cycle + 0.001) % 1.0
        
        # La température globale varie selon le cycle jour/nuit
        time_modifier = np.sin(self.day_night_cycle * 2 * np.pi)
        self.global_temperature = 20 + 10 * time_modifier
    
    def set_cell_type(self, x, y, terrain_type):
        """Change le type de terrain d'une cellule."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cells[x, y].terrain_type = terrain_type
            self.cells[x, y].color = Config.ENVIRONMENTS[terrain_type]
            
            # Ajustement des conditions environnementales en fonction du nouveau terrain
            if terrain_type == "water":
                self.cells[x, y].temperature = 20
                self.cells[x, y].humidity = 90
            elif terrain_type == "desert":
                self.cells[x, y].temperature = 40
                self.cells[x, y].humidity = 10
            elif terrain_type == "forest":
                self.cells[x, y].temperature = 25
                self.cells[x, y].humidity = 70
            elif terrain_type == "mountain":
                self.cells[x, y].temperature = 10
                self.cells[x, y].humidity = 40
    
    def adjust_temperature(self, x, y, delta):
        """Modifie la température d'une cellule."""
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.cells[x, y]
            cell.temperature += delta
            # Limiter à des valeurs raisonnables
            cell.temperature = max(-20, min(50, cell.temperature))
    
    def adjust_humidity(self, x, y, delta):
        """Modifie l'humidité d'une cellule."""
        if 0 <= x < self.width and 0 <= y < self.height:
            cell = self.cells[x, y]
            cell.humidity += delta
            # Limiter à des valeurs raisonnables (pourcentage)
            cell.humidity = max(0, min(100, cell.humidity))
    
    def get_cell(self, x, y):
        """Récupère une cellule à une position donnée."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[x, y]
        return None
    
    def get_neighbors(self, x, y, radius=1):
        """Récupère les cellules voisines dans un certain rayon."""
        neighbors = []
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height and (dx != 0 or dy != 0):
                    neighbors.append(self.cells[nx, ny])
        return neighbors
    
    def trigger_flood(self):
        """Déclenche une inondation sur une partie de la carte."""
        # Choisir un point de départ aléatoire pour l'inondation
        center_x = np.random.randint(self.width)
        center_y = np.random.randint(self.height)
        flood_radius = np.random.randint(5, 15)
        
        # Convertir les cellules dans le rayon en eau
        for x in range(max(0, center_x - flood_radius), min(self.width, center_x + flood_radius + 1)):
            for y in range(max(0, center_y - flood_radius), min(self.height, center_y + flood_radius + 1)):
                # Distance au centre
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                if distance <= flood_radius:
                    # Probabilité décroissante avec la distance
                    if np.random.random() < (1 - distance / flood_radius):
                        self.set_cell_type(x, y, "water")
    
    def trigger_fire(self):
        """Déclenche un incendie sur une partie de la carte."""
        # Choisir un point de départ aléatoire pour l'incendie
        center_x = np.random.randint(self.width)
        center_y = np.random.randint(self.height)
        fire_radius = np.random.randint(5, 10)
        
        # Les incendies affectent principalement les forêts
        for x in range(max(0, center_x - fire_radius), min(self.width, center_x + fire_radius + 1)):
            for y in range(max(0, center_y - fire_radius), min(self.height, center_y + fire_radius + 1)):
                cell = self.cells[x, y]
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                
                if distance <= fire_radius:
                    # Les forêts brûlent et deviennent des déserts
                    if cell.terrain_type == "forest" and np.random.random() < (1 - distance / fire_radius):
                        self.set_cell_type(x, y, "desert")
                    
                    # Augmenter la température et réduire l'humidité dans la zone
                    self.adjust_temperature(x, y, 10 * (1 - distance / fire_radius))
                    self.adjust_humidity(x, y, -20 * (1 - distance / fire_radius))
    
    def trigger_drought(self):
        """Déclenche une sécheresse sur toute la carte."""
        # Une sécheresse affecte l'humidité et la nourriture
        for x in range(self.width):
            for y in range(self.height):
                cell = self.cells[x, y]
                
                # Réduire drastiquement l'humidité
                reduction = np.random.randint(30, 60)
                self.adjust_humidity(x, y, -reduction)
                
                # Réduire la nourriture disponible
                cell.food = max(0, cell.food - np.random.randint(1, 3))
                
                # Possibilité de transformer l'eau peu profonde en désert
                if cell.terrain_type == "water" and np.random.random() < 0.2:
                    self.set_cell_type(x, y, "desert")

    def degrade_resources(self):
        """Dégrade périodiquement les ressources pour simuler l'épuisement naturel."""
        # Appliquer tous les X frames (par exemple tous les 50 frames)
        if self.frame_counter % 50 == 0:
            for x in range(self.width):
                for y in range(self.height):
                    cell = self.cells[x, y]
                    # Réduire la nourriture de 5-10%
                    cell.food *= 0.9 + np.random.random() * 0.05
                    # Réduire l'eau sauf dans les cellules d'eau
                    if cell.terrain_type != "water":
                        cell.water *= 0.9 + np.random.random() * 0.05