import numpy as np
from config import Config

class Genome:
    """
    Représente le génome d'une créature, définissant ses traits et capacités.
    Gère les mécanismes de mutation et de croisement génétique.
    """
    def __init__(self, parent_genome=None):
        # Si un génome parent est fourni, effectuer une mutation
        if parent_genome:
            self.traits = parent_genome.traits.copy()
            self.mutate()
        else:
            # Sinon, créer un génome aléatoire
            self.initialize_random()
    
    def initialize_random(self):
        """Initialise un génome avec des valeurs aléatoires."""
        self.traits = {
            # Traits physiques (0-100)
            "size": np.random.randint(10, 90),          # Taille corporelle
            "speed": np.random.randint(10, 90),         # Vitesse de déplacement
            "strength": np.random.randint(10, 90),      # Force physique
            "vision_range": np.random.randint(10, 90),  # Portée de vision
            
            # Traits de survie et comportementaux (0-100)
            "metabolism": np.random.randint(10, 90),    # Vitesse de consommation d'énergie
            "aggression": np.random.randint(10, 90),    # Tendance à l'agression
            "reproduction_rate": np.random.randint(10, 90),  # Fréquence de reproduction
            "social_tendency": np.random.randint(10, 90),    # Tendance à la socialisation
            
            # Adaptations environnementales (0-100)
            "heat_tolerance": np.random.randint(10, 90),     # Tolérance à la chaleur
            "cold_tolerance": np.random.randint(10, 90),     # Tolérance au froid
            "water_affinity": np.random.randint(10, 90),     # Affinité pour l'eau
            "mountain_affinity": np.random.randint(10, 90),  # Affinité pour les montagnes
            
            # Traits spéciaux (booléens)
            "can_swim": np.random.random() > 0.5,       # Capacité à nager
            "can_climb": np.random.random() > 0.5,      # Capacité à grimper
            
            # Couleur (RGB)
            "color_r": np.random.randint(0, 255),
            "color_g": np.random.randint(0, 255),
            "color_b": np.random.randint(0, 255),
        }
    
    def mutate(self):
        """Applique des mutations aléatoires au génome."""
        for trait in self.traits:
            # Chance de mutation pour chaque trait
            if np.random.random() < Config.MUTATION_RATE:
                if isinstance(self.traits[trait], bool):
                    # Inversion pour les traits booléens
                    self.traits[trait] = not self.traits[trait]
                elif trait.startswith("color_"):
                    # Mutation de couleur
                    delta = np.random.randint(-30, 31)
                    self.traits[trait] = max(0, min(255, self.traits[trait] + delta))
                else:
                    # Mutation de valeur numérique
                    mutation_strength = np.random.randint(5, 20)
                    direction = 1 if np.random.random() > 0.5 else -1
                    self.traits[trait] += direction * mutation_strength
                    
                    # S'assurer que les valeurs restent dans des bornes raisonnables
                    self.traits[trait] = max(1, min(100, self.traits[trait]))
    
    @staticmethod
    def crossover(genome1, genome2):
        """
        Crée un nouveau génome par croisement de deux génomes parents.
        Utilise un croisement uniforme où chaque trait est pris de l'un des parents.
        """
        child_genome = Genome()
        
        for trait in genome1.traits:
            # Pour chaque trait, choisir aléatoirement l'un des parents
            if np.random.random() < 0.5:
                child_genome.traits[trait] = genome1.traits[trait]
            else:
                child_genome.traits[trait] = genome2.traits[trait]
        
        # Appliquer une mutation potentielle après le croisement
        if np.random.random() < Config.MUTATION_RATE:
            child_genome.mutate()
            
        return child_genome
    
    def get_color(self):
        """Récupère la couleur RGB définie par le génome."""
        return (self.traits["color_r"], self.traits["color_g"], self.traits["color_b"])
    
    def get_size(self):
        """Récupère la taille visuelle basée sur le trait de taille."""
        # Conversion du trait de taille (1-100) en pixels (min-max)
        return Config.CREATURE_MIN_SIZE + (self.traits["size"] / 100) * (Config.CREATURE_MAX_SIZE - Config.CREATURE_MIN_SIZE)
    
    def get_speed(self):
        """Récupère la vitesse de déplacement en cellules par frame."""
        # Conversion du trait de vitesse (1-100) en vitesse réelle
        return 0.05 + (self.traits["speed"] / 100) * 0.2
    
    def get_vision_range(self):
        """Récupère la portée de vision en nombre de cellules."""
        # Conversion du trait de vision (1-100) en cellules
        return 1 + int((self.traits["vision_range"] / 100) * 7)
    
    def get_metabolic_rate(self):
        """Récupère le taux métabolique (consommation d'énergie)."""
        # Un métabolisme élevé consomme plus d'énergie
        return 0.5 + (self.traits["metabolism"] / 100) * 1.5
    
    def calculate_environmental_fitness(self, cell):
        """
        Calcule l'adaptation de la créature à un environnement spécifique.
        Retourne une valeur de 0 (très mal adapté) à 1 (parfaitement adapté).
        """
        fitness = 0.5  # Valeur de base
        
        # Adaptation au type de terrain
        if cell.terrain_type == "water":
            fitness += 0.3 if self.traits["can_swim"] else -0.3
            fitness += (self.traits["water_affinity"] - 50) / 100
        elif cell.terrain_type == "mountain":
            fitness += 0.3 if self.traits["can_climb"] else -0.2
            fitness += (self.traits["mountain_affinity"] - 50) / 100
        
        # Adaptation à la température
        if cell.temperature > 30:  # Environnement chaud
            fitness += (self.traits["heat_tolerance"] - 50) / 100
        elif cell.temperature < 10:  # Environnement froid
            fitness += (self.traits["cold_tolerance"] - 50) / 100
        
        # Normaliser le résultat entre 0 et 1
        fitness = max(0.1, min(1.0, fitness))
        
        return fitness