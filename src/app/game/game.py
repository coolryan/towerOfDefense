import arcade
from entities.entity import *
from configs.settings import *
from ui.ui import *

class TowerDefenseGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.AMAZON

        # game state variables
        self.gold = 100
        self.mouse_x, self.mouse_y = 0, 0
        self.selected_tower_type = "Basic"
        self.towers = []
        self.dragging = False

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.enemy_list = arcade.SpriteList()
        self.tower_list = arcade.SpriteList()

    def setup(self):
        # Create a tower & enemy
        tower = Tower(400, 300)
        self.tower_list.append(tower)

        enemy = Enemy()
        self.enemy_list.append(enemy)

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_update(self, delta_time):
            """
            All the logic to move, and the game logic goes here.
            Normally, you'll call update() on the sprite lists that
            need it.
            """
            self.enemy_list.update()
            self.tower_list.on_update(delta_time)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.tower_list.draw()
        self.enemy_list.draw_health_bar()

        self.towerOfDefenseUI = self.towerOfDefenseUI()

        # Draw UI text
        arcade.draw_text(f"Gold: {self.gold}", 10, 560, arcade.color.BLACK, 20)
        arcade.draw_text(
            f"Selected: {self.selected_tower_type}",
            10,
            530,
            arcade.color.BLACK,
            14,
        )
        arcade.draw_text(
            "Keys: [1] Basic Tower, [2] Heavy Tower",
            10,
            500,
            arcade.color.BLACK,
            12,
        )

        # Draw placed towers
        for x, y, color in self.towers:
            arcade.draw_circle_filled(x, y, 20, color)

        # Draw ghost tower on mouse hover
        arcade.draw_circle_filled(self.mouse_x, self.mouse_y, 20, (0, 0, 255, 100))

    # --- Keyboard Events ---
    def on_key_press(self, symbol: int, modifiers: int):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if symbol == arcade.key.KEY_1:
            self.selected_tower_type = "Basic Tower"
            print("selected Basic Tower")
        elif symbol == arcade.key.KEY_2:
            self.selected_tower_type = "Heavy Tower"
            print("selected Heavy Tower")
        elif symbol == arcade.key.ESCAPE:
            self.close()
    
    def on_key_release(self, symbol: int, modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if symbol == arcade.key.KEY_1 or symbol == arcade.key.KEY_2:
            print("Tower selection key released.")

    # --- Mouse Motion Events ---
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Called whenever the mouse moves.
        """
        self.mouse_x, self.mouse_y = x, y

    def on_mouse_press(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            # Spend gold & place a tower
            if self.gold >= 50:
                color = (
                    arcade.color.BLUE
                    if self.selected_tower_type == "Basic Tower"
                    else arcade.color.RED
                )
                self.towers.append((x, y, color))
                self.gold -= 50
                print(f"Placed {self.selected_tower_type} at ({x}, {y})")
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.dragging = True
            print("Started right-click drag mode.")

    def on_mouse_release(self, x: float, y: float, button: int, key_modifiers: int):
        """
        Called when a user releases a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_RIGHT:
            self.dragging = False
            print("Ended right-click drag mode.")
    
    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        """Called when the user drags the mouse."""
        self.mouse_x, self.mouse_y = x, y
        if self.dragging:
            # Dragging to pan map or remove towers
            pass
    
    def on_mouse_scroll(self, x: float, y: float, scroll_x: float, scroll_y: float):
        """Called when the user scrolls the mouse wheel."""
        if scroll_y > 0:
            print("Zoom in or cycle forward.")
        else:
            print("Zoom in or cycle forward.")