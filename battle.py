from direct.interval.IntervalGlobal import Func, Wait, SoundInterval
from options import *


class Mob(Menu):
    def __init__(self, name, life_description, death_description):
        Menu.__init__(self, name)
        self.empty()
        self.freeze = True
        self.add(Stay("look", life_description))
        self.death_description = death_description
        self.attack = self.add(Return("attack", "you attack!", self.attack))
        self.defend = self.add(Return("defend", "you defend!", self.defend))
        self.text.node().text_color = (1,0,0,1)
        self.hp = 1
        self.ap = 10

    def cam_shake(self, heft):
        base.start_sequence(
            LerpFunctionInterval(self.node.set_x, 0.05, fromData=self.node.get_x(self.node), toData=heft),
            LerpFunctionInterval(self.node.set_x, 0.05, fromData=self.node.get_x(self.node), toData=-heft),
            LerpFunctionInterval(self.node.set_x, 0.02, fromData=self.node.get_x(self.node), toData=heft),
            LerpFunctionInterval(self.node.set_x, 0.02, fromData=self.node.get_x(self.node), toData=-heft),
            Func(self.node.set_x, self.node, 0),
        )
    
    def die(self):
        base.interface.say("It died.")
        self.node.name = "dead " + self.node.name
        self.text.node().text = self.node.name
        self.text.node().text_color = (0.5,0,0,1)
        self.freeze = False
        base.sounds["down"].play()
        base.interface.room.freeze = False
        base.play_music(None)
        self.empty();self.empty()
        print(self.options)
        self.selection = 0
        self.add(Return("nevermind", "you leave it"))
        self.add(Return("look", self.death_description))

    def hurt(self, color):
        base.transition.setFadeColor(*color)
        base.transition.fadeOut(0)
        base.transition.fadeIn(0.04)
        base.sounds["hit1"].play()

    def turn(self):
        self.cam_shake(0.2)
        base.start_sequence(            
            Wait(1.0),
            Func(base.interface.say, "It attacks!"),
            Func(self.hurt, (1,1,1))
        )

    def defend(self):
        pass

    def attack(self):
        self.hp -= 1
        base.start_sequence(
            Func(self.hurt, (1,0,0)),
            Wait(0.25),
        )
        if self.hp <= 0:
            self.die()
        else:
            self.turn()

    def init(self):
        if self.hp > 0:
            base.transition.setFadeColor(1, 0, 0)
            base.transition.fadeOut(0)
            base.transition.fadeIn(0.1)
            base.play_music("battlesong")
            # TODO: If speed > playerspeed: fight first
            base.interface.say("Oh my goooood! It's a "+self.node.name)
    