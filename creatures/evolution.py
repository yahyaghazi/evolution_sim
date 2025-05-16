import pygame
import numpy as np
from config import Config
from simulation.statistics import Statistics

class Evolution:
    """
    Gère les mécanismes d'évolution dans la simulation.
    Implémente les algorithmes de sélection naturelle, mutation et adaptation.
    """
    def __init__(self, grid):
        self.grid = grid
        self.statistics = Statistics()
        
        # Paramètres d'évolution
        self.mutation_rate = Config.MUTATION_RATE
        self.crossover_rate = Config.CROSSOVER_RATE
        self.selection_pressure = Config.SELECTION_PRESSURE
        
        # Tracker d'adaptation environnementale
        self.adaptation_map = np.zeros((grid.width, grid.height), dtype=float)
        self.update_adaptation_map()
    
    def select_parents(self, population):
        """
        Sélectionne des parents pour la reproduction en utilisant
        une sélection par tournoi avec pression de sélection.
        """
        if len(population.creatures) < 2:
            return None, None
        
        # Taille du tournoi (nombre de créatures à comparer)
        tournament_size = max(2, int(len(population.creatures) * 0.1))
        
        # Sélection du premier parent - utiliser toList() pour convertir en liste Python
        candidates1 = np.random.choice(
            population.creatures, 
            size=min(tournament_size, len(population.creatures)), 
            replace=False
        ).tolist()
        
        parent1 = self._select_fittest(candidates1)
        
        # Sélection du second parent (différent du premier)
        remaining = [c for c in population.creatures if c != parent1]
        if not remaining:
            return parent1, np.random.choice(population.creatures)
        
        candidates2 = np.random.choice(
            remaining,
            size=min(tournament_size, len(remaining)),
            replace=False
        ).tolist()
        
        parent2 = self._select_fittest(candidates2)
        
        return parent1, parent2
    
    def _select_fittest(self, candidates):
        """
        Sélectionne la créature la plus adaptée parmi les candidats,
        en tenant compte de la pression de sélection.
        """
        # Vérifier si la liste des candidats est vide en utilisant len()
        if len(candidates) == 0:
            return None
        
        # Calculer le fitness de chaque candidat
        fitness_scores = []
        for creature in candidates:
            # Combiner plusieurs facteurs pour le fitness
            fitness = self._calculate_fitness(creature)
            fitness_scores.append(fitness)
        
        # Appliquer la pression de sélection
        selection_probs = np.array(fitness_scores) ** self.selection_pressure
        sum_probs = np.sum(selection_probs)
        
        # Éviter la division par zéro
        if sum_probs <= 0:
            # Si toutes les probabilités sont nulles, sélectionner aléatoirement
            return np.random.choice(candidates)
        
        # Normaliser les probabilités
        selection_probs = selection_probs / sum_probs
        
        try:
            # Sélection probabiliste basée sur le fitness
            selected_index = np.random.choice(len(candidates), p=selection_probs)
            return candidates[selected_index]
        except ValueError:
            # Fallback en cas d'erreur (probas invalides, etc.)
            return np.random.choice(candidates)
    
    def _calculate_fitness(self, creature):
        """
        Calcule la valeur d'adaptation (fitness) d'une créature.
        Combine plusieurs facteurs: énergie, santé, âge et adaptation environnementale.
        """
        # Facteurs de base
        energy_factor = creature.energy / 100
        health_factor = creature.health / 100
        
        # Facteur d'âge (préférence pour les créatures matures mais pas trop vieilles)
        age_ratio = creature.age / creature.max_age
        age_factor = 1.0
        if age_ratio < 0.2:
            # Jeunes créatures: fitness réduit
            age_factor = 0.5 + age_ratio * 2.5
        elif age_ratio > 0.7:
            # Vieilles créatures: fitness diminue progressivement
            age_factor = 1.0 - (age_ratio - 0.7) * 2
        
        # Facteur d'adaptation environnementale
        cell_x, cell_y = int(creature.x), int(creature.y)
        if 0 <= cell_x < self.grid.width and 0 <= cell_y < self.grid.height:
            cell = self.grid.get_cell(cell_x, cell_y)
            env_factor = creature.genome.calculate_environmental_fitness(cell)
        else:
            env_factor = 0.5  # Valeur par défaut
        
        # Combinaison des facteurs (avec différentes pondérations)
        fitness = (
            energy_factor * 0.3 +
            health_factor * 0.2 +
            age_factor * 0.2 +
            env_factor * 0.3
        )
        
        return max(0.01, fitness)  # Garantir un fitness minimum positif
    
    def perform_evolution(self, population):
        """
        Effectue une étape d'évolution sur toute la population.
        Applique la sélection naturelle, la reproduction et la mutation.
        """
        # Mettre à jour la carte d'adaptation
        self.update_adaptation_map()
        
        # Nombre de couples à former pour la reproduction
        num_pairs = len(population.creatures) // 3
        
        # Nouvelle génération de créatures
        new_creatures = []
        
        for _ in range(num_pairs):
            # Sélectionner les parents
            parent1, parent2 = self.select_parents(population)
            
            if parent1 and parent2 and parent1 != parent2:
                # Vérifier si les parents sont prêts à se reproduire
                if parent1.is_ready_to_reproduce() and parent2.is_ready_to_reproduce():
                    # Créer un enfant par croisement des génomes
                    child = parent1.reproduce(parent2)
                    new_creatures.append(child)
        
        # Ajouter les nouveaux-nés à la population
        population.creatures.extend(new_creatures)
        
        # Mettre à jour les statistiques
        self.statistics.update_population_stats(population.generation, population)
        
        return len(new_creatures)
    
    def update_adaptation_map(self):
        """
        Met à jour la carte d'adaptation environnementale.
        Cette carte représente à quel point chaque cellule est adaptée à la vie.
        """
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                cell = self.grid.get_cell(x, y)
                if cell:
                    self.adaptation_map[x, y] = cell.get_habitability()
    
    def detect_speciation(self, population):
        """
        Détecte si la population a commencé à se diviser en espèces distinctes.
        Utilise le clustering pour identifier les groupes génétiques.
        """
        # Seuil minimal de créatures pour la détection d'espèces
        if len(population.creatures) < 10:
            return 1, {}  # Une seule espèce
        
        # Extraire les traits génétiques clés pour chaque créature
        genetic_data = []
        for creature in population.creatures:
            genome = creature.genome.traits
            
            # Utiliser un sous-ensemble de traits pour la classification
            traits = [
                genome["size"],
                genome["speed"],
                genome["strength"],
                genome["heat_tolerance"],
                genome["cold_tolerance"],
                genome["water_affinity"],
                genome["mountain_affinity"],
                1 if genome["can_swim"] else 0,
                1 if genome["can_climb"] else 0
            ]
            genetic_data.append(traits)
        
        # Convertir en tableau numpy
        data = np.array(genetic_data)
        
        # Nombre d'espèces potentielles (k-means clustering simplifié)
        k = min(5, max(1, len(data) // 20))
        
        # Centres initiaux avec k créatures aléatoires
        indices = np.random.choice(len(data), k, replace=False)
        centers = data[indices]
        
        # Assigner chaque créature à une espèce
        species = {}
        for _ in range(5):  # Nombre d'itérations pour affiner les clusters
            # Réinitialiser les clusters
            clusters = [[] for _ in range(k)]
            
            # Assigner chaque créature au centre le plus proche
            for i, traits in enumerate(data):
                distances = [np.sum((traits - center) ** 2) for center in centers]
                closest = np.argmin(distances)
                clusters[closest].append(i)
            
            # Mettre à jour les centres
            for i, cluster in enumerate(clusters):
                if cluster:  # Éviter la division par zéro
                    centers[i] = np.mean(data[cluster], axis=0)
        
        # Compter les créatures par espèce
        species_counts = {i: len(clusters[i]) for i in range(k)}
        
        # Nombre d'espèces réelles (certains clusters peuvent être vides)
        num_species = sum(1 for count in species_counts.values() if count > 0)
        
        return num_species, species_counts
    
    def analyze_adaptation(self, population):
        """
        Analyse l'adaptation de la population à son environnement.
        Retourne des informations sur les tendances d'adaptation.
        """
        if not population.creatures:
            return {
                "avg_adaptation": 0,
                "best_adaptation": 0,
                "worst_adaptation": 0,
                "habitat_preferences": {}
            }
        
        # Initialiser les compteurs
        adaptation_scores = []
        habitat_counts = {
            "water": 0,
            "desert": 0,
            "forest": 0,
            "mountain": 0
        }
        
        # Analyser chaque créature
        for creature in population.creatures:
            cell_x, cell_y = int(creature.x), int(creature.y)
            if 0 <= cell_x < self.grid.width and 0 <= cell_y < self.grid.height:
                cell = self.grid.get_cell(cell_x, cell_y)
                
                # Évaluer l'adaptation de la créature à cette cellule
                adaptation = creature.genome.calculate_environmental_fitness(cell)
                adaptation_scores.append(adaptation)
                
                # Comptage des habitats
                if cell.terrain_type in habitat_counts:
                    habitat_counts[cell.terrain_type] += 1
        
        # Calculer les statistiques d'adaptation
        if adaptation_scores:
            avg_adaptation = sum(adaptation_scores) / len(adaptation_scores)
            best_adaptation = max(adaptation_scores)
            worst_adaptation = min(adaptation_scores)
        else:
            avg_adaptation = best_adaptation = worst_adaptation = 0
        
        # Normaliser les préférences d'habitat
        total_creatures = len(population.creatures)
        habitat_preferences = {
            terrain: count / total_creatures if total_creatures > 0 else 0
            for terrain, count in habitat_counts.items()
        }
        
        return {
            "avg_adaptation": avg_adaptation,
            "best_adaptation": best_adaptation,
            "worst_adaptation": worst_adaptation,
            "habitat_preferences": habitat_preferences
        }
    
    def get_statistics(self):
        """Récupère les statistiques d'évolution actuelles."""
        return self.statistics
    
    def log_evolutionary_event(self, day, event_type, description):
        """Enregistre un événement évolutif important."""
        self.statistics.log_event(day, event_type, description)