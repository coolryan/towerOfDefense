import arcade
from configs.settings import *
from game.game import *

def main():
    """ Main function """
    game = TowerDefenseGame()
    game.setup()
    
    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()