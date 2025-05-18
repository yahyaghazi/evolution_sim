class Config:
    """
    Configuration globale pour la simulation d'évolution.
    Centralise tous les paramètres ajustables du jeu.
    """

    # Paramètres de l'écran
    SCREEN_WIDTH = 1200   # Ajustez selon la résolution de votre écran
    SCREEN_HEIGHT = 800  # Ajustez selon la résolution de votre écran
    FPS = 120             # Augmentez pour plus de fluidité

    # Paramètres du monde
    GRID_WIDTH = 120   # Nombre de cellules en largeur
    GRID_HEIGHT = 80  # Nombre de cellules en hauteur
    CELL_SIZE = 20     # Taille d'une cellule en pixels

    # Types d'environnements
    ENVIRONMENTS = {
        'water': (0, 0, 255),        # Bleu
        'desert': (237, 201, 175),   # Beige
        'forest': (34, 139, 34),     # Vert forêt
        'mountain': (139, 137, 137)  # Gris
    }

    # Paramètres des créatures
    INITIAL_POPULATION = 100  # Population initiale
    CREATURE_MIN_SIZE = 2     # Taille minimale d'une créature
    CREATURE_MAX_SIZE = 8     # Taille maximale d'une créature

    # Paramètres d'évolution
    MUTATION_RATE = 0.05      # Probabilité de mutation (5%)
    CROSSOVER_RATE = 0.7      # Probabilité de croisement (70%)
    SELECTION_PRESSURE = 1.5  # Influence de la fitness sur la sélection

    # Paramètres de simulation
    FOOD_SPAWN_RATE = 0.003   # Probabilité d'apparition de nourriture par cellule
    DAY_LENGTH = 500          # Durée d'un jour en frames

    # Paramètres de l'interface
    UI_PANEL_WIDTH = 200      # Largeur du panneau d'interface utilisateur