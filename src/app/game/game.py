import arcade
from entities.entity import *
from entities.towerTypes import TowerType
from configs.settings import *
from ui.ui import *

# Number keys 1-9 select tower types in the order they're listed in TowerType.
# Keys past the last tower type do nothing until more types are added.
TOWER_KEYS = [
    arcade.key.KEY_1, arcade.key.KEY_2, arcade.key.KEY_3,
    arcade.key.KEY_4, arcade.key.KEY_5, arcade.key.KEY_6,
    arcade.key.KEY_7, arcade.key.KEY_8, arcade.key.KEY_9,
]

levels = {
    # List of (x, y) coordinates represenating the turns on the map path
    1: {
        "map": "./resources/images/backgrounds/map.gif",
        "waypoints": [
            # arcade's y-axis starts at the bottom of the screen, so these are
            # measured from the bottom-left corner of the map
            (0, 340), # spawn point (left side)
            (280, 340), # first turn (goes up)
            (280, 515), # second turn (goes right, across the top bridge)
            (1240, 515), # third turn (goes down)
            (1240, 340), # fourth turn (goes left)
            (1000, 340), # fifth turn (goes down)
            (1000, 245), # sixth turn (goes right)
            (1280, 245), # exit point (right side)
        ],
        "towerLocations": [
            # each spot is on open grass next to the path, in path order
            (136, 396), # above the entry road
            (295, 285), # grass just outside the bottom-left corner of the path
            (336, 576), # above the top-left corner
            (772, 616), # above the road, just before the top bridge
            (824, 460), # below the road, just before the top bridge
            (1028, 460), # below the road, just after the top bridge
            (1150, 420), # inside the right-hand loop
            (1176, 192), # below the exit road
        ],
        "enemyWaves": [
            {
                "startTime": 1,
                "phrases": [
                    {
                        "time": 0,
                        "enemyLevels": [1]
                    },
                    {
                        "time": 5,
                        "enemyLevels": [1,1]
                    },
                    {
                        "time": 10,
                        "enemyLevels": [1,1,1]
                    }
                ]
            },
            {
                "startTime": 15,
                "phrases": [
                    {
                        "time": 0,
                        "enemyLevels": [2]
                    },
                    {
                        "time": 5,
                        "enemyLevels": [2,1,1]
                    },
                    {
                        "time": 10,
                        "enemyLevels": [2,2,2]
                    }
                ]
            }
        ]
    },
}

class TowerDefenseGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_textures = []

        # game state variables
        self.gold = 100
        self.lives = 20  # lose one each time an enemy makes it to the exit
        self.game_over = False
        self.mouse_x, self.mouse_y = 0, 0
        self.selected_tower_type = TowerType.BASIC
        self.dragging = False

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.enemy_list = arcade.SpriteList()
        self.tower_list = arcade.SpriteList()
        self.projectile_list = []

        #self.enemy_path = [(0, 360), (1280, 360)]  # walk straight across the middle of the screen
        self.enemy_path = levels.get(1).get("waypoints")
        self.tower_locations = levels.get(1).get("towerLocations")
        self.tower_spot_size = 0  # set in setup() to match the tower's width
        self.occupied_spots = set()  # tower locations that already have a tower
        # Enemy waves: build a list of (spawn time, enemy level) for every enemy
        # in every wave, sorted so the next enemy to spawn is always first.
        self.game_time = 0.0  # seconds since the game started
        self.enemy_spacing = 0.75  # seconds between enemies in the same phrase, so they don't stack
        self.spawn_schedule = []
        for wave in levels.get(1).get("enemyWaves"):
            for phrase in wave["phrases"]:
                phrase_time = wave["startTime"] + phrase["time"]
                for i, level in enumerate(phrase["enemyLevels"]):
                    self.spawn_schedule.append((phrase_time + i * self.enemy_spacing, level))
        self.spawn_schedule.sort()

    def setup(self):
        image_files = [
            levels.get(1).get("map"),
            # "./resources/images/backgrounds/Background_medieval_4.webp",
            # "./resources/images/backgrounds/empty-silhouette-medieval-background.jpg",
            # "./resources/images/backgrounds/MedievalKingdom.jpg"
        ]

        for file_path in image_files:
            texture = arcade.load_texture(file_path)
            self.background_textures.append(texture)

        # We start with no towers. Tower spots are squares as wide as a tower,
        # marking where its base goes, so measure a sample tower for the size.
        self.tower_spot_size = Tower(0, 0).width

        # Create an enemy

        # enemy = Enemy(self.enemy_path, level=self.enemy_level)
        # self.enemy_list.append(enemy)

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
            if self.game_over:
                return

            ## Add enemies
            self.enemy_list.update()
            self.game_time += delta_time
            # spawn every enemy whose time has come
            while self.spawn_schedule and self.spawn_schedule[0][0] <= self.game_time:
                _, level = self.spawn_schedule.pop(0)
                self.enemy_list.append(Enemy(self.enemy_path, level=level))

            # enemies that make it to the exit cost us a life
            for enemy in list(self.enemy_list):
                if enemy.reached_end:
                    enemy.remove_from_sprite_lists()
                    self.lives -= 1
            if self.lives <= 0:
                self.lives = 0
                self.game_over = True

            

            for tower in self.tower_list:
                tower.on_update(delta_time, self.enemy_list, self.projectile_list)

            for projectile in self.projectile_list:
                projectile.update(delta_time)
                self.gold += projectile.gold_reward
            self.projectile_list = [p for p in self.projectile_list if p.alive]

    def on_draw(self):
        """
        Render the screen.
        """
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        for i, texture in enumerate(self.background_textures):
            arcade.draw_texture_rect(
                texture = texture,
                rect = arcade.LBWH(i * SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
            )

        # Draw a gray box on every empty spot where a tower can be placed
        for x, y in self.tower_locations:
            if (x, y) in self.occupied_spots:
                continue
            spot = arcade.XYWH(x, y, self.tower_spot_size, self.tower_spot_size)
            arcade.draw_rect_filled(spot, (128, 128, 128, 160))
            arcade.draw_rect_outline(spot, arcade.color.DARK_GRAY, 2)

        self.tower_list.draw()
        self.enemy_list.draw()
        for projectile in self.projectile_list:
            projectile.draw()
        for enemy in self.enemy_list:
            enemy.draw_health_bar()

        # Draw UI text
        arcade.draw_text(f"Lives: {self.lives}", 10, 590, arcade.color.BLACK, 20)
        arcade.draw_text(f"Gold: {self.gold}", 10, 560, arcade.color.BLACK, 20)
        selected = self.selected_tower_type.value
        arcade.draw_text(
            f"Selected: {selected.name} Tower (${selected.cost})",
            10,
            530,
            arcade.color.BLACK,
            14,
        )
        tower_keys_text = ", ".join(
            f"[{i}] {tower_type.value.name} ${tower_type.value.cost}"
            for i, tower_type in enumerate(TowerType, start=1)
        )
        arcade.draw_text(
            f"Keys: {tower_keys_text}",
            10,
            500,
            arcade.color.BLACK,
            12,
        )

        # Draw ghost tower on mouse hover, with the selected tower's range around it
        arcade.draw_circle_filled(self.mouse_x, self.mouse_y, 20, (0, 0, 255, 100))
        arcade.draw_circle_outline(self.mouse_x, self.mouse_y, selected.range, (0, 0, 255, 100), 2)

        if self.game_over:
            arcade.draw_text(
                "GAME OVER",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.RED,
                64,
                anchor_x="center",
                anchor_y="center",
                bold=True,
            )

    # --- Keyboard Events ---
    def on_key_press(self, symbol: int, modifiers: int):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        if symbol in TOWER_KEYS:
            tower_types = list(TowerType)
            index = TOWER_KEYS.index(symbol)
            if index < len(tower_types):
                self.selected_tower_type = tower_types[index]
                print(f"selected {self.selected_tower_type.value.name} Tower")
        elif symbol == arcade.key.ESCAPE:
            self.close()
    
    def on_key_release(self, symbol: int, modifiers: int):
        """
        Called whenever the user lets off a previously pressed key.
        """
        if symbol in TOWER_KEYS:
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
            # Spend gold & place a tower, but only on an empty tower spot
            spot = self.find_tower_spot(x, y)
            if spot is None:
                return
            tower_cost = self.selected_tower_type.value.cost
            if self.gold < tower_cost:
                print(f"Not enough gold to place a {self.selected_tower_type.value.name} Tower.")
                return
            self.place_tower(spot, self.selected_tower_type)
            self.gold -= tower_cost
            print(f"Placed {self.selected_tower_type.value.name} Tower at {spot}")
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.dragging = True
            print("Started right-click drag mode.")

    def find_tower_spot(self, x, y):
        """Return the empty tower spot under (x, y), or None if there isn't one."""
        half = self.tower_spot_size / 2
        for spot_x, spot_y in self.tower_locations:
            if (spot_x, spot_y) in self.occupied_spots:
                continue
            if abs(x - spot_x) <= half and abs(y - spot_y) <= half:
                return (spot_x, spot_y)
        return None

    def place_tower(self, spot, tower_type: TowerType = TowerType.BASIC):
        """Build a tower of the given type standing on the given spot."""
        spot_x, spot_y = spot
        tower = Tower(spot_x, spot_y, tower_type)

        # The tower image has empty space under it, so line up the bottom of
        # the visible tower with the bottom of the gray square.
        image = tower.texture.image
        base_offset = (image.getbbox()[3] - image.height / 2) * tower.scale_y
        tower.center_y = spot_y - self.tower_spot_size / 2 + base_offset

        self.tower_list.append(tower)
        self.occupied_spots.add(spot)

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