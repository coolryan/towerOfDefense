import arcade
from configs.settings import *
from game.game import GameView

def main():
    """ Main function """
    # Create a window class. This is what actually shows on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

    # Create & setup the GameView
    game_view = GameView()

    # Show GameView on screen
    window.show_view(game_view)

    # Start the arcade game loop
    arcade.run()

if __name__ == "__main__":
    main()