import requests
import arcade

from Classes.CONSTANTES import *
from Classes.Tanks import GreenTank

with open('Screen size.txt') as f:
    SCREEN_WIDTH, SCREEN_HEIGHT = [int(line) for line in f]


class Client1(arcade.View):
    def __init__(self):
        super().__init__()
        self.pl1_x = 100
        self.pl1_y = 420
        self.pl2_x = 0
        self.pl2_y = 0
        arcade.schedule(self.get_coord, UPDATE_TIME)
        arcade.schedule(self.post_coord, UPDATE_TIME)
        self.player_1 = GreenTank(self.pl1_x, self.pl1_y, self)
        self.players_list = arcade.SpriteList()
        self.players_list.append(self.player_1)
        self.map_setup()
        self.accel = False  # Флаг ускорения
        self.forward = False  # Флаг для направления ускорения
        self.camera = arcade.camera.Camera2D()
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.camera.view_data,  # Трястись будет только то, что попадает в объектив мировой камеры
            max_amplitude=15.0,  # Параметры, с которыми можно поиграть
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

    def get_coord(self, delta_t):  # Клиент 1, поэтому принимаю координаты второго, отправляю свои
        try:
            response = requests.get(server_address + '/player2').json()
            self.pl2_x = response['x']
            self.pl2_y = response['y']
        except Exception:
            pass

    def post_coord(self, delta_t):
        try:
            response = requests.post(server_address + '/player1', json={
                'x': self.pl1_x,
                'y': self.pl1_y
            })
        except Exception:
            pass

    def on_draw(self):
        self.clear()
        self.camera_shake.update_camera()  # Запчасть от тряски камеры
        self.camera.use()
        self.land_list.draw()
        self.details_list.draw()
        self.players_list.draw()
        arcade.draw_circle_filled(self.pl2_x, self.pl2_y, 20, arcade.color.SKY_BLUE)

    def on_update(self, delta_t):
        self.engine.update()
        self.player_1.change_y -= 1
        self.players_list.update(delta_t)
        self.update_speed()
        self.camera_update(delta_t)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.accel = True
            self.forward = False
        elif key == arcade.key.RIGHT:
            self.accel = True
            self.forward = True

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.accel = False

    def update_speed(self):
        if self.player_1.center_x < 10:
            self.player_1.change_x = 0
            self.player_1.center_x = 10
        else:
            if self.accel and self.forward and abs(self.player_1.change_x) < 3:
                self.player_1.change_x += SPEED_DELTA
            elif self.accel and not self.forward and abs(self.player_1.change_x) < 3:
                self.player_1.change_x -= SPEED_DELTA
            if self.accel is False and self.player_1.change_x > 0:
                self.player_1.change_x -= SPEED_DELTA
            elif self.accel is False and self.player_1.change_x < 0:
                self.player_1.change_x += SPEED_DELTA
            if 0 < abs(self.player_1.change_x) <= 0.05:
                self.player_1.change_x = 0

    def camera_update(self, delta_t):
        self.camera_shake.update(delta_t)
        cam_x, cam_y = self.camera.position
        dz_left = cam_x - DEAD_ZONE_W // 2
        dz_right = cam_x + DEAD_ZONE_W // 2
        dz_bottom = cam_y - DEAD_ZONE_H // 2
        dz_top = cam_y + DEAD_ZONE_H // 2

        px, py = self.player_1.center_x, self.player_1.center_y
        target_x, target_y = cam_x, cam_y

        if px < dz_left:
            target_x = px + DEAD_ZONE_W // 2
        elif px > dz_right:
            target_x = px - DEAD_ZONE_W // 2
        if py < dz_bottom:
            target_y = py + DEAD_ZONE_H // 2
        elif py > dz_top:
            target_y = py - DEAD_ZONE_H // 2

        # Не показываем «пустоту» за краями карты
        half_w = self.camera.viewport_width / 2
        half_h = self.camera.viewport_height / 2
        target_x = max(half_w, min(self.world_width - half_w, target_x))
        target_y = max(half_h, min(self.world_height - half_h, target_y))

        # Плавно к цели, аналог arcade.math.lerp_2d, но руками
        smooth_x = (1 - CAMERA_LERP) * cam_x + CAMERA_LERP * target_x
        smooth_y = (1 - CAMERA_LERP) * cam_y + CAMERA_LERP * target_y
        self.cam_target = (smooth_x, smooth_y)

        self.camera.position = (self.cam_target[0], self.cam_target[1])
    def map_setup(self):
        tile_map = arcade.load_tilemap('Files/map_for_tanks.tmx', scaling=1)
        self.collision_list = tile_map.sprite_lists['collision']
        self.details_list = tile_map.sprite_lists['details']
        self.land_list = tile_map.sprite_lists['Land']
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.engine = arcade.PhysicsEngineSimple(self.player_1, self.collision_list)
        self.world_width = int(tile_map.width * tile_map.tile_width)
        self.world_height = int(tile_map.height * tile_map.tile_height)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    client = Client1()
    window.show_view(client)
    arcade.run()


if __name__ == '__main__':
    main()
