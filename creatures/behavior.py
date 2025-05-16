import pygame
import numpy as np
from config import Config
from creatures.creature import Creature

class Behavior:
    """
    Définit et gère les comportements possibles des créatures.
    Implémente les algorithmes de prise de décision et d'intelligence artificielle.
    """
    # Types de comportements
    EXPLORING = "exploring"
    HUNTING = "hunting"
    FLEEING = "fleeing"
    MATING = "mating"
    RESTING = "resting"
    MIGRATING = "migrating"
    
    def __init__(self):
        # Paramètres de comportement
        self.decision_interval = 10  # Intervalles entre les décisions (en frames)
        self.group_distance = 3      # Distance pour considérer des créatures comme un groupe
        
        # Initialisation des tables de décision
        self.init_decision_tables()
    
    def init_decision_tables(self):
        """Initialise les tables de décision pour différents comportements."""
        # Table de prise de décision pour l'exploration
        self.exploration_weights = {
            "random": 0.5,            # Tendance à se déplacer aléatoirement
            "curiosity": 0.3,         # Tendance à explorer de nouveaux territoires
            "resource_attraction": 0.2 # Attraction vers les ressources visibles
        }
        
        # Table de prise de décision pour la chasse
        self.hunting_weights = {
            "hunger": 0.5,            # Importance de la faim
            "distance": 0.3,          # Importance de la distance à la nourriture
            "risk": 0.2               # Considération du risque
        }
        
        # Table de prise de décision pour la fuite
        self.fleeing_weights = {
            "danger": 0.6,            # Importance du niveau de danger
            "escape_route": 0.4       # Importance de la route d'échappement
        }
        
        # Table de prise de décision pour la reproduction
        self.mating_weights = {
            "readiness": 0.4,         # Préparation à la reproduction
            "partner_quality": 0.3,   # Qualité du partenaire potentiel
            "competition": 0.3        # Niveau de compétition
        }
    
    def decide_behavior(self, creature, nearby_creatures):
        """
        Décide du comportement d'une créature en fonction de son état
        et de son environnement.
        """
        # Priorité aux besoins vitaux
        if creature.energy < 30:
            return self.HUNTING, None
        
        # Reproduction possible?
        if creature.is_ready_to_reproduce() and np.random.random() < 0.1:
            # Chercher un partenaire potentiel
            partner = self.find_mating_partner(creature, nearby_creatures)
            if partner:
                return self.MATING, partner
        
        # Repos si besoin de récupérer
        if creature.energy < 50 and np.random.random() < 0.3:
            return self.RESTING, None
        
        # Possibilité de migration si l'environnement n'est pas favorable
        if self.should_migrate(creature):
            return self.MIGRATING, None
        
        # Par défaut, exploration
        return self.EXPLORING, None
    
    def find_mating_partner(self, creature, nearby_creatures):
        """
        Recherche un partenaire compatible pour la reproduction
        parmi les créatures proches.
        """
        potential_partners = []
        
        for other in nearby_creatures:
            if other == creature:
                continue
                
            # Vérifier si l'autre créature est prête à se reproduire
            if not other.is_ready_to_reproduce():
                continue
                
            # Calculer la distance
            distance = np.sqrt((creature.x - other.x)**2 + (creature.y - other.y)**2)
            
            # Ne considérer que les créatures dans le rayon de vision
            if distance > creature.genome.get_vision_range():
                continue
                
            # Évaluer la compatibilité génétique (pour éviter la consanguinité)
            compatibility = self.assess_genetic_compatibility(creature.genome, other.genome)
            
            potential_partners.append((other, compatibility, distance))
        
        # Si des partenaires potentiels ont été trouvés
        if potential_partners:
            # Trier par compatibilité et distance
            potential_partners.sort(key=lambda x: (x[1], -x[2]), reverse=True)
            
            # Retourner le meilleur candidat
            return potential_partners[0][0]
            
        return None
    
    def assess_genetic_compatibility(self, genome1, genome2):
        """
        Évalue la compatibilité génétique entre deux génomes.
        Une valeur plus haute indique une meilleure compatibilité.
        """
        # Calcul simple de la différence génétique
        diff_sum = 0
        trait_count = 0
        
        for trait in genome1.traits:
            if trait in genome2.traits and not trait.startswith("color_"):
                # Ne pas considérer les couleurs pour la compatibilité
                if isinstance(genome1.traits[trait], bool):
                    # Pour les traits booléens, différence binaire
                    diff_sum += 0 if genome1.traits[trait] == genome2.traits[trait] else 1
                else:
                    # Pour les traits numériques, différence relative
                    trait_diff = abs(genome1.traits[trait] - genome2.traits[trait])
                    normalized_diff = trait_diff / 100 if trait_diff <= 100 else 1
                    diff_sum += normalized_diff
                
                trait_count += 1
        
        if trait_count == 0:
            return 0.5  # Valeur par défaut
        
        # Différence moyenne normalisée (0 = identiques, 1 = complètement différents)
        avg_diff = diff_sum / trait_count
        
        # Convertir en compatibilité (0 = incompatibles, 1 = parfaitement compatibles)
        # Une différence modérée est préférable (ni trop similaire ni trop différent)
        compatibility = 1.0 - abs(avg_diff - 0.3) * 2
        
        return max(0, min(1, compatibility))
    
    def should_migrate(self, creature):
        """
        Détermine si une créature devrait migrer en fonction
        des conditions environnementales.
        """
        # Récupérer la cellule actuelle
        cell_x, cell_y = int(creature.x), int(creature.y)
        cell = creature.grid.get_cell(cell_x, cell_y)
        
        if not cell:
            return False
            
        # Calculer l'adaptation environnementale
        env_fitness = creature.genome.calculate_environmental_fitness(cell)
        
        # Probabilité de migration inversement proportionnelle à l'adaptation
        migration_probability = 0.05 * (1 - env_fitness)
        
        return np.random.random() < migration_probability
    
    def choose_target_for_hunting(self, creature):
        """
        Choisit une cible pour la chasse (nourriture) en évaluant
        les options disponibles dans le champ de vision.
        """
        # Cette fonctionnalité est déjà implémentée dans la méthode find_food
        # de la classe Creature, donc on délègue à cette méthode.
        creature.find_food()
        return creature.target
    
    def choose_escape_direction(self, creature, danger):
        """
        Détermine la meilleure direction pour fuir un danger.
        """
        if not danger:
            # Si pas de danger spécifié, direction aléatoire
            creature.set_random_direction()
            return
            
        # Direction opposée au danger
        danger_x, danger_y = danger
        dx = creature.x - danger_x
        dy = creature.y - danger_y
        
        # Normaliser la direction
        distance = np.sqrt(dx**2 + dy**2)
        if distance > 0:
            creature.direction = (dx / distance, dy / distance)
        else:
            # Si on est exactement sur le danger, direction aléatoire
            creature.set_random_direction()
    
    def choose_rest_location(self, creature):
        """
        Choisit un endroit approprié pour se reposer.
        """
        # Vérifier si la cellule actuelle est appropriée pour le repos
        cell_x, cell_y = int(creature.x), int(creature.y)
        cell = creature.grid.get_cell(cell_x, cell_y)
        
        if cell and cell.get_habitability() > 0.6:
            # Cellule actuelle convenable, rester sur place
            creature.direction = (0, 0)
            return True
            
        # Chercher une meilleure cellule dans les environs
        vision_range = creature.genome.get_vision_range()
        best_cell = None
        best_value = 0
        
        for dx in range(-vision_range, vision_range + 1):
            for dy in range(-vision_range, vision_range + 1):
                nx, ny = cell_x + dx, cell_y + dy
                
                # Vérifier les limites
                if 0 <= nx < creature.grid.width and 0 <= ny < creature.grid.height:
                    check_cell = creature.grid.get_cell(nx, ny)
                    
                    # Évaluer la cellule pour le repos
                    habitability = check_cell.get_habitability()
                    distance = np.sqrt(dx**2 + dy**2)
                    
                    # Valeur combinée (habitabilité diminuée par la distance)
                    cell_value = habitability / (1 + distance * 0.2)
                    
                    if cell_value > best_value:
                        best_value = cell_value
                        best_cell = (nx, ny)
        
        if best_cell:
            # Se diriger vers la meilleure cellule
            creature.target = best_cell
            return False
            
        # Aucune bonne cellule trouvée, rester sur place
        creature.direction = (0, 0)
        return True
    
    def update_group_behavior(self, creatures):
        """
        Met à jour le comportement de groupe des créatures.
        Implémente des comportements simples de groupe comme le rassemblement.
        """
        # Identifier les groupes de créatures proches
        groups = self.identify_groups(creatures)
        
        # Pour chaque groupe
        for group in groups:
            if len(group) < 3:
                continue  # Ignorer les petits groupes
                
            # Identifier l'espèce dominante dans le groupe
            species_counts = {}
            for creature in group:
                # Classification simple par taille et vitesse
                size_class = "small" if creature.genome.traits["size"] < 50 else "large"
                speed_class = "slow" if creature.genome.traits["speed"] < 50 else "fast"
                species_key = f"{size_class}_{speed_class}"
                
                if species_key not in species_counts:
                    species_counts[species_key] = 0
                species_counts[species_key] += 1
                
            # Espèce dominante
            dominant_species = max(species_counts, key=species_counts.get)
            
            # Ajuster le comportement en fonction de l'espèce dominante
            for creature in group:
                size_class = "small" if creature.genome.traits["size"] < 50 else "large"
                speed_class = "slow" if creature.genome.traits["speed"] < 50 else "fast"
                creature_species = f"{size_class}_{speed_class}"
                
                if creature_species == dominant_species:
                    # Ajuster le comportement des membres de l'espèce dominante
                    # Ex: augmenter légèrement l'agressivité en groupe
                    if np.random.random() < 0.1 and creature.state == self.EXPLORING:
                        creature.state = self.HUNTING
                else:
                    # Ajuster le comportement des autres espèces
                    # Ex: tendance à fuir si en infériorité numérique
                    if np.random.random() < 0.2 and creature.state != self.FLEEING:
                        creature.state = self.FLEEING
                        # Fuir le centre du groupe
                        center_x = sum(c.x for c in group) / len(group)
                        center_y = sum(c.y for c in group) / len(group)
                        creature.target = (center_x, center_y)
    
    def identify_groups(self, creatures):
        """
        Identifie les groupes de créatures basés sur la proximité.
        Utilise un algorithme de clustering spatial simple.
        """
        if not creatures:
            return []
            
        # Initialiser les groupes
        groups = []
        processed = set()
        
        for creature in creatures:
            if creature in processed:
                continue
                
            # Nouvelle créature, nouveau groupe
            current_group = [creature]
            processed.add(creature)
            
            # Chercher des créatures proches de façon récursive
            self._expand_group(creature, creatures, current_group, processed)
            
            # Ajouter le groupe s'il contient au moins une créature
            if current_group:
                groups.append(current_group)
                
        return groups
    
    def _expand_group(self, creature, all_creatures, current_group, processed, depth=0):
        """
        Fonction récursive pour étendre un groupe en incluant les créatures proches.
        """
        if depth > 5:  # Limite de récursion pour éviter les problèmes de performance
            return
            
        for other in all_creatures:
            if other in processed:
                continue
                
            # Calculer la distance
            distance = np.sqrt((creature.x - other.x)**2 + (creature.y - other.y)**2)
            
            # Si assez proche, ajouter au groupe et continuer la récursion
            if distance <= self.group_distance:
                current_group.append(other)
                processed.add(other)
                self._expand_group(other, all_creatures, current_group, processed, depth + 1)