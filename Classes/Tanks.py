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
        self.hp = 100

    def update(self, dt):
        if self.hp <= 0:
            self.texture = arcade.load_texture('Files/Green tank/Died.png')

    def revival(self): # Функция оживления
        self.center_x = 100
        self.center_y = 420
        self.hp = 100
        self.texture = arcade.load_texture('Files/Green tank/Tank0.png')



class GrayTank(arcade.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game
        self.texture = arcade.load_texture('Files/Gray tank/Tank0.png')
        self.center_x = x
        self.center_y = y
        self.scale_x = -TANK_SKALE
        self.scale_y = TANK_SKALE
        self.hp = 100

    def update(self, dt):
        if self.hp <= 0:
            self.texture = arcade.load_texture('Files/Gray tank/Died.png')

    def revival(self): # Функция оживления
        self.center_x = 100
        self.center_y = 420
        self.hp = 100
        self.texture = arcade.load_texture('Files/Gray tank/Tank0.png')
