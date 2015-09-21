import pi3d
import math
import random

KEYBOARD = pi3d.Keyboard()
LOGGER = pi3d.Log.logger(__name__)

BACKGROUND_COLOR = (1.0, 1.0, 1.0, 0.0)

#DISPLAY = pi3d.Display.create(tk=True, background=BACKGROUND_COLOR)
#winw, winh, bord = 1200, 600, 0     #64MB GPU memory setting
DISPLAY = pi3d.Display.create(tk=True, window_title='Tiger Tank demo in Pi3D',
                              #                              w=winw, h=winh - bord, far=3000.0,
                              background=(0.4, 0.8, 0.8, 1), frames_per_second=16)
WIDTH, HEIGHT = DISPLAY.width, DISPLAY.height
ZPLANE = 1000
fov = 2.0 * math.degrees(math.atan(HEIGHT/2.0/ZPLANE))
win = DISPLAY.tkwin

CAMERA = pi3d.Camera((0, 0, 0), (0, 0, -1.0),
                     (1, 1100, fov,
                      WIDTH / float(HEIGHT)))
SHADER = pi3d.Shader('uv_flat')

TEXTURE_NAMES = ['../graphics/piratebunny.png']
TEXTURES = [pi3d.Texture(t) for t in TEXTURE_NAMES]

#key presses
mymouse = pi3d.Mouse(restrict = False)
mymouse.start()
omx, omy = mymouse.position()


class Block(pi3d.ImageSprite):

    def __init__(self, camera=None, shader=None, texture=None,
                 x=10, y=0,
                 w=10.0, h=10.0, z=1000):
        super(Block, self).__init__(camera=camera, texture=texture, shader=shader, w=w, h=h, x=x, y=y, z=z)

block = Block(texture=TEXTURES[0], shader=SHADER, w=50, h=50, camera=CAMERA)
SPRITES = [block]
DISPLAY.add_sprites(*SPRITES)

while DISPLAY.loop_running():
    if KEYBOARD.read() == 27:
        DISPLAY.stop()

    mx, my = mymouse.position()
    button_status =mymouse.button_status()
    print(mx)
    print(my)
    print(button_status)
    print('\n')

    try:
        win.update()
    except Exception as e:
        print("bye,bye2", e)
        DISPLAY.destroy()
        try:
            win.destroy()
        except:
            pass
        mymouse.stop()
        exit()

    if win.ev == "key":
        print(win.key)

    if win.ev == "click" or win.ev == "drag":
        print("Click")
        block.x = 30
        #block.repaint()
    else:
        win.ev=""  #clear the event so it doesn't repeat
