import os
import pygame, sys
from settings import *
from state import SplashScreen


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT),pygame.FULLSCREEN|pygame.SCALED)
        self.font = pygame.font.Font(FONT,TILE_SIZE)
        self.running = True
        self.fps = 60

        # List of states/screens. When game is initialised, we start with splash screen.
        self.states = []
        self.splash_screen = SplashScreen(self)
        self.states.append(self.splash_screen)

    def render_text(self,text:str,colour,font,pos, centralised=True):
        surf = font.render(str(text),False,colour)
        rect = surf.get_rect(center=pos) if centralised else surf.get_rect(topleft=pos)
        self.screen.blit(surf,rect)


    def custom_cursor(self,screen):
        pygame.mouse.set_visible(False)
        cursor_image = pygame.image.load('assets/cursor.png').convert_alpha()
        cursor_rect = cursor_image.get_frect(center=pygame.mouse.get_pos())
        cursor_image.set_alpha(150)
        self.screen.blit(cursor_image, cursor_rect.center)


    def get_images(self,path):
        images = []
        for file in os.listdir(path):
            full_path = os.path.join(path,file)
            img = pygame.image.load(full_path).convert_alpha()
            images.append(img)
        return images


    def get_animations(self,path):
        animations = {}

        for file_name in os.listdir(path):
            animations.update({file_name:[]})
        return animations


    def get_inputs(self):

        # So this is a loop that goes through all the events in the game and checks if some of them are triggered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            # Character movement!
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    INPUTS["escape"] = True
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    INPUTS["space"] = True
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    INPUTS["left"] = True
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    INPUTS["right"] = True
                elif event.key in (pygame.K_w, pygame.K_UP):
                    INPUTS["up"] = True
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    INPUTS["down"] = True

            if event.type == pygame.KEYUP:

                if event.key == pygame.K_SPACE:
                    INPUTS["space"] = False
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    INPUTS["left"] = False
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    INPUTS["right"] = False
                elif event.key in (pygame.K_w, pygame.K_UP):
                    INPUTS["up"] = False
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    INPUTS["down"] = False

            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1: # Scroll up
                    INPUTS["scroll_up"] = True
                elif event.y == -1: # Scroll down
                    INPUTS["scroll_down"] = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Mouse click
                    INPUTS["left_click"] = True
                elif event.button == 3:
                    INPUTS["right_click"] = True
                elif event.button == 4:
                    INPUTS["scroll_down"] = True
                elif event.button == 2:
                    INPUTS["scroll_up"] = True

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # Mouse click
                    INPUTS["left_click"] = False
                elif event.button == 3:
                    INPUTS["right_click"] = False
                elif event.button == 4:
                    INPUTS["scroll_down"] = False
                elif event.button == 2:
                    INPUTS["scroll_up"] = False


    def reset_inputs(self):
        for key in INPUTS:
            INPUTS[key] = False

    # Game loop
    def loop(self):
        while self.running:
            dt = self.clock.tick(self.fps)/1000
            self.get_inputs()
            self.states[-1].update(dt)
            self.states[-1].draw(self.screen)
            self.custom_cursor(self.screen)
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.loop()