# Класс взрыва для анимации
import arcade

class Blast(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.load_texture('Files/Blasts/Blast1/img0.png')
        self.center_x = x
        self.center_y = y + 20
        self.cnt = 0
        self.scale = 0.2
    def update(self, delta_t):
        self.cnt += 1
        self.scale = self.scale[0] + 0.03
        if self.cnt % 8 == 0:
            try:
                self.texture = arcade.load_texture(f'Files/Blasts/Blast1/img{self.cnt // 8}.png')
            except FileNotFoundError:
                self.remove_from_sprite_lists()