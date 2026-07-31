import arcade
from configs.settings import *
from game.game import *

def main():
    """ Main function """
    game = TowerDefenseGame()
    
    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()