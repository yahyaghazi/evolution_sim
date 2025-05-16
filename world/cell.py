class Cell:
    """
    Représente une cellule individuelle dans la grille du monde.
    Contient des informations sur le terrain, les conditions environnementales
    et les ressources disponibles.
    """
    def __init__(self, x, y):
        # Position dans la grille
        self.x = x
        self.y = y
        
        # Type de terrain et propriétés visuelles
        self.terrain_type = "forest"  # Par défaut
        self.color = (34, 139, 34)    # Vert forêt par défaut
        
        # Conditions environnementales
        self.temperature = 20   # En degrés Celsius
        self.humidity = 50      # Pourcentage
        self.elevation = 0      # En mètres
        
        # Ressources disponibles
        self.food = 0           # Quantité de nourriture
        self.water = 0          # Quantité d'eau
        
        # État spécial (pour les catastrophes naturelles, etc.)
        self.special_state = None  # None, "burning", "flooded", etc.
        self.state_duration = 0    # Durée restante de l'état spécial
    
    def get_habitability(self):
        """
        Calcule un score d'habitabilité pour cette cellule.
        Représente à quel point cette cellule est adaptée à la vie.
        """
        # Exemple de calcul simple d'habitabilité
        habitability = 0
        
        # Contribution du type de terrain
        if self.terrain_type == "water":
            habitability += 3  # Bon pour certaines espèces
        elif self.terrain_type == "forest":
            habitability += 5  # Très bon pour la plupart des espèces
        elif self.terrain_type == "desert":
            habitability += 1  # Difficile pour la plupart des espèces
        elif self.terrain_type == "mountain":
            habitability += 2  # Difficile mais viable
        
        # Contribution de la température (préférence pour 15-25°C)
        temp_factor = 0
        if 15 <= self.temperature <= 25:
            temp_factor = 1.0
        elif 5 <= self.temperature < 15 or 25 < self.temperature <= 35:
            temp_factor = 0.5
        else:
            temp_factor = 0.1
        
        # Contribution de l'humidité (préférence pour 40-70%)
        humidity_factor = 0
        if 40 <= self.humidity <= 70:
            humidity_factor = 1.0
        elif 20 <= self.humidity < 40 or 70 < self.humidity <= 90:
            humidity_factor = 0.5
        else:
            humidity_factor = 0.2
        
        # Calcul final avec ressources
        habitability = habitability * temp_factor * humidity_factor
        habitability += self.food * 0.5  # Bonus pour la nourriture disponible
        
        # Pénalité pour les états spéciaux
        if self.special_state in ["burning", "flooded", "drought"]:
            habitability *= 0.2
        
        return habitability
    
    def update(self):
        """Met à jour l'état de la cellule pour chaque frame."""
        # Mise à jour des états spéciaux
        if self.special_state and self.state_duration > 0:
            self.state_duration -= 1
            if self.state_duration <= 0:
                self.special_state = None
        
        # Ajustement de l'eau en fonction de l'humidité
        if self.humidity > 70 and self.terrain_type != "water":
            self.water = max(5, self.water)
        elif self.humidity < 30:
            self.water = max(0, self.water - 0.1)