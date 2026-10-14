import pygame
from camera import Camera
from pytmx.util_pygame import load_pygame
from characters import Player
from settings import *
from objects import Object, Wall


class State:

    def __init__(self,game):
        self.game = game
        self.prev_state = None

    def enter_state(self):
        if len(self.game.states) > 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)

    def exit_state(self):
        self.game.states.pop()

    # Will be overwritten by child classes
    def update(self,dt):
        pass

    def draw(self,screen):
        pass

# Different screens!
class SplashScreen(State):
    def __init__(self,game):
        State.__init__(self,game)

    # Also known as navigate to... new screen and other features
    def update(self,dt):
        if INPUTS["space"]:
            Scene(self.game).enter_state()
            self.game.reset_inputs()

    # Draw, also called - Screen Fill... + we can add some text!
    def draw(self,screen):
        screen.fill(COLOURS["blue"])
        self.game.render_text("Press ENTER to Start", COLOURS["white"],self.game.font,(WIDTH/2,HEIGHT/2),centralised=True)

class Scene(State):

    def __init__(self,game):
        State.__init__(self,game)
        self.camera = Camera(self)
        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()

        self.tmx_data = load_pygame("scenes/0/0.tmx")
        self.create_scene()


    def create_scene(self):
        layers = []
        for layer in self.tmx_data.layers:
            layers.append(layer.name)

        if "blocks" in layers:
            for x, y, surf in self.tmx_data.get_layer_by_name("blocks").tiles():
                Wall([self.block_sprites, self.drawn_sprites],(x*TILE_SIZE,y*TILE_SIZE),"blocks",surf)

        if "entries" in layers:
            for obj in self.tmx_data.get_layer_by_name("entries"):
                if obj.name == "0": # Creating a player instance - setting the entry point!
                    self.player = Player(self.game, self, [self.update_sprites, self.drawn_sprites],
                                         (obj.x,obj.y),"blocks", "player")


    def debugger(self,debug_list):
        for index, name in enumerate(debug_list):
            self.game.render_text(name,COLOURS["white"],self.game.font,(10,15 * index),False)

    def update(self, dt):
        self.update_sprites.update(dt)
        self.camera.update(dt,self.player)

    def draw(self, screen):
        self.camera.draw(screen,self.drawn_sprites)
        # Adding some debugging things
        self.debugger(
            [(round(self.game.clock.get_fps(),2)),
             (round(self.player.vel,2)) ])