#!/usr/bin/kivy
'''
Basic Picture Viewer
====================

This simple image browser demonstrates the scatter widget. You should
see three framed photographs on a background. You can click and drag
the photos around, or multi-touch to drop a red dot to scale and rotate the
photos.

The photos are loaded from the local images directory, while the background
picture is from the data shipped with kivy in kivy/data/images/background.jpg.
The file pictures.kv describes the interface and the file shadow32.png is
the border to make the images look like framed photographs. Finally,
the file android.txt is used to package the application for use with the
Kivy Launcher Android application.

For Android devices, you can copy/paste this directory into
/sdcard/kivy/pictures on your Android device.

The images in the image directory are from the Internet Archive,
`https://archive.org/details/PublicDomainImages`, and are in the public
domain.

'''

import kivy
import math
kivy.require('1.0.6')

from glob import glob
from random import randint
from os.path import join, dirname
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
# FIXME this shouldn't be necessary
from kivy.core.window import Window

pics = []

class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y) and touch.grab_current == self:
            print('The touch is at position', touch.pos)
            np, dist = self.nearest_pic(pics)
            if dist < 100:
                self.x=(np.x+np.width*.65)*.2+self.x*.8
                self.y=np.y*.2+self.y*.8
        super(Picture, self).on_touch_move(touch)
    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y) and touch.grab_current == self:
            print('LIFT', touch.pos)
            print(self.x)
            np, dist = self.nearest_pic(pics)
            if dist < 100:
                self.x=np.x+np.width*.65
                self.y=np.y
        #print dir(self)
        super(Picture, self).on_touch_up(touch)
    def nearest_pic(self, pics):
        nearest = pics[0]
        shortest = 10000000
        for p in pics:
            if p != self:
                xd = self.x-p.x
                yd = self.y-p.y
                td = math.sqrt(xd*xd+yd*yd)
                if td < shortest:
                    shortest = td
                    nearest = p
        return nearest, shortest


class PicturesApp(App):

    def build(self):

        # the root is created in pictures.kv
        root = self.root

        # get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'images', '*.png')):
            try:
                # load the image
                picture = Picture(source=filename)#, rotation=randint(-30, 30))
                pics.append(picture)
                # add to the main field
                root.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True


if __name__ == '__main__':
    PicturesApp().run()

