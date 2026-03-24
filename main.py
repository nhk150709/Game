"""
Space RTS — Entry Point
=======================
Run this file to start the game:

    python main.py

Requirements:
    pip install pygame
"""
import sys
import pygame

def main():
    pygame.init()
    pygame.font.init()

    from core.game import Game
    game = Game()
    game.run()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
