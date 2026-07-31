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

        self.player = Player()
        self.path = [(100, 100), (700, 500), (100, 500)]
        self.enemies = []
        self.towers = [Tower(400, 300)]
        self.spawn_timer = 0


        # If you have sprite lists, you should create them here,
        # and set them to None
        self.towerOfDefenseUI = self.towerOfDefenseUI()

    def reset(self):
        """Reset the game to the initial state."""
        # Do changes needed to restart the game here if you want to support that
        pass

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        arcade.start_render()

        # draw path
        arcade.draw_line_strip(self.path, arcade.color.YELLOW, 4)

        # draw entities
        for enemy in self.enemies:
            enemy.draw()

        for tower in self.towers:
            tower.draw()

        # draw UI text
        arcade.draw_text(f"Gold: {self.player.gold}", 10, 560, arcade.color.WHITE, 18)
        arcade.draw_text(f"Lives: {self.player.lives}", 150, 560, arcade.color.WHITE, 18)

        # draw UI
        self.towerOfDefenseUI.on_draw()

        # Call draw() on all your sprite lists below
    
    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        # Spawn enemies over time
        self.spawn_timer += 1
        if self.spawn_timer > 90:
            self.enemies.append(Enemy(self.path))
            self.spawn_timer = 0

        # update entities
        for enemy in self.enemies:
            enemy.update()

            if not enemy.active & enemy.health <= 0:
                self.player.gold += 10
            elif not enemy.active:
                self.player.lives -= 1

        # remove dead/finished enemies
        self.enemies = [e for e in self.enemies if e.active]

        # always update ui
        self.towerOfDefenseUI.on_update()

    def on_key_press(self, symbol, modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass
    
    def on_key_release(self, symbol, modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass
    
    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass
    
    def on_mouse_drag(self, x, y, dx, dy, _buttons, _modifiers):
        """Called when the user drags the mouse."""
        pass
    
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Called when the user scrolls the mouse wheel."""
        pass