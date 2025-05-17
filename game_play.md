Je vais vous expliquer le fonctionnement de cette simulation d'évolution. Il s'agit d'un projet complet qui simule l'évolution de créatures dans un environnement dynamique.

## Vue d'ensemble

Cette simulation modélise un écosystème où des créatures autonomes évoluent dans un monde en grille 2D. Chaque créature possède un génome qui définit ses traits et capacités. Les créatures interagissent avec leur environnement et entre elles, et évoluent au fil des générations grâce à des mécanismes de sélection naturelle, de reproduction et de mutation.

## Composants principaux

### Le monde (World)
- Une grille 2D divisée en cellules
- Chaque cellule a un type de terrain (eau, désert, forêt, montagne)
- Les cellules possèdent des propriétés environnementales (température, humidité)
- Des ressources (nourriture, eau) sont disponibles dans les cellules

### Les créatures
- Possèdent un génome qui définit leurs caractéristiques
- Se déplacent dans le monde à la recherche de nourriture
- Dépensent de l'énergie pour se déplacer et survivre
- Peuvent se reproduire si elles ont suffisamment d'énergie
- Meurent si leur énergie tombe à zéro ou si elles vieillissent trop

### Système d'évolution
- Croisement génétique lors de la reproduction
- Mutations aléatoires qui modifient les traits
- Sélection naturelle (les mieux adaptés survivent plus longtemps)
- Adaptation à l'environnement (les traits avantageux dans certains environnements sont favorisés)

### Événements environnementaux
- Cycle jour/nuit qui affecte les conditions
- Saisons qui modifient la température et l'humidité
- Catastrophes naturelles (inondations, incendies, sécheresses)

## Fonctionnement du cycle de simulation

1. **Initialisation**:
   - Génération d'une carte du monde avec différents terrains
   - Création d'une population initiale de créatures avec des génomes aléatoires

2. **Boucle principale**:
   - Mise à jour de l'environnement (conditions climatiques, ressources)
   - Mise à jour de chaque créature:
     - Décision du comportement (exploration, chasse, fuite, reproduction)
     - Déplacement et consommation d'énergie
     - Interaction avec l'environnement et les autres créatures
   - Gestion des événements environnementaux
   - Rendu graphique de la simulation

3. **Cycle jour/nuit**:
   - À la fin de chaque jour:
     - Déclenchement de la reproduction
     - Analyse des statistiques d'évolution
     - Événements possibles comme catastrophes naturelles

## Mécanismes d'évolution en détail

### Génome
Le génome des créatures définit plusieurs types de traits:
- **Traits physiques**: taille, vitesse, force, vision
- **Traits de survie**: métabolisme, agressivité, taux de reproduction
- **Adaptations environnementales**: tolérance à la chaleur/froid, affinité pour l'eau/montagnes
- **Traits spéciaux**: capacité à nager, grimper
- **Apparence**: couleur (RGB)

### Reproduction
Lorsque deux créatures se reproduisent:
1. Les génomes des parents sont croisés (chaque trait a 50% de chance de venir de chaque parent)
2. Des mutations peuvent survenir (certains traits sont modifiés aléatoirement)
3. Les parents dépensent de l'énergie pour créer l'enfant
4. Un cooldown de reproduction est appliqué aux parents

### Adaptation
- Les créatures avec des traits adaptés à leur environnement:
  - Trouvent plus facilement de la nourriture
  - Dépensent moins d'énergie pour se déplacer
  - Survivent plus longtemps et se reproduisent davantage
- Les créatures mal adaptées:
  - Peinent à trouver de la nourriture
  - Dépensent plus d'énergie
  - Meurent plus rapidement

## Interface utilisateur et contrôles

La simulation offre une interface utilisateur interactive permettant de:
- Modifier le terrain (eau, désert, forêt, montagne)
- Ajuster les conditions environnementales (température, humidité)
- Déclencher des catastrophes naturelles
- Mettre en pause, accélérer ou ralentir la simulation
- Visualiser des statistiques sur l'évolution des espèces

## Émergence de comportements complexes

Avec le temps, on peut observer:
- L'émergence d'espèces différentes adaptées à des niches écologiques spécifiques
- Des migrations de populations suite à des changements environnementaux
- Des oscillations de population en fonction des ressources disponibles
- Des adaptations face aux catastrophes naturelles

Cette simulation est un exemple fascinant de la façon dont des règles simples peuvent générer des comportements complexes et illustrer les principes de l'évolution naturelle par sélection.