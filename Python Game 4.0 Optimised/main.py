from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import numpy as np
import noise

app = Ursina()
player = FirstPersonController()

#variables
chunk = 8
chunk_count = 12
block = []
seed = 37847862262
player.speed = 10
player.gravity = 0.98

#rounding to the closest 8
def chunkround(x, base=8):  
    return base * round(x/base)

#load textures
grass_texture = load_texture('assets/blocks/2d_textures/grass_block.png')
sky_texture = load_texture('assets/blocks/2d_textures/skybox.png')

#sky
class Sky(Entity):
	def __init__(self):
		super().__init__(
			parent = scene,
			model = 'sphere',
			texture = sky_texture,
			scale = 100,
			double_sided = True)

#Idea: create terrain based on the game checing the 3 blocks next to it for entities in block positions, so it only genenerates the visible part of a block
class Voxel(Button):
	def __init__(self, position = (0,0,0), texture = grass_texture):
		super().__init__(
			parent = scene,
			position = position,
			model = 'assets/blocks/3d_textures/grass_block',
			origin_y = 0.5,
			texture = texture,
			color = color.color(0,0,random.uniform(0.9,1)),
			scale = 0.5
			)

class Terrain():
    perlin1 = PerlinNoise(octaves=3, seed=seed)
    perlin2 = PerlinNoise(octaves=0.05, seed=seed)
    for x in range(round(player.x) + (chunk * chunk_count)):
        for z in range(round(player.z) + (chunk * chunk_count)):
            y = perlin1([x/60, z/60]) + perlin2([x/12, z/12])
            y = round(y * 8)
            block = Voxel(position = (x, y, z))

def update():
    sky.position = player.position
    terrain = Terrain()

sky = Sky()
terrain = Terrain()
app.run()