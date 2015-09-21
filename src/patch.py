import pi3d
import math

KEYBOARD = pi3d.Keyboard()
LOGGER = pi3d.Log.logger(__name__)

BACKGROUND_COLOR = (0.4, 0.8, 0.8, 1)

LEFT_BUTTON = 9
RIGHT_BUTTON = 10

winw, winh, bord = 1200, 600, 0     # 64MB GPU memory setting
DISPLAY = pi3d.Display.create(tk=True, window_title='Tiger Tank demo in Pi3D',
                              w=winw, h=winh - bord, far=3000.0,
                              background=BACKGROUND_COLOR, frames_per_second=16)
WIDTH, HEIGHT = DISPLAY.width, DISPLAY.height
ZPLANE = 1000
fov = 2.0 * math.degrees(math.atan(HEIGHT/2.0/ZPLANE))
win = DISPLAY.tkwin

CAMERA = pi3d.Camera(is_3d=False)
SHADER = pi3d.Shader('uv_flat')

TEXTURE_NAMES = ['../graphics/piratebunny2.png']
TEXTURES = [pi3d.Texture(t) for t in TEXTURE_NAMES]

# key presses
mymouse = pi3d.Mouse(restrict=False)
mymouse.start()
omx, omy = mymouse.position()


class Block(pi3d.ImageSprite):

    def __init__(self, camera=None, shader=None, texture=None,
                 x=10, y=0,
                 w=10.0, h=10.0, z=1000):
        super(Block, self).__init__(camera=camera, texture=texture,
                                    shader=shader, w=w, h=h, x=x, y=y, z=z)

    def is_under_mouse(self, mx, my):
        LOGGER.info("block centre %s %s", self.x(), self.y())
        return ((self.x() - self.width) < mx < (self.x() + self.width)) and \
            ((self.y() - self.height) < my < (self.y() + self.height))

block = Block(texture=TEXTURES[0], shader=SHADER, w=50, h=50, camera=CAMERA)
SPRITES = [block]
DISPLAY.add_sprites(*SPRITES)


def find_blocks_under_mouse(mx, my):
    return (s for s in SPRITES if s.is_under_mouse(mx, my))

while DISPLAY.loop_running():

    mx, my = mymouse.position()
    button_status = mymouse.button_status()

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
        if win.key == "Escape":
            try:
                print("bye,bye1")
                DISPLAY.destroy()
                try:
                    win.destroy()
                except:
                    pass
                mymouse.stop()
                exit()
            except:
                pass
        if win.key == 'w':
            block.translateY(10)
        elif win.key == 's':
            block.translateY(-10)
        elif win.key == 'a':
            block.translateX(-10)
        elif win.key == 'd':
            block.translateX(10)

    if button_status == LEFT_BUTTON:
        LOGGER.info("LEFT_BUTTON")
        LOGGER.info("thing %s %s", mx, my)
        for block in find_blocks_under_mouse(mx, my):
            block.translateX(10)
    if button_status == RIGHT_BUTTON:
        LOGGER.info("RIGHT_BUTTON")
        for block in find_blocks_under_mouse(mx, my):
            block.translateX(-10)
