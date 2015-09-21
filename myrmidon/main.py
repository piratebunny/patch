import sys
from myrmidon import Game, Entity
from myrmidon.consts import *
from pygame.locals import *


class App(Entity):
    hover_block = None
    grab_block = None
    
    def execute(self):
        self.images = {
            'blue_block' : Game.load_image("blue_block.png"),
            'red_block' : Game.load_image("red_block.png"),
            }
        self.blocks = [
            Block(self, 100, 100, 'red'),
            Block(self, 100, 300, 'blue')
            ]
        while True:
            if Game.keyboard_key_released(K_ESCAPE):
                sys.exit()
            yield

            
class Block(Entity):
    collision_on = True
    
    def execute(self, app, x, y, block_type):
        self.app = app
        self.x = x
        self.y = y
        self.block_type = block_type
        self.image = self.app.images[block_type + '_block']
        yield self.switch_state("state_normal")
        
    def state_normal(self):
        while True:
            self.alpha = 1.0
            if self.collide_with(Game.mouse()).result:
                if not self.app.hover_block:
                    self.app.hover_block = self
                    yield self.switch_state("state_hover")
            yield            

    def state_hover(self):
        while True:
            self.alpha = 0.9
            if not self.collide_with(Game.mouse()).result:
                self.app.hover_block = None
                yield self.switch_state("state_normal")
            if Game.mouse().left_down:
                self.app.grab_block = self
                yield self.switch_state("state_grabbed")
            yield

    def state_grabbed(self):
        while True:
            self.x = Game.mouse().x#rel[0]
            self.y = Game.mouse().y#rel[1]
            self.check_snapping()
            if Game.mouse().left_up:
                self.app.hover_block = None
                self.app.grab_block = None
                yield self.switch_state("state_normal")            
            yield

    def check_snapping(self):
        collide = self.collide_with(self.app.blocks)
        if collide.result:
            self.my_corners = self.collision_rectangle_calculate_corners()
            self.other_corners = collide.entity.collision_rectangle_calculate_corners()
            if abs(collide.entity.y - self.y) < 20 and \
               (self.my_corners['ul'][0] - self.other_corners['ur'][0]) < 30:
                self.snap_to(collide.entity)

    def snap_to(self, other):
        self.x = other.x + other.image.width - 20
        self.y = other.y

App()
