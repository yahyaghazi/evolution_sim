import numpy as np
from config import Config

class Environment:
    """
    Gère les conditions environnementales du monde.
    Contrôle le climat, les cycles jour/nuit et les catastrophes naturelles.
    """
    def __init__(self, grid):
        self.grid = grid
        
        # Paramètres climatiques globaux
        self.base_temperature = 20  # Température de base en °C
        self.base_humidity = 50     # Humidité de base en %
        
        # Variations saisonnières
        self.season_cycle = 0       # 0 = printemps, 0.25 = été, 0.5 = automne, 0.75 = hiver
        self.season_length = 90     # Durée d'une saison en jours
        
        # Cycle jour/nuit
        self.day_night_cycle = 0    # 0 = midi, 0.5 = minuit
        self.day_length = Config.DAY_LENGTH  # Durée d'un jour en frames
        
        # Variations climatiques
        self.global_warming = 0     # Réchauffement climatique progressif
        self.weather_systems = []   # Systèmes météorologiques actifs
        
        # Historique des catastrophes
        self.disaster_history = []
        
        # Probabilités de catastrophes naturelles
        self.disaster_probs = {
            "flood": 0.001,         # Probabilité quotidienne d'inondation
            "fire": 0.001,          # Probabilité quotidienne d'incendie
            "drought": 0.0005,      # Probabilité quotidienne de sécheresse
            "meteor": 0.0001        # Probabilité quotidienne d'impact de météorite
        }
    
    def update(self):
        """Met à jour les conditions environnementales à chaque frame."""
        # Mise à jour du cycle jour/nuit
        self.update_day_night_cycle()
        
        # Mise à jour des saisons
        self.update_seasons()
        
        # Mise à jour des systèmes météorologiques
        self.update_weather_systems()
        
        # Possibilité de catastrophes naturelles
        self.check_for_disasters()
        
        # Appliquer les variations climatiques à la grille
        self.apply_environmental_conditions()
    
    def update_day_night_cycle(self):
        """Met à jour le cycle jour/nuit."""
        # Avancer dans le cycle jour/nuit
        self.day_night_cycle = (self.day_night_cycle + 1 / self.day_length) % 1.0
        
        # Convertir en position angulaire (0 = midi, π = minuit)
        angle = self.day_night_cycle * 2 * np.pi
        
        # Calculer le facteur de température jour/nuit
        # Température plus élevée le jour, plus basse la nuit
        self.grid.global_temperature = self.base_temperature + 10 * np.sin(angle)
    
    def update_seasons(self):
        """Met à jour les saisons."""
        # Avancer dans le cycle des saisons
        day_progress = 1 / (self.season_length * self.day_length)
        self.season_cycle = (self.season_cycle + day_progress) % 1.0
        
        # Convertir en position angulaire
        angle = self.season_cycle * 2 * np.pi
        
        # Ajuster la température de base selon la saison
        seasonal_temp_variation = 10 * np.sin(angle)
        self.base_temperature = 20 + seasonal_temp_variation + self.global_warming
        
        # Ajuster l'humidité de base selon la saison
        seasonal_humidity_variation = 20 * np.sin(angle + np.pi / 2)  # Décalé d'un quart de cycle
        self.base_humidity = 50 + seasonal_humidity_variation
    
    def update_weather_systems(self):
        """Met à jour les systèmes météorologiques."""
        # Mise à jour des systèmes existants
        active_systems = []
        for system in self.weather_systems:
            system["duration"] -= 1
            if system["duration"] > 0:
                active_systems.append(system)
                self.apply_weather_system(system)
        
        # Remplacer la liste par les systèmes encore actifs
        self.weather_systems = active_systems
        
        # Possibilité de création d'un nouveau système météo
        if np.random.random() < 0.005:  # 0.5% de chance par frame
            self.generate_weather_system()
    
    def generate_weather_system(self):
        """Génère un nouveau système météorologique."""
        # Types de systèmes météo
        weather_types = [
            {"type": "rain", "temp_mod": -5, "humidity_mod": 40},
            {"type": "heat_wave", "temp_mod": 15, "humidity_mod": -20},
            {"type": "cold_front", "temp_mod": -15, "humidity_mod": 10},
            {"type": "fog", "temp_mod": -2, "humidity_mod": 30}
        ]
        
        # Sélectionner un type aléatoire
        weather_type = np.random.choice(weather_types)
        
        # Position de départ du système (bord de la carte)
        side = np.random.randint(4)  # 0: haut, 1: droite, 2: bas, 3: gauche
        if side == 0:
            start_x = np.random.randint(self.grid.width)
            start_y = 0
            direction = (0, 1)  # Du nord au sud
        elif side == 1:
            start_x = self.grid.width - 1
            start_y = np.random.randint(self.grid.height)
            direction = (-1, 0)  # D'est en ouest
        elif side == 2:
            start_x = np.random.randint(self.grid.width)
            start_y = self.grid.height - 1
            direction = (0, -1)  # Du sud au nord
        else:
            start_x = 0
            start_y = np.random.randint(self.grid.height)
            direction = (1, 0)  # D'ouest en est
        
        # Paramètres du système
        new_system = {
            "type": weather_type["type"],
            "position": (start_x, start_y),
            "direction": direction,
            "speed": np.random.uniform(0.05, 0.2),
            "radius": np.random.randint(5, 15),
            "intensity": np.random.uniform(0.3, 1.0),
            "duration": np.random.randint(100, 500),
            "temp_mod": weather_type["temp_mod"],
            "humidity_mod": weather_type["humidity_mod"]
        }
        
        # Ajouter à la liste des systèmes actifs
        self.weather_systems.append(new_system)
    
    def apply_weather_system(self, system):
        """Applique les effets d'un système météorologique à la grille."""
        # Mettre à jour la position du système
        x, y = system["position"]
        dx, dy = system["direction"]
        
        # Nouvelle position
        new_x = x + dx * system["speed"]
        new_y = y + dy * system["speed"]
        
        # Vérifier si le système est sorti de la grille
        if (new_x < -system["radius"] or new_x > self.grid.width + system["radius"] or
            new_y < -system["radius"] or new_y > self.grid.height + system["radius"]):
            system["duration"] = 0  # Marquer comme terminé
            return
        
        # Mettre à jour la position
        system["position"] = (new_x, new_y)
        
        # Appliquer les effets du système aux cellules dans son rayon
        center_x, center_y = int(new_x), int(new_y)
        radius = system["radius"]
        
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                cell_x, cell_y = center_x + dx, center_y + dy
                
                # Vérifier les limites de la grille
                if 0 <= cell_x < self.grid.width and 0 <= cell_y < self.grid.height:
                    # Calculer la distance au centre du système
                    distance = np.sqrt(dx**2 + dy**2)
                    
                    if distance <= radius:
                        # L'intensité diminue avec la distance
                        intensity_factor = (1 - distance / radius) * system["intensity"]
                        
                        # Appliquer les modifications à la cellule
                        cell = self.grid.get_cell(cell_x, cell_y)
                        
                        if cell:
                            # Modifier la température et l'humidité
                            temp_change = system["temp_mod"] * intensity_factor
                            humidity_change = system["humidity_mod"] * intensity_factor
                            
                            cell.temperature += temp_change * 0.1  # Changement progressif
                            cell.humidity += humidity_change * 0.1
                            
                            # Limiter aux valeurs raisonnables
                            cell.temperature = max(-30, min(50, cell.temperature))
                            cell.humidity = max(0, min(100, cell.humidity))
                            
                            # Effets spéciaux selon le type de système
                            if system["type"] == "rain" and intensity_factor > 0.7:
                                cell.water = min(cell.water + 0.1, 10)
                            elif system["type"] == "heat_wave" and intensity_factor > 0.8:
                                cell.water = max(0, cell.water - 0.05)
    
    def check_for_disasters(self):
        """Vérifie si une catastrophe naturelle se produit."""
        # Vérifier chaque type de catastrophe
        for disaster_type, probability in self.disaster_probs.items():
            # La probabilité est par jour, donc diviser par le nombre de frames par jour
            frame_probability = probability / self.day_length
            
            if np.random.random() < frame_probability:
                self.trigger_disaster(disaster_type)
    
    def trigger_disaster(self, disaster_type):
        """Déclenche une catastrophe naturelle spécifique."""
        # Enregistrer la catastrophe
        day = int(self.grid.day_night_cycle * self.day_length)
        self.disaster_history.append({
            "type": disaster_type,
            "day": day,
            "season": self.get_current_season()
        })
        
        # Déclencher l'effet approprié
        if disaster_type == "flood":
            self.grid.trigger_flood()
        elif disaster_type == "fire":
            self.grid.trigger_fire()
        elif disaster_type == "drought":
            self.grid.trigger_drought()
        elif disaster_type == "meteor":
            self.trigger_meteor_impact()
    
    def trigger_meteor_impact(self):
        """Déclenche l'impact d'une météorite."""
        # Choisir un point d'impact aléatoire
        impact_x = np.random.randint(self.grid.width)
        impact_y = np.random.randint(self.grid.height)
        
        # Rayon d'impact
        impact_radius = np.random.randint(3, 8)
        
        # Appliquer les dégâts dans la zone d'impact
        for x in range(max(0, impact_x - impact_radius), min(self.grid.width, impact_x + impact_radius + 1)):
            for y in range(max(0, impact_y - impact_radius), min(self.grid.height, impact_y + impact_radius + 1)):
                distance = np.sqrt((x - impact_x)**2 + (y - impact_y)**2)
                
                if distance <= impact_radius:
                    cell = self.grid.get_cell(x, y)
                    
                    if cell:
                        # Effets de l'impact basés sur la distance
                        effect_strength = 1 - (distance / impact_radius)
                        
                        # Centre de l'impact: transformation en terrain désertique
                        if distance < impact_radius * 0.3:
                            self.grid.set_cell_type(x, y, "desert")
                        
                        # Réduction drastique des ressources
                        cell.food = 0
                        cell.water = 0
                        
                        # Augmentation temporaire de la température
                        cell.temperature += 30 * effect_strength
                        
                        # Marquer avec un état spécial
                        cell.special_state = "impact"
                        cell.state_duration = int(100 * effect_strength)
    
    def apply_environmental_conditions(self):
        """Applique les conditions environnementales globales à toutes les cellules."""
        # Appliquer les effets du jour/nuit et des saisons
        day_night_factor = np.sin(self.day_night_cycle * 2 * np.pi)
        season_factor = np.sin(self.season_cycle * 2 * np.pi)
        
        # Calculer les modificateurs globaux
        temp_modifier = 5 * day_night_factor + 10 * season_factor + self.global_warming
        humidity_modifier = -10 * day_night_factor + 20 * season_factor
        
        # Les modifications sont appliquées graduellement à travers la méthode
        # diffuse_environment de la classe Grid
    
    def get_current_season(self):
        """Retourne la saison actuelle sous forme textuelle."""
        if 0 <= self.season_cycle < 0.25:
            return "spring"
        elif 0.25 <= self.season_cycle < 0.5:
            return "summer"
        elif 0.5 <= self.season_cycle < 0.75:
            return "autumn"
        else:
            return "winter"
    
    def get_daylight(self):
        """Retourne un facteur de luminosité (0 = nuit, 1 = jour)."""
        # Convertir le cycle jour/nuit en luminosité
        # Jour de 0.25 à 0.75 du cycle (0.5 = midi)
        if 0.25 <= self.day_night_cycle < 0.75:
            # Luminosité pendant la journée (maximum à midi)
            return 1 - abs(self.day_night_cycle - 0.5) * 2
        else:
            # Nuit (faible lumière)
            if self.day_night_cycle < 0.25:
                night_progress = self.day_night_cycle + 0.25
            else:
                night_progress = self.day_night_cycle - 0.75
            
            # Lumière résiduelle pendant la nuit
            return 0.1 + 0.1 * (1 - night_progress / 0.25)
    
    def apply_global_warming(self, rate):
        """Applique un effet de réchauffement climatique progressif."""
        self.global_warming += rate
        
        # Limiter à des valeurs raisonnables
        self.global_warming = min(15, self.global_warming)
        
        # Des effets supplémentaires pourraient être ajoutés ici
        # Comme l'augmentation de la fréquence des catastrophes
        if self.global_warming > 5:
            # Augmenter la probabilité d'incendies et de sécheresses
            self.disaster_probs["fire"] = 0.001 * (1 + self.global_warming / 10)
            self.disaster_probs["drought"] = 0.0005 * (1 + self.global_warming / 5)
    
    def get_environment_summary(self):
        """Retourne un résumé des conditions environnementales actuelles."""
        season = self.get_current_season()
        time_of_day = "day" if 0.25 <= self.day_night_cycle < 0.75 else "night"
        
        # Calculer les conditions moyennes
        avg_temp = 0
        avg_humidity = 0
        cell_count = 0
        
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell(x, y)
                if cell:
                    avg_temp += cell.temperature
                    avg_humidity += cell.humidity
                    cell_count += 1
        
        avg_temp /= cell_count if cell_count > 0 else 1
        avg_humidity /= cell_count if cell_count > 0 else 1
        
        # Compter les cellules par type de terrain
        terrain_counts = {terrain: 0 for terrain in Config.ENVIRONMENTS.keys()}
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell(x, y)
                if cell:
                    terrain_counts[cell.terrain_type] += 1
        
        # Calculer les pourcentages
        terrain_percentages = {
            terrain: count / cell_count * 100 if cell_count > 0 else 0
            for terrain, count in terrain_counts.items()
        }
        
        return {
            "season": season,
            "time_of_day": time_of_day,
            "avg_temperature": avg_temp,
            "avg_humidity": avg_humidity,
            "global_warming": self.global_warming,
            "terrain_percentages": terrain_percentages,
            "active_weather_systems": len(self.weather_systems),
            "disaster_history": len(self.disaster_history)
        }