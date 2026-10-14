import pygame
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
        self.image = self.animations['idle'][self.frame_index].convert_alpha()
        self.rect = self.image.get_frect(topleft=pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width/2, -self.rect.height/2)
        self.speed = 60
        self.force = 2000
        self.acc = vec(0,0)
        self.vel = vec(0,0)
        self.fric = -15


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

    def update(self,dt):
        self.physics(dt)
        self.animate('idle', dt)


class Player(NPC):
    def __init__(self,game,scene,groups,pos, z, name):
        super().__init__(game,scene,groups,pos,z,name)

    def movement(self):
        if INPUTS["left"]:
            self.acc.x = -self.force
        elif INPUTS["right"]:
            self.acc.x = self.force
        else:
            self.acc.x = 0

        if INPUTS["up"]:
            self.acc.y = -self.force
        elif INPUTS["down"]:
            self.acc.y = self.force
        else:
            self.acc.y = 0

    def update(self,dt):
        self.physics(dt)
        self.movement()
        # Changing the animation depending on the velocity!
        if self.vel.magnitude() < 1:
            self.animate('idle', 5 * dt)
        else:
            self.animate('run', 5 * dt)
