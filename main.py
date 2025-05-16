import pygame
import sys
from engine.game_loop import GameLoop
from config import Config

def main():
    # Initialisation de Pygame
    pygame.init()
    pygame.display.set_caption("Simulation d'Évolution")
    
    # Création de la fenêtre avec les dimensions définies dans la configuration
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Création et démarrage de la boucle de jeu
    game = GameLoop(screen, clock)
    game.run()
    
    # Nettoyage à la fin du programme
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()