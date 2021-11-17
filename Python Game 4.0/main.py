from perlin_noise.perlin_noise import PerlinNoise
from ursina import *
from random import *
from ursina import collider
from ursina.prefabs.first_person_controller import *
from ursina.prefabs.health_bar import *
from ursina.input_handler import *
from perlin_noise import *
import threading
from numba import jit
import asyncio
import time

app = Ursina()
#rounding to the closest 8
def chunkround(x, base=8):  
    return base * round(x/base)

#variables
seed = randint(10000000, 19999999)
chunk = 8
chunk_count = 20
block_width = chunk * chunk_count
water_level = 0
blocks = dict()

#texture loading
blocks = [
            load_texture('grass_block.png'),
        ]

#voxel
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), scale=1):
        super().__init__(
            parent = scene,
            position = position,
            collider = 'box',
            model = 'cube',
            scale = scale,
            color = color.color(0,0,random.uniform(0.9,1)),
            double_sided = False,
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                self.color = color.red
                destroy(self)
            if key == 'right mouse down':
                block = Voxel(position=self.position + mouse.normal)
        

#terrain
def terrain():
    perlin1 = PerlinNoise(octaves=0.6, seed=seed)
    perlin2 = PerlinNoise(octaves=0.05, seed=seed)
    for x in range(chunk * chunk_count):
        for z in range(chunk * chunk_count):
            y = perlin1([x/8, z/8]) + perlin2([x/8, z/8])
            y = round(y * 10)
            block = Voxel(position = (x, y, z))
            print(f'Created Block at X: {x} Y: {y} Z: {z}')

if __name__ == '__main__':
    x = threading.Thread(target=terrain)
    x.start()
    x.join()

EditorCamera()
app.run()