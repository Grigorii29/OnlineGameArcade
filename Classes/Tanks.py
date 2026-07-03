import arcade
from Classes.CONSTANTES import *


class GreenTank(arcade.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.texture = arcade.load_texture('Files/Green tank/Tank0.png')
        self.center_x = x
        self.center_y = y
        self.scale = TANK_SKALE

    def on_update(self, dt):
        self.center_x += self.change_x * dt


class GrayTank(arcade.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.texture = arcade.load_texture('Files/Gray tank/Tank0.png')
        self.center_x = x
        self.center_y = y
        self.scale_x = -TANK_SKALE
        self.scale_y = TANK_SKALE

    def on_update(self, dt):
        self.center_x += self.change_x * dt
