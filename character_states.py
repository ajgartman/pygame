from settings import *


class Idle:
    def enter_state(self,character):
        if character.vel.magnitude() > 1:
            return Walk()

        if INPUTS["space"]:
            return Jump()

    def update(self,dt,character):
        character.animate(f"idle_{character.get_direction()}", 2*dt)
        character.movement()
        character.physics(dt)


class Walk:
    def enter_state(self, character):
        if character.vel.magnitude() < 1:
            return Idle()

        if INPUTS["space"]:
            return Jump()

    def update(self, dt, character):
        character.animate(f"walk_{character.get_direction()}", 2 * dt)
        character.movement()
        character.physics(dt)


class Jump:
    def __init__(self):
        self.timer = 0.25

    def enter_state(self, character):
        if self.timer < 0:
            return Idle()

    def update(self, dt, character):
        self.timer -= dt
        character.animate("jump", 2 * dt)
        character.vel = vec()