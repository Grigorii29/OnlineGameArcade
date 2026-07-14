import requests
import arcade

from Classes.CONSTANTES import *
from Classes.Tanks import GreenTank, GrayTank
from Classes.Bullets import Bullet, Bullet2

with open('Screen size.txt') as f:
    SCREEN_WIDTH, SCREEN_HEIGHT = [int(line) for line in f]


class Client1(arcade.View):
    def __init__(self):
        super().__init__()
        self.attack = False  # Флаг состояния атака или нет.

        arcade.schedule(self.get_coord, UPDATE_TIME)  # Делаем запросы на сервер постоянными
        arcade.schedule(self.post_coord, UPDATE_TIME)
        arcade.schedule(self.get_bullets_from_player_2, UPDATE_TIME)
        arcade.schedule(self.post_bullet, UPDATE_TIME)

        self.players_list = arcade.SpriteList()  # Создаем спрайтлист, танки, добавляем их в список
        self.player_1 = GreenTank(100, 420, self)
        self.player_2 = GrayTank(0, 0, self)
        self.players_list.append(self.player_1)
        self.players_list.append(self.player_2)

        self.bullets_list = arcade.SpriteList()
        self.player_1_bullets_list = arcade.SpriteList()  # Список, в котором хранятся пули 1-го игрока
        self.player_2_bullets_list = arcade.SpriteList()
        self.blast_list = arcade.SpriteList()  # Список анимаций взрывов
        self.bullets_list_to_server = []

        self.aim = arcade.Sprite('Files/arrow.png')
        self.aim.alpha = 0
        self.aim.scale = 0.3
        self.aim_list = arcade.SpriteList()
        self.aim_list.append(self.aim)

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
            self.player_2.center_x, self.player_2.center_y = response['x'], response['y']
            self.player_2.hp = response['hp']
        except Exception:
            pass

    def post_coord(self, delta_t):
        try:
            response = requests.post(server_address + '/player1', json={
                'x': self.player_1.center_x,
                'y': self.player_1.center_y,
                'hp': self.player_1.hp
            })
        except Exception:
            pass

    def get_bullets_from_player_2(self, delta_t):
        response = requests.get(server_address + '/bullets_to_player_1').json()['Bullets']
        for el in response:
            print(el)
            if el[3] == 'Bullet2':
                self.player_2_bullets_list.append(Bullet2(el[0], el[1], self, el[2]))

    def post_bullet(self, delta_t):
        try:
            # print(self.bullets_list_to_server)
            request = requests.post(server_address + '/bullets_from_player_1', json={
                'bullets': self.bullets_list_to_server
            })
            self.bullets_list_to_server = []
        except Exception:
            pass

    def on_draw(self):
        self.clear()
        self.camera_shake.update_camera()  # Запчасть от тряски камеры
        self.camera.use()
        self.details_list.draw()
        self.land_list.draw()
        self.players_list.draw()
        self.aim_list.draw()
        self.player_1_bullets_list.draw()
        self.player_2_bullets_list.draw()
        self.blast_list.draw()

    def on_update(self, delta_t):
        self.engine.update()
        self.player_1.change_y -= GRAVITY
        self.players_list.update(delta_t)
        self.update_speed()
        self.camera_update(delta_t)
        self.player_1_bullets_list.update()
        self.player_2_bullets_list.update()
        self.blast_list.update()
        self.update_bullets()

        if self.attack:
            self.aim.center_x = self.player_1.center_x + 40
            self.aim.center_y = self.player_1.center_y + 30

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F:
            if self.attack:
                self.attack = False
                self.aim.alpha = 0
            else:
                self.attack = True
                self.accel = False
                self.aim.alpha = 255  # Обработка появления прицела
        if not self.attack:
            if key == arcade.key.LEFT:
                self.accel = True
                self.forward = False
            elif key == arcade.key.RIGHT:
                self.accel = True
                self.forward = True
        if key == arcade.key.SPACE and self.attack:
            bullet = Bullet(self.player_1.center_x + 40, self.player_1.center_y + 30, self, -self.aim.angle)
            self.player_1_bullets_list.append(bullet)
            self.bullets_list_to_server.append([bullet.center_x, bullet.center_y, bullet.angle, 'Bullet'])
            # print([bullet.center_x, bullet.center_y, bullet.angle, 'Bullet'])

        if self.attack:
            if key == arcade.key.UP:
                if self.aim.angle > -90:
                    self.aim.angle -= 5
            if key == arcade.key.DOWN:
                if -90 <= self.aim.angle < 0:
                    self.aim.angle += 5

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.LEFT, arcade.key.RIGHT]:
            self.accel = False

    def update_speed(self):  # Функия для расчета текущей скорости в зависимости от зажатых клавиш
        if self.player_1.center_x < 10:
            self.player_1.change_x = 0
            self.player_1.center_x = 10

        elif self.player_1.center_x > 8390:
            self.player_1.change_x = 0
            self.player_1.center_x = 8390

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
        self.world_width = int(tile_map.width * tile_map.tile_width)
        self.world_height = int(tile_map.height * tile_map.tile_height)

        # ! Подключаем простой движок к текущему игроку
        self.engine = arcade.PhysicsEngineSimple(self.player_1, self.collision_list)

    def update_bullets(self):
        for el in arcade.check_for_collision_with_list(self.player_1, self.player_2_bullets_list):
            el.start_blast()
            self.player_1.hp -= 15

        # Уменьшение здоровья за столкновение со следом взрыва
        self.player_1.hp -= 0.5 * len(arcade.check_for_collision_with_list(self.player_1, self.blast_list))

        if self.player_1.hp <= 0:  # Удаляю танк при смерти
            self.player_1.texture = arcade.load_texture('Files/Green tank/Tank1.png')

        # Для более реалистичной отрисовки проверяю коллизии и для 2-го танка
        for el in arcade.check_for_collision_with_list(self.player_2, self.player_1_bullets_list):
            el.start_blast()

        if self.player_2.hp <= 0:
            self.player_2.texture = arcade.load_texture('Files/Gray tank/Tank1.png')


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    client = Client1()
    window.show_view(client)
    arcade.run()


if __name__ == '__main__':
    main()
