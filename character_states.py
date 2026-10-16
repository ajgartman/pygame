from settings import *


class Idle:
    def enter_state(self,character):
        if character.vel.magnitude() > 1:
            return Walk()

        # User inputs! Only for Player class!
        if character.controllable:
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

        # This is only for the Player class!
        if character.controllable:
            if INPUTS["space"]:
                return Jump()

    def update(self, dt, character):
        character.animate(f"walk_{character.get_direction()}", 2 * dt)
        character.movement()
        character.physics(dt)


class Jump:
    def __init__(self):
        self.timer = 0.5
        INPUTS["space"] = False
        self.jump_pending = False

    def enter_state(self, character):
        if INPUTS["space"]:
            self.jump_pending = True

        if self.timer < 0:
            if self.jump_pending: return Jump()
            else: return Idle()

    def update(self, dt, character):
        self.timer -= dt
        character.animate("jump", 2 * dt,False)
        character.vel = vec()