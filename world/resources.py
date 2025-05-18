class Resources:
    """
    Gère les ressources disponibles dans le monde de la simulation.
    S'occupe de la génération et distribution des ressources comme la nourriture, l'eau, etc.
    """
    def __init__(self, grid):
        self.grid = grid
        
        # Liste des types de ressources
        self.resource_types = ["food", "water"]
        
        # Paramètres de régénération des ressources
        self.regeneration_rates = {
            "food": {
                "water": 0.02,      # Taux de régénération dans l'eau
                "desert": 0.005,    # Taux de régénération dans le désert
                "forest": 0.03,     # Taux de régénération dans la forêt
                "mountain": 0.01    # Taux de régénération dans les montagnes
            },
            "water": {
                "water": 0.05,      # Taux de régénération dans l'eau
                "desert": 0.001,    # Taux de régénération dans le désert
                "forest": 0.02,     # Taux de régénération dans la forêt
                "mountain": 0.01    # Taux de régénération dans les montagnes
            }
        }
        
        # Capacité maximale de chaque ressource par type de terrain
        self.max_capacity = {
            "food": {
                "water": 2,         # Capacité maximale dans l'eau
                "desert": 1,        # Capacité maximale dans le désert
                "forest": 4,       # Capacité maximale dans la forêt
                "mountain": 1       # Capacité maximale dans les montagnes
            },
            "water": {
                "water": 5,        # Capacité maximale dans l'eau
                "desert": 0.5,        # Capacité maximale dans le désert
                "forest": 2,        # Capacité maximale dans la forêt
                "mountain": 1       # Capacité maximale dans les montagnes
            }
        }
        
        # Initialiser les ressources sur la grille
        self.initialize_resources()
    
    def initialize_resources(self):
        """Initialise les ressources sur toute la grille."""
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell(x, y)
                if cell:
                    terrain_type = cell.terrain_type
                    
                    # Initialiser chaque type de ressource
                    for resource_type in self.resource_types:
                        # Quantité initiale basée sur le type de terrain et un facteur aléatoire
                        max_amount = self.max_capacity[resource_type][terrain_type]
                        initial_amount = max_amount * 0.5  # 50% de la capacité maximale
                        
                        # Ajouter un peu de randomisation
                        if resource_type == "food":
                            cell.food = initial_amount
                        elif resource_type == "water":
                            cell.water = initial_amount
    
    def update(self):
        """Met à jour les ressources sur toute la grille à chaque frame."""
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self.update_cell_resources(x, y)
    
    def update_cell_resources(self, x, y):
        """Met à jour les ressources pour une cellule spécifique."""
        cell = self.grid.get_cell(x, y)
        if not cell:
            return
        
        terrain_type = cell.terrain_type
        
        # Mise à jour de chaque type de ressource
        for resource_type in self.resource_types:
            # Déterminer le taux de régénération
            regen_rate = self.regeneration_rates[resource_type][terrain_type]
            max_amount = self.max_capacity[resource_type][terrain_type]
            
            # Appliquer la régénération en fonction de l'humidité
            humidity_factor = 1.0
            if cell.humidity > 70:
                humidity_factor = 1.5  # Plus d'humidité = plus de régénération
            elif cell.humidity < 30:
                humidity_factor = 0.5  # Moins d'humidité = moins de régénération
            
            # Calculer la quantité à ajouter
            if resource_type == "food":
                # Facteur de croissance aléatoire
                if cell.food < max_amount and self.grid.day_night_cycle < 0.5:  # Croissance le jour
                    growth = regen_rate * humidity_factor
                    cell.food = min(cell.food + growth, max_amount)
                    
            elif resource_type == "water":
                # L'eau s'accumule en fonction de l'humidité
                if cell.water < max_amount and cell.humidity > 50:
                    accumulation = regen_rate * (cell.humidity / 50)
                    cell.water = min(cell.water + accumulation, max_amount)
                
                # L'eau s'évapore si la température est élevée
                if cell.temperature > 30:
                    evaporation = 0.01 * (cell.temperature - 30) / 20
                    cell.water = max(0, cell.water - evaporation)
    
    def add_resource(self, x, y, resource_type, amount):
        """Ajoute une quantité spécifique d'une ressource à une cellule."""
        cell = self.grid.get_cell(x, y)
        if not cell:
            return
        
        if resource_type == "food":
            cell.food = min(cell.food + amount, self.max_capacity["food"][cell.terrain_type])
        elif resource_type == "water":
            cell.water = min(cell.water + amount, self.max_capacity["water"][cell.terrain_type])
    
    def remove_resource(self, x, y, resource_type, amount):
        """Retire une quantité spécifique d'une ressource d'une cellule."""
        cell = self.grid.get_cell(x, y)
        if not cell:
            return
        
        if resource_type == "food":
            cell.food = max(0, cell.food - amount)
        elif resource_type == "water":
            cell.water = max(0, cell.water - amount)
    
    def get_resource_amount(self, x, y, resource_type):
        """Récupère la quantité d'une ressource spécifique à une position donnée."""
        cell = self.grid.get_cell(x, y)
        if not cell:
            return 0
        
        if resource_type == "food":
            return cell.food
        elif resource_type == "water":
            return cell.water
        
        return 0
    
    def apply_disaster_effects(self, disaster_type):
        """Applique les effets d'une catastrophe naturelle sur les ressources."""
        if disaster_type == "drought":
            # Une sécheresse réduit l'eau et la nourriture
            for x in range(self.grid.width):
                for y in range(self.grid.height):
                    cell = self.grid.get_cell(x, y)
                    if cell:
                        cell.water *= 0.3  # Réduit l'eau à 30%
                        cell.food *= 0.5   # Réduit la nourriture à 50%
        
        elif disaster_type == "fire":
            # Un incendie détruit la nourriture dans les zones touchées
            # Cette logique est gérée par la méthode grid.trigger_fire()
            pass
        
        elif disaster_type == "flood":
            # Une inondation augmente l'eau mais peut réduire la nourriture
            # Cette logique est gérée par la méthode grid.trigger_flood()
            pass