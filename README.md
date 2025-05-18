# Evolution Sim 🧬

Une simulation interactive d'évolution de créatures virtuelles développée avec Pygame.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.6+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📝 Description

Evolution Sim modélise un écosystème où des créatures autonomes évoluent dans un environnement dynamique en grille 2D. Chaque créature possède un génome qui définit ses caractéristiques et capacités. Elles interagissent avec leur environnement et entre elles, évoluant au fil des générations selon les principes de la sélection naturelle.

Le joueur peut modifier l'environnement en temps réel, en changeant le terrain, la température, l'humidité, et en déclenchant des catastrophes naturelles pour observer comment les créatures s'adaptent aux nouvelles conditions environnementales.

## ✨ Fonctionnalités

- **Créatures autonomes** : Les créatures se déplacent, cherchent de la nourriture, se reproduisent et interagissent entre elles selon leurs caractéristiques génétiques.
- **Système d'évolution génétique** : Génome, mutations, croisements et sélection naturelle permettant l'adaptation progressive aux conditions environnementales.
- **Environnement modifiable** : Différents types de terrain (eau, désert, forêt, montagne) avec leurs conditions environnementales spécifiques.
- **Catastrophes naturelles** : Inondations, incendies, sécheresses et impacts de météorites modifiant l'écosystème.
- **Interface utilisateur interactive** : Modification du monde, statistiques d'évolution et contrôles de simulation.
- **Visualisation des statistiques** : Suivi de l'évolution des espèces et des tendances adaptatives.
- **Cycle jour/nuit et saisons** : Variations environnementales cycliques affectant les ressources et les conditions.

## 🔧 Installation

1. Assurez-vous d'avoir Python 3.6+ installé
2. Clonez le dépôt :
   ```
   git clone https://github.com/yourusername/evolution_sim.git
   cd evolution_sim
   ```
3. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```
4. Lancez la simulation :
   ```
   python main.py
   ```

## 🎮 Contrôles

| Touche | Action |
|--------|--------|
| **Espace** | Pause/Reprendre la simulation |
| **S** | Avancer d'un pas (quand en pause) |
| **+/-** | Ajuster la vitesse de simulation |
| **1/2/3** | Changer le mode d'édition (terrain, température, humidité) |
| **W/D/F/M** | Sélectionner le type de terrain (eau, désert, forêt, montagne) |
| **F1** | Déclencher une inondation |
| **F2** | Déclencher un incendie |
| **F3** | Déclencher une sécheresse |
| **Souris** | Modifier le monde en cliquant et en faisant glisser |

## 🧬 Concepts d'évolution

### Génome

Le génome de chaque créature définit ses caractéristiques à travers divers traits :

- **Traits physiques** : taille, vitesse, force, portée de vision
- **Traits de survie** : métabolisme, agressivité, taux de reproduction
- **Adaptations environnementales** : tolérance à la chaleur/froid, affinité pour l'eau/montagnes
- **Traits spéciaux** : capacité à nager, grimper
- **Apparence** : couleur (RGB)

### Sélection naturelle

La sélection naturelle opère via plusieurs mécanismes :

1. **Survie différentielle** : Les créatures mal adaptées trouvent moins de nourriture et meurent plus rapidement.
2. **Reproduction différentielle** : Les créatures bien adaptées accumulent plus d'énergie et se reproduisent plus fréquemment.
3. **Sélection par tournoi** : Les parents sont sélectionnés en comparant un petit groupe de créatures et en choisissant les plus adaptées.

### Mutations et croisements

Lors de la reproduction :

1. **Croisement** : Le génome de l'enfant est créé en mélangeant les traits des deux parents.
2. **Mutation** : Certains traits ont une chance aléatoire d'être légèrement modifiés.

Ces mécanismes permettent l'émergence de nouvelles combinaisons de traits et l'adaptation aux changements environnementaux.

## 🔬 Structure du projet

```
evolution_sim/
├── main.py                  # Point d'entrée du programme
├── config.py                # Configuration et paramètres globaux
├── engine/                  # Moteur de jeu
│   ├── game_loop.py         # Boucle de jeu principale
│   └── event_handler.py     # Gestion des événements
├── world/                   # Environnement du monde
│   ├── grid.py              # Grille du monde
│   ├── cell.py              # Cellule individuelle
│   ├── environment.py       # Gestion des environnements
│   └── resources.py         # Gestion des ressources
├── creatures/               # Créatures et évolution
│   ├── creature.py          # Classe de base des créatures
│   ├── genome.py            # Définition du génome
│   ├── behavior.py          # Comportements des créatures
│   └── evolution.py         # Mécanismes d'évolution
├── simulation/              # Logique de simulation
│   ├── population.py        # Gestion des populations
│   └── statistics.py        # Suivi des statistiques
└── ui/                      # Interface utilisateur
    ├── renderer.py          # Système de rendu graphique
    ├── camera.py            # Gestion de la vue
    └── controls.py          # Interface utilisateur
```

## 🛠️ Personnalisation

Vous pouvez modifier les paramètres de la simulation dans le fichier `config.py` :

- Taille de la grille et de l'écran
- Taille initiale de la population
- Taux de mutation et de croisement
- Pression de sélection
- Taux d'apparition de nourriture
- Et bien d'autres paramètres...

## 🚀 Idées d'extension

- Ajout de prédateurs et d'une chaîne alimentaire
- Implémentation d'un système d'écosystèmes plus complexe
- Ajout de barrières géographiques et de migration
- Visualisation graphique avancée des statistiques
- Sauvegarde et chargement de simulations
- Interface graphique plus élaborée

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.