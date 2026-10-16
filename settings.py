from pygame.math import Vector2 as vec

# Settings
WIDTH, HEIGHT = 400, 224
TILE_SIZE = 16
FONT = 'assets/imaki-oblique.ttf'

INPUTS = {"escape":False,
          "space":False,
          "up":False,
          "down":False,
          "left":False,
          "right":False,
          "left_click":False,
          "right_click":False,
          "scroll_up":False,
          "scroll_down":False}

COLOURS = {"black":(0,0,0),
           "white":(255,255,255),
           "red":(200,100,100),
           "green":(100,200,100),
           "blue":(100,100,200)}


LAYERS = ['background',
          'objects',
          'characters',
          "blocks",
          'particles',
          "foreground "]