# evolution_sim

Une simulation d'évolution de créatures virtuelles avec Pygame.

## Description

Evolution Sim est une simulation interactive où des créatures autonomes évoluent dans un environnement dynamique. Les créatures possèdent un génome qui définit leurs caractéristiques et capacités. Elles interagissent avec leur environnement et entre elles, et évoluent au fil des générations grâce à un système de sélection naturelle, de reproduction et de mutation.

Le joueur peut modifier l'environnement en temps réel, en changeant le terrain, la température, l'humidité, et en déclenchant des catastrophes naturelles. Cela permet d'observer comment les créatures s'adaptent aux changements environnementaux.

## Fonctionnalités

- **Simulation de créatures autonomes** : Les créatures se déplacent, cherchent de la nourriture, se reproduisent et interagissent entre elles.
- **Système d'évolution génétique** : Génome, mutations, croisements et sélection naturelle.
- **Environnement modifiable** : Différents types de terrain (eau, désert, forêt, montagne) avec leurs conditions environnementales.
- **Catastrophes naturelles** : Inondations, incendies, sécheresses et impacts de météorites.
- **Interface utilisateur interactive** : Modification du monde, statistiques d'évolution et contrôles de simulation.
- **Visualisation des statistiques** : Suivi de l'évolution des espèces et des tendances adaptatives.

## Installation

1. Assurez-vous d'avoir Python 3.6+ installé
2. Installez les dépendances :
   ```
   pip install pygame numpy
   ```
3. Clonez le dépôt :
   ```
   git clone https://github.com/yourusername/evolution_sim.git
   cd evolution_sim
   ```
4. Lancez la simulation :
   ```
   python main.py
   ```

## Contrôles

- **Espace** : Pause/Reprendre la simulation
- **S** : Avancer d'un pas (quand en pause)
- **+/-** : Ajuster la vitesse de simulation
- **1/2/3** : Changer le mode d'édition (terrain, température, humidité)
- **W/D/F/M** : Sélectionner le type de terrain (eau, désert, forêt, montagne)
- **F1/F2/F3** : Déclencher des catastrophes naturelles (inondation, incendie, sécheresse)
- **Souris** : Modifier le monde en cliquant et en faisant glisser

## Structure du projet

```
evolution_sim/
├── main.py                  # Point d'entrée du programme
├── config.py                # Configuration et paramètres globaux
├── engine/                  # Moteur de jeu
│   ├── game_loop.py         # Boucle de jeu principale
│   └── event_handler.py     # Gestion des événements (clavier, souris)
├── world/                   # Environnement du monde
│   ├── grid.py              # Grille du monde
│   ├── cell.py              # Cellule individuelle
│   ├── environment.py       # Gestion des environnements
│   └── resources.py         # Gestion des ressources
├── creatures/               # Créatures et évolution
│   ├── creature.py          # Classe de base des créatures
│   ├── genome.py            # Définition et manipulation du génome
│   ├── behavior.py          # Comportements des créatures
│   └── evolution.py         # Mécanismes d'évolution
├── simulation/              # Logique de simulation
│   ├── population.py        # Gestion des populations
│   └── statistics.py        # Suivi des statistiques
└── ui/                      # Interface utilisateur
    ├── renderer.py          # Système de rendu graphique
    ├── camera.py            # Gestion de la vue
    └── controls.py          # Interface utilisateur pour modifier le monde
```

## Concepts d'évolution

### Génome

Le génome d'une créature définit ses caractéristiques et capacités. Il est représenté par un ensemble de traits numériques (0-100) et booléens. Les principaux traits sont :

- **Traits physiques** : taille, vitesse, force, portée de vision
- **Traits de survie** : métabolisme, agressivité, taux de reproduction
- **Adaptations environnementales** : tolérance à la chaleur/froid, affinité pour l'eau/montagnes
- **Traits spéciaux** : capacité à nager, grimper
- **Apparence** : couleur (RGB)

### Sélection naturelle

La sélection naturelle est implémentée par plusieurs mécanismes :

1. **Survie différentielle** : Les créatures mal adaptées à leur environnement ont moins d'énergie, trouvent moins de nourriture et meurent plus rapidement.
2. **Reproduction différentielle** : Les créatures bien adaptées accumulent plus d'énergie et peuvent se reproduire plus fréquemment.
3. **Sélection par tournoi** : Lors de la reproduction, les parents sont sélectionnés en comparant un petit groupe de créatures et en choisissant les plus adaptées.

### Mutations et croisements

Lors de la reproduction :

1. **Croisement** : Le génome de l'enfant est créé en mélangeant les traits des deux parents.
2. **Mutation** : Certains traits ont une chance aléatoire d'être modifiés légèrement.

Ces mécanismes permettent l'apparition de nouvelles combinaisons de traits et l'exploration de nouvelles stratégies d'adaptation.

## Personnalisation

Vous pouvez modifier les paramètres de la simulation dans le fichier `config.py` :

- Taille de la grille et de l'écran
- Taille initiale de la population
- Taux de mutation et de croisement
- Pression de sélection
- Taux d'apparition de nourriture
- Et bien d'autres paramètres...

## Extension du projet

Voici quelques idées pour étendre le projet :

- Ajout de prédateurs et d'une chaîne alimentaire
- Implémentation d'un système d'écosystèmes plus complexe
- Ajout de barrières géographiques et de migration
- Visualisation graphique avancée des statistiques
- Sauvegarde et chargement de simulations
- Interface graphique plus élaborée

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.