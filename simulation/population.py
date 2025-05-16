import numpy as np
from creatures.evolution import Evolution
from config import Config
from simulation.statistics import Statistics
from creatures.creature import Creature

class Population:
    """
    Gère l'ensemble des créatures dans la simulation.
    S'occupe de la reproduction, de la sélection naturelle et de l'évolution.
    """
    def __init__(self, grid):
        self.grid = grid
        self.creatures = []
        self.dead_creatures = []  # Historique des créatures mortes
        self.generation = 1       # Compteur de génération
        
        # Importation du système d'évolution
        from creatures.evolution import Evolution
        
        # Initialisation du système d'évolution
        self.evolution = Evolution(grid)
        
        # Importation des statistiques
        from simulation.statistics import Statistics
        
        # Statistiques de population
        self.statistics = Statistics()
        
        # Initialisation de la population de départ
        self.initialize_population()

    def initialize_population(self):
        """Crée la population initiale de créatures."""
        # Cette méthode sera implémentée avec vos classes existantes
        from creatures.creature import Creature
        
        for _ in range(Config.INITIAL_POPULATION):
            # Position aléatoire
            x = np.random.randint(0, self.grid.width)
            y = np.random.randint(0, self.grid.height)
            
            # Vérifier si la position est viable pour une créature initiale
            cell = self.grid.get_cell(x, y)
            if cell and cell.terrain_type == "water":
                continue  # Éviter de placer des créatures dans l'eau initialement
            
            # Créer la créature et l'ajouter à la population
            creature = Creature(self.grid, x, y)
            self.creatures.append(creature)
        
        # Enregistrement des statistiques initiales
        self.statistics.update_population_stats(self.generation, self)
            
    def update(self):
        """Met à jour toutes les créatures et gère les interactions."""
        # Liste des créatures à supprimer
        to_remove = []
        
        # Tentatives de reproduction à traiter après les mises à jour
        reproduction_pairs = []
        
        # Mise à jour de chaque créature
        for creature in self.creatures:
            # Mettre à jour la créature et vérifier si elle survit
            if not creature.update():
                to_remove.append(creature)
                continue
            
            # Gestion des interactions entre créatures
            for other in self.creatures:
                if creature == other:
                    continue
                
                # Calculer la distance entre les créatures
                distance = np.sqrt((creature.x - other.x)**2 + (creature.y - other.y)**2)
                
                # Si les créatures sont proches
                if distance < 1.5:
                    # Possibilité de reproduction
                    if (creature.state == "mating" or other.state == "mating") and \
                       creature.is_ready_to_reproduce() and other.is_ready_to_reproduce():
                        reproduction_pairs.append((creature, other))
                    
                    # Possibilité de combat (basé sur l'agressivité)
                    elif creature.genome.traits["aggression"] > 70 and np.random.random() < 0.2:
                        self.handle_combat(creature, other)
        
        # Traiter les reproductions
        new_creatures = []
        for creature1, creature2 in reproduction_pairs:
            # Vérifier si les créatures sont toujours vivantes et prêtes
            if creature1 not in to_remove and creature2 not in to_remove:
                # Créer un nouvel enfant
                child = creature1.reproduce(creature2)
                new_creatures.append(child)
        
        # Ajouter les nouveaux-nés
        self.creatures.extend(new_creatures)
        
        # Supprimer les créatures mortes
        for creature in to_remove:
            self.creatures.remove(creature)
            self.dead_creatures.append(creature)
        
        # Contrôle de la population (limite maximale pour éviter les surcharges)
        self.control_population()
        
        # Mise à jour des statistiques
        if len(to_remove) > 0 or len(new_creatures) > 0:
            self.statistics.update_population_stats(self.generation, self)
    
    def handle_combat(self, attacker, defender):
        """Gère un combat entre deux créatures."""
        # Calculer la force d'attaque
        attack_power = attacker.genome.traits["strength"] * \
                      (1 + attacker.genome.traits["aggression"] / 100)
        
        # Calculer la défense
        defense = defender.genome.traits["strength"] * \
                 (1 - defender.genome.traits["aggression"] / 200)  # L'agressivité réduit la défense
        
        # Résultat du combat
        damage = max(0, attack_power - defense) / 10  # Réduire l'échelle des dégâts
        
        # Appliquer les dégâts
        defender.health -= damage
        
        # Consommation d'énergie pour l'attaquant
        attacker.energy -= attack_power / 20
        
        # Si le défenseur survit, il peut fuir
        if defender.health > 0 and np.random.random() < 0.7:
            defender.state = "fleeing"
            defender.target = (attacker.x, attacker.y)  # Fuir l'attaquant
    
    def end_day(self):
        """
        Traitement de fin de journée.
        Déclenche la reproduction forcée pour maintenir l'espèce.
        """
        self.generation += 1
        
        # Si la population est trop faible, encourager la reproduction
        if len(self.creatures) < Config.INITIAL_POPULATION / 2:
            self.trigger_breeding_season()
        
        # Appliquer les effets d'évolution
        num_reproductions = self.evolution.perform_evolution(self)
        
        # Enregistrer l'événement si significatif
        if num_reproductions > len(self.creatures) / 10:
            self.evolution.log_evolutionary_event(
                self.generation,
                "mass_reproduction",
                f"{num_reproductions} nouvelles créatures sont nées suite à une reproduction massive."
            )
        
        # Analyser l'adaptation de la population
        adaptation_info = self.evolution.analyze_adaptation(self)
        
        # Détection d'émergence d'espèces
        num_species, species_counts = self.evolution.detect_speciation(self)
        if num_species > 1:
            self.evolution.log_evolutionary_event(
                self.generation,
                "speciation",
                f"{num_species} espèces distinctes détectées dans la population."
            )
        
        # Enregistrement des statistiques quotidiennes
        self.statistics.update_population_stats(self.generation, self)
        
        # Mise à jour des métriques environnementales
        self.statistics.update_environment_metrics(self.generation, self.grid)
    
    def trigger_breeding_season(self):
        """Déclenche une saison de reproduction pour maintenir la population."""
        # Liste des créatures capables de se reproduire
        eligible_creatures = [c for c in self.creatures if c.is_ready_to_reproduce()]
        
        # Mélanger la liste pour des appariements aléatoires
        np.random.shuffle(eligible_creatures)
        
        # Former des couples
        new_creatures = []
        for i in range(0, len(eligible_creatures) - 1, 2):
            parent1 = eligible_creatures[i]
            parent2 = eligible_creatures[i + 1]
            
            # Créer plusieurs enfants par couple
            num_children = np.random.randint(1, 4)
            for _ in range(num_children):
                child = parent1.reproduce(parent2)
                new_creatures.append(child)
        
        # Ajouter les nouveaux-nés à la population
        self.creatures.extend(new_creatures)
        
        # Enregistrer l'événement
        if new_creatures:
            self.evolution.log_evolutionary_event(
                self.generation,
                "breeding_season",
                f"Saison de reproduction déclenchée: {len(new_creatures)} nouvelles créatures nées."
            )
    
    def control_population(self):
        """Limite la taille de la population pour éviter les surcharges."""
        max_population = Config.INITIAL_POPULATION * 3
        
        if len(self.creatures) > max_population:
            # Trier les créatures par âge et santé (éliminer les plus âgées/faibles)
            self.creatures.sort(key=lambda c: c.age / c.max_age - c.health / 100)
            
            # Conserver uniquement les plus fortes
            excess = len(self.creatures) - max_population
            removed = self.creatures[:excess]
            self.creatures = self.creatures[excess:]
            
            # Ajouter aux statistiques
            self.dead_creatures.extend(removed)
            
            # Enregistrer l'événement
            self.evolution.log_evolutionary_event(
                self.generation,
                "population_control",
                f"Contrôle de population: {excess} créatures éliminées par sélection naturelle."
            )
    
    def get_statistics(self):
        """Récupère les statistiques principales pour l'affichage."""
        return self.statistics.get_summary()
    
    def get_creatures_by_terrain(self):
        """Compte les créatures par type de terrain."""
        terrain_counts = {terrain: 0 for terrain in Config.ENVIRONMENTS.keys()}
        
        for creature in self.creatures:
            cell_x, cell_y = int(creature.x), int(creature.y)
            cell = self.grid.get_cell(cell_x, cell_y)
            
            if cell:
                terrain_counts[cell.terrain_type] += 1
        
        return terrain_counts
    
    def get_species_diversity(self):
        """Calcule un indice de diversité des espèces basé sur les traits génétiques."""
        if len(self.creatures) < 5:
            return 0
        
        # Extraire les valeurs de traits clés
        trait_values = {}
        for creature in self.creatures:
            for trait, value in creature.genome.traits.items():
                if trait not in trait_values:
                    trait_values[trait] = []
                trait_values[trait].append(value)
        
        # Calculer l'écart-type de chaque trait
        diversity_scores = {}
        for trait, values in trait_values.items():
            if isinstance(values[0], bool):
                # Pour les traits booléens, calculer la proportion
                true_ratio = sum(1 for v in values if v) / len(values)
                # Diversité maximale quand le ratio est proche de 0.5
                diversity_scores[trait] = 1 - abs(0.5 - true_ratio) * 2
            else:
                # Pour les traits numériques, calculer l'écart-type normalisé
                std_dev = np.std(values)
                max_possible_std = 100 / np.sqrt(12)  # Écart-type max pour une distribution uniforme [0, 100]
                diversity_scores[trait] = min(1.0, std_dev / max_possible_std)
        
        # Moyenner les scores de diversité (en ignorant les couleurs)
        relevant_traits = [t for t in diversity_scores.keys() if not t.startswith("color_")]
        avg_diversity = sum(diversity_scores[t] for t in relevant_traits) / len(relevant_traits)
        
        return avg_diversity