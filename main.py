from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from terrain import MeshTerrain
from random import random
from landscale import Map
from UrsinaLighting import LitDirectionalLight, LitPointLight, LitSpotLight, LitObject, LitInit
from ursina.shaders import lit_with_shadows_shader

app = Ursina()
lit = LitInit()

subject = FirstPersonController()
subject.gravity = 0.0
subject.x = 15
subject.z = 15

pX = subject.x
pZ = subject.z

scene.fog_density = (0, 95)
scene.fog_color = color.gray

Audio('assets/C418_Subwoofer_Lullaby.mp3', True)
grass_audio = Audio('assets/step.ogg',autoplay=False,loop=False)
water_swim = Audio('assets/water-swim.mp3',autoplay=False,loop=False)

arm_texture = load_texture('assets/arm_texture.png')
skyboxTexture = Texture("textures/skybox.jpg")

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3(150,-10,0),
            position = Vec2(0.4,-0.6),
            shader = lit_with_shadows_shader
        )

    def active(self):
        self.position = Vec2(0.3,-0.5)

    def passive(self):
        self.position = Vec2(0.4,-0.6)

hand = Hand()

map = Map(1371)
terrain = MeshTerrain(map.landscale_mask)

skybox = Sky(model = "sphere", double_sided = True, texture = skyboxTexture, rotation = (0, 90, 0))
water = LitObject(position = (floor(terrain.subWidth/2), -0.1, floor(terrain.subWidth/2)), scale = terrain.subWidth,
                  water = True, cubemapIntensity = 0.75, collider='box', texture_scale=(terrain.subWidth, terrain.subWidth),
                  ambientStrength = 0.5)

def input(key):
    terrain.input(key)

count = 0
def update():
    global count, pX, pZ

    count+=1
    if count == 4:

        count=0
        terrain.update(subject.position,camera)

    # Change subset position based on subject position.
    if abs(subject.x-pX) > 1 or abs(subject.z-pZ) > 1:
        pX=subject.x
        pZ=subject.z

        if subject.y >= 0 and grass_audio.playing == False:
            grass_audio.pitch=random()+0.7
            grass_audio.play()
        elif subject.y < 0 and water_swim.playing == False:
            water_swim.pitch = random() + 0.3
            water_swim.play()

    blockFound=False
    height = 1.76

    x = floor(subject.x+0.5)
    z = floor(subject.z+0.5)
    y = floor(subject.y+0.5)
    for step in range(-2,2):
        if terrain.td.get((x,y+step,z))=="t":
            # ***
            # Now make sure there isn't a block on top...
            if terrain.td.get((x,y+step+1,z))!="t":
                target = y+step+height
                blockFound = True
                break
            else: 
                target = y+step+height+1
                blockFound = True
                break
    if blockFound==True:
        # Step up or down :>
        subject.y = lerp(subject.y, target, 6 * time.dt)
    else:
        subject.y -= 9.8 * time.dt

terrain.genTerrain()

app.run()