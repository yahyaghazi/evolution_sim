import numpy as np
from config import Config

class Statistics:
    """
    Collecte et analyse les statistiques d'évolution de la simulation.
    Permet de suivre les tendances d'adaptation des créatures au fil du temps.
    """
    def __init__(self):
        # Historique de population
        self.population_history = []
        
        # Historique des traits génétiques moyens par génération
        self.trait_history = {}
        
        # Espèces détectées et leur évolution
        self.species = {}
        self.species_counts = []
        
        # Journalisation des événements importants
        self.events = []
        
        # Métriques environnementales
        self.environment_metrics = []
    
    def update_population_stats(self, generation, population):
        """Met à jour les statistiques de population pour une génération."""
        # Enregistrer la taille de la population
        self.population_history.append({
            "generation": generation,
            "count": len(population.creatures)
        })
        
        # Si pas de créatures, ne pas calculer les autres statistiques
        if not population.creatures:
            return
        
        # Calculer les moyennes des traits
        trait_sums = {}
        trait_mins = {}
        trait_maxs = {}
        
        for creature in population.creatures:
            for trait, value in creature.genome.traits.items():
                if trait not in trait_sums:
                    trait_sums[trait] = 0
                    trait_mins[trait] = value
                    trait_maxs[trait] = value
                else:
                    trait_sums[trait] += value
                    trait_mins[trait] = min(trait_mins[trait], value)
                    trait_maxs[trait] = max(trait_maxs[trait], value)
        
        # Enregistrer les statistiques de traits
        self.trait_history[generation] = {
            "averages": {
                trait: value / len(population.creatures)
                for trait, value in trait_sums.items()
            },
            "mins": trait_mins,
            "maxs": trait_maxs
        }
        
        # Grouper les créatures en espèces basées sur leurs traits
        self.identify_species(generation, population)
    
    def identify_species(self, generation, population):
        """
        Identifie les espèces émergentes en fonction des traits génétiques.
        Utilise un algorithme de clustering simple.
        """
        # Liste des créatures avec leurs traits clés pour la classification
        creatures_data = []
        for creature in population.creatures:
            genome = creature.genome.traits
            
            # Sélectionner les traits pour la classification (traits physiques principalement)
            species_traits = [
                genome["size"],
                genome["speed"],
                genome["vision_range"],
                genome["heat_tolerance"],
                genome["cold_tolerance"],
                genome["can_swim"],
                genome["can_climb"]
            ]
            creatures_data.append(species_traits)
        
        # Si trop peu de créatures, ne pas faire de clustering
        if len(creatures_data) < 5:
            return
        
        # Convertir en tableau numpy pour les calculs
        data = np.array(creatures_data)
        
        # Algorithme de clustering simple (k-means simplifié)
        # Note: Pour un système plus complexe, utiliser scikit-learn
        # Ici, nous utilisons simplement une approche basée sur la distance
        
        # Nombre de clusters (espèces potentielles)
        k = min(5, len(data) // 10 + 1)  # Adapter selon la taille de la population
        
        # Initialiser les centres avec k créatures aléatoires
        centers_idx = np.random.choice(len(data), k, replace=False)
        centers = data[centers_idx]
        
        # Assigner chaque créature à un cluster
        clusters = {}
        for i, creature_data in enumerate(data):
            # Trouver le centre le plus proche
            min_dist = float('inf')
            best_cluster = -1
            
            for cluster_id, center in enumerate(centers):
                # Distance euclidienne simple
                dist = np.sum((creature_data - center) ** 2)
                if dist < min_dist:
                    min_dist = dist
                    best_cluster = cluster_id
            
            # Assigner au cluster
            if best_cluster not in clusters:
                clusters[best_cluster] = []
            clusters[best_cluster].append(i)
        
        # Compter les créatures par espèce
        species_counts = {i: len(members) for i, members in clusters.items()}
        
        # Enregistrer le résultat
        self.species_counts.append({
            "generation": generation,
            "species_counts": species_counts
        })
        
        # Définir les caractéristiques de chaque espèce
        self.species[generation] = {}
        for species_id, members in clusters.items():
            if len(members) > 0:
                # Calculer les moyennes des traits pour cette espèce
                species_data = data[members]
                species_center = np.mean(species_data, axis=0)
                
                # Enregistrer les caractéristiques de l'espèce
                self.species[generation][species_id] = {
                    "count": len(members),
                    "traits": {
                        "size": species_center[0],
                        "speed": species_center[1],
                        "vision_range": species_center[2],
                        "heat_tolerance": species_center[3],
                        "cold_tolerance": species_center[4],
                        "can_swim": species_center[5] > 0.5,  # Convertir en booléen
                        "can_climb": species_center[6] > 0.5  # Convertir en booléen
                    }
                }
    
    def log_event(self, day, event_type, description):
        """Enregistre un événement important dans la simulation."""
        self.events.append({
            "day": day,
            "type": event_type,
            "description": description
        })
    
    def update_environment_metrics(self, day, grid):
        """Enregistre des métriques sur l'environnement."""
        # Compter les types de terrain
        terrain_counts = {
            "water": 0,
            "desert": 0,
            "forest": 0,
            "mountain": 0
        }
        
        # Moyennes de température et d'humidité
        avg_temp = 0
        avg_humidity = 0
        
        # Quantité totale de nourriture
        total_food = 0
        
        # Parcourir la grille
        cell_count = grid.width * grid.height
        for x in range(grid.width):
            for y in range(grid.height):
                cell = grid.cells[x, y]
                
                # Compter les types de terrain
                terrain_counts[cell.terrain_type] += 1
                
                # Ajouter à la moyenne
                avg_temp += cell.temperature
                avg_humidity += cell.humidity
                
                # Compter la nourriture
                total_food += cell.food
        
        # Calculer les moyennes
        avg_temp /= cell_count
        avg_humidity /= cell_count
        
        # Enregistrer les métriques
        self.environment_metrics.append({
            "day": day,
            "terrain_counts": terrain_counts,
            "avg_temperature": avg_temp,
            "avg_humidity": avg_humidity,
            "total_food": total_food
        })
    
    def get_population_trend(self, last_n_generations=10):
        """Récupère la tendance de population sur les n dernières générations."""
        if len(self.population_history) < 2:
            return 0  # Pas assez de données
        
        # Limiter aux n dernières générations
        history = self.population_history[-last_n_generations:]
        
        # Calculer la pente de la tendance
        if len(history) < 2:
            return 0
        
        # Simple calcul de pente entre le début et la fin
        start_count = history[0]["count"]
        end_count = history[-1]["count"]
        
        return (end_count - start_count) / len(history)
    
    def get_dominant_species(self, generation=None):
        """Récupère l'espèce dominante à une génération donnée."""
        if generation is None:
            # Utiliser la dernière génération disponible
            if not self.species:
                return None
            generation = max(self.species.keys())
        
        if generation not in self.species:
            return None
        
        # Trouver l'espèce avec le plus de membres
        species_data = self.species[generation]
        if not species_data:
            return None
        
        dominant_id = max(species_data, key=lambda s: species_data[s]["count"])
        return species_data[dominant_id]
    
    def get_trait_evolution(self, trait, start_gen=0, end_gen=None):
        """Récupère l'évolution d'un trait au fil des générations."""
        if not self.trait_history:
            return []
        
        if end_gen is None:
            end_gen = max(self.trait_history.keys())
        
        evolution = []
        for gen in range(start_gen, end_gen + 1):
            if gen in self.trait_history and trait in self.trait_history[gen]["averages"]:
                evolution.append({
                    "generation": gen,
                    "average": self.trait_history[gen]["averages"][trait],
                    "min": self.trait_history[gen]["mins"][trait],
                    "max": self.trait_history[gen]["maxs"][trait]
                })
        
        return evolution
    
    def get_summary(self):
        """Génère un résumé des statistiques actuelles de la simulation."""
        if not self.population_history:
            return "Pas encore de données statistiques disponibles."
        
        # Dernière génération
        last_gen = self.population_history[-1]["generation"]
        current_pop = self.population_history[-1]["count"]
        
        # Tendance de population
        trend = self.get_population_trend()
        trend_desc = "stable"
        if trend > 1:
            trend_desc = "en forte croissance"
        elif trend > 0.2:
            trend_desc = "en croissance"
        elif trend < -1:
            trend_desc = "en fort déclin"
        elif trend < -0.2:
            trend_desc = "en déclin"
        
        # Espèce dominante
        dominant = self.get_dominant_species()
        
        summary = f"Génération {last_gen}: Population de {current_pop} créatures ({trend_desc}).\n"
        
        if dominant:
            summary += "Espèce dominante: "
            summary += f"Taille: {dominant['traits']['size']:.1f}, "
            summary += f"Vitesse: {dominant['traits']['speed']:.1f}, "
            summary += f"Vision: {dominant['traits']['vision_range']:.1f}\n"
            summary += f"Adaptations: "
            
            adaptations = []
            if dominant['traits']['heat_tolerance'] > 70:
                adaptations.append("chaleur")
            if dominant['traits']['cold_tolerance'] > 70:
                adaptations.append("froid")
            if dominant['traits']['can_swim']:
                adaptations.append("nage")
            if dominant['traits']['can_climb']:
                adaptations.append("escalade")
            
            if adaptations:
                summary += ", ".join(adaptations)
            else:
                summary += "aucune adaptation spéciale"
        
        return summary