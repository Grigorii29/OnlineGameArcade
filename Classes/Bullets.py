import arcade
from .CONSTANTES import *
from math import cos, sin, radians


class Bullet(arcade.Sprite):
    def __init__(self, x, y, game, angle, player_speed_x):
        super().__init__()
        self.speed = 10
        self.angle = angle
        self.texture = arcade.load_texture("Files/Bullets images/Bullet0.png")
        self.center_x, self.center_y = x, y
        self.game = game
        self.scale = TANK_SKALE
        self.engine = arcade.PhysicsEngineSimple(self, self.game.collision_list)

        self.change_y = sin(radians(angle)) * self.speed
        self.change_x = cos(radians(angle)) * self.speed + player_speed_x

    def update(self, delta_t):
        upd = self.engine.update()
        self.change_y -= GRAVITY
        if upd:
            self.remove_from_sprite_lists()