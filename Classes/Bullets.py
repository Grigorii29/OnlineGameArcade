import arcade
from Classes.Blast import Blast
from .CONSTANTES import *
from math import cos, sin, radians, acos, degrees


class Bullet(arcade.Sprite):
    def __init__(self, x, y, game, angle):
        super().__init__()
        self.speed = 15
        self.angle = angle
        self.texture = arcade.load_texture("Files/Bullets images/Bullet0.png")
        self.center_x, self.center_y = x, y
        self.game = game
        self.scale = TANK_SKALE
        self.engine = arcade.PhysicsEngineSimple(self, self.game.collision_list)
        self.damage = 15

        self.change_y = sin(radians(angle)) * self.speed
        self.change_x = cos(radians(angle)) * self.speed

    def update(self, delta_t):
        upd = self.engine.update()
        if upd:
            self.remove_from_sprite_lists()
            self.game.blast_list.append(Blast(self.center_x, self.center_y))
        current_speed = (
                                self.change_x ** 2 + self.change_y ** 2) ** 0.5  # Расчёт текущей скорости, чтобы определить угол
        self.angle = degrees(acos(self.change_x / current_speed))
        if self.change_y > 0:
            self.angle *= -1
        self.change_y -= GRAVITY

    def start_blast(self):
        self.remove_from_sprite_lists()
        self.game.blast_list.append(Blast(self.center_x, self.center_y))


class Rocket(arcade.Sprite):
    def __init__(self, x, y, game, angle):
        super().__init__()
        self.speed = 35
        self.angle = angle
        self.scale = TANK_SKALE
        self.damage = 30
        if 40 <= self.angle <= 50 or -230 <= self.angle <= -220:
            self.texture = arcade.load_texture("Files/Bullets images/Rocket0_fly.png")
            self.center_x, self.center_y = x + 20, y + 20
        else:
            self.texture = arcade.load_texture("Files/Bullets images/Rocket0.png")
            self.center_x, self.center_y = x, y
        self.game = game
        self.scale = TANK_SKALE
        self.engine = arcade.PhysicsEngineSimple(self, self.game.collision_list)

        self.change_y = sin(radians(angle)) * self.speed
        self.change_x = cos(radians(angle)) * self.speed

    def update(self, delta_t):
        upd = self.engine.update()
        if upd:
            self.remove_from_sprite_lists()
            self.game.blast_list.append(Blast(self.center_x, self.center_y))
        current_speed = (
                                self.change_x ** 2 + self.change_y ** 2
                        ) ** 0.5  # Расчёт текущей скорости, чтобы определить угол
        self.angle = degrees(acos(self.change_x / current_speed))
        if self.change_y > 0:
            self.angle *= -1
        self.change_y -= GRAVITY * 0.85

    def start_blast(self):
        self.remove_from_sprite_lists()
        self.game.blast_list.append(Blast(self.center_x, self.center_y))
