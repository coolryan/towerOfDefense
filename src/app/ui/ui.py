import arcade
import arcade.gui

class TowerDefesneView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Game stats
        self.money, self.score = 100, 0

        # Sprites
        self.enemy_list = arcade.SpriteList()
        self.tower_list = arcade.SpriteList()

        # Setup GUI layout
        self.v_box = arcade.gui.UIBoxLayout(vertical=False)

        # Build Tower button
        self.btn_build = arcade.gui.UIFlatButton(
            text="Build Tower ($50)", width=180
        )
        self.v_box.add(self.btn_build.with_space_around(right=20))

        # Wave start button
        self.btn_wave = arcade.gui.UIFlatButton(
            "Start Wave", width=140
        )
        self.v_box.add(self.btn_wave)

        # attach click triggers
        self.btn_build.on_click = self.on_click_build
        self.btn_wave.on_click = self.btn_wave

        # add widget manager to anchor layout
        self.manager.add(
            arcade.gui.UIAnchorLayout(
                anchor_x="center", anchor_y="button", align_y=20, child=self.v_box
            )
        )

        def on_click_build(self, event):
            if self.money >= 50:
                self.money -= 50

            # create a simple shape-based or colored sprite for the tower
            tower = arcade.SpriteSolidColor(40, 40, arcade.color.BLUE)
            tower.center_x = 400
            tower.center_y = 300
            self.tower_list.append(tower)

        def on_click_wave(self, event):
            # Spawn an enemy at the top moving down
            enemy = arcade.SpriteSolidColor(30, 30, arcade.color.RED)
            enemy.center_x = 100
            enemy.center_y = 550
            enemy.change_y = -1.0
            self.enemy_list.append(enemy)

        def on_draw(self):
            self.clear()
            arcade.set_background_color(arcade.csscolor.DARK_OLIVE_GREEN)

            # Draw game entities
            self.tower_list.draw()
            self.enemy_list.draw()

            # draw HUD text
            arcade.draw_text(
                f"Money: ${self.money}", 20, 560, arcade.color.WHITE, 16
            )

            arcade.draw_text(
                f"Score: ${self.score}", 20, 535, arcade.color.WHITE, 16
            )

            # draw GUI manager
            self.manager.draw()

        def on_update(self, delta_time):
            self.enemy_list.update()

            # Simple check if enemy reached button
            for enemy in self.enemy_list:
                if enemy.center_y < 0:
                    enemy.remove_from_sprite_lists()