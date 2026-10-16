import pygame
from character_states import Idle,Walk,Jump
from settings import *

# Base statistics class
class NPC(pygame.sprite.Sprite):
    def __init__(self,game,scene,groups,pos,z,name):
        super().__init__(groups)

        self.game = game
        self.scene = scene
        self.z = z
        self.name = name
        self.import_images(f'assets/characters/{self.name}/')
        self.frame_index = 0
        self.image = self.animations['idle_down'][self.frame_index].convert_alpha()
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)
        self.speed = 60
        self.force = 2000
        self.acc = vec()
        self.vel = vec()
        self.fric = -15
        self.move = {"left":False,"right":False,"up":False,"down":False,}
        self.state = Idle()
        self.controllable = False

    def import_images(self,path):
        self.animations = self.game.get_animations(path)

        for animation in self.animations.keys():
            full_path = path + animation
            frames = self.game.get_images(full_path)
            # Can be used to scale up or down the character...
            self.animations[animation] = [pygame.transform.scale(frame,(frame.get_width(),frame.get_height())) for frame in frames]


    def animate(self,state,fps,loop=True):
        self.frame_index += fps
        if self.frame_index >= len(self.animations[state])-1:
            if loop:
                self.frame_index = 0
            else:
                self.frame_index = len(self.animations[state])-1

        self.image = self.animations[state][int(self.frame_index)]


    def get_direction(self):
        angle = self.vel.angle_to(vec(0,1))
        angle = (angle + 360) % 360
        if 45 <= angle < 135: return "right"
        elif 135 <= angle < 225: return "up"
        elif 225 <= angle < 315: return "left"
        else: return "down"


    def movement(self):
        if self.move["left"]: self.acc.x = -self.force
        elif self.move["right"]: self.acc.x = self.force
        else:
            self.acc.x = 0

        if self.move["up"]: self.acc.y = -self.force
        elif self.move["down"]: self.acc.y = self.force
        else:
            self.acc.y = 0


    def get_collide_list(self,group):
        collidable_list = pygame.sprite.spritecollide(self,group, False)
        return collidable_list


    def collisions(self, axis, group):
        for sprite in self.get_collide_list(group):
            if self.hitbox.colliderect(sprite.hitbox):
                if axis == 'x':
                    if self.vel.x >= 0: self.hitbox.right = sprite.hitbox.left
                    if self.vel.x <= 0: self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                if axis == 'y':
                    if self.vel.y >= 0: self.hitbox.bottom = sprite.hitbox.top
                    if self.vel.y <= 0: self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery


    def physics(self,dt):
        # X-axis
        self.acc.x += self.vel.x * self.fric
        self.vel.x += self.acc.x * dt
        self.hitbox.centerx += self.vel.x * dt + (self.vel.x/2) * dt
        self.rect.centerx = self.hitbox.centerx
        self.collisions("x",self.scene.block_sprites)

        # Y-axis
        self.acc.y += self.vel.y * self.fric
        self.vel.y += self.acc.y * dt
        self.hitbox.centery += self.vel.y * dt + (self.vel.y/2) * dt
        self.rect.centery = self.hitbox.centery
        self.collisions("y", self.scene.block_sprites)

        # When we are moving diagonally
        if self.vel.magnitude() >= self.speed:
            self.vel = self.vel.normalize() * self.speed


    def change_state(self,dt):
        new_state = self.state.enter_state(self)
        if new_state: self.state = new_state
        else: self.state


    def update(self,dt):
        self.get_direction()
        self.change_state(dt)
        self.state.update(dt,self)


    def return_coordinates(self):
        return self.rect.centerx, self.rect.centery


class Player(NPC):
    def __init__(self,game,scene,groups,pos, z, name):
        super().__init__(game,scene,groups,pos,z,name)
        # Overwriting the controllable parameter, this class responds to the user inputs!
        self.controllable = True

    def movement(self):
        if INPUTS["left"]: self.acc.x = -self.force
        elif INPUTS["right"]: self.acc.x = self.force
        else: self.acc.x = 0

        if INPUTS["up"]: self.acc.y = -self.force
        elif INPUTS["down"]: self.acc.y = self.force
        else: self.acc.y = 0

    def vec_to_mouse(self,speed):
        # function returns the mouse pointer vector representation
        direction = vec(pygame.mouse.get_pos()) - (vec(self.rect.center) - vec(self.scene.camera.offset))
        if direction.length() > 0: direction.normalize_ip()
        return direction

