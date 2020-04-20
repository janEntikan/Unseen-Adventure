from direct.interval.IntervalGlobal import Func, Wait, SoundInterval
from options import *


class Mob(Menu):
    def __init__(self, name, life_description, death_description):
        Menu.__init__(self, "?")
        self.name = name
        self.empty()
        self.freeze = True
        self.add(Stay("listen", life_description)).function = self.meet
        self.death_description = death_description
        self.defend = self.add(Return("defend", "you defend!", self.defend))
        self.attack = self.add(Return("attack", "you attack!", self.attack))
        self.text.node().text_color = (1,0,0,1)
        self.sensitivity = None
        self.hp = 1
        self.ap = 10
        self.attack = 4

    def meet(self):
        if not self.name in base.interface.creature_codex:
            base.interface.creature_codex.append(self.name)
        self.text.node().text = self.name

    def cam_shake(self, heft):
        base.start_sequence(
            LerpFunctionInterval(self.node.set_x, 0.05, fromData=self.node.get_x(self.node), toData=heft),
            LerpFunctionInterval(self.node.set_x, 0.05, fromData=self.node.get_x(self.node), toData=-heft),
            LerpFunctionInterval(self.node.set_x, 0.02, fromData=self.node.get_x(self.node), toData=heft),
            LerpFunctionInterval(self.node.set_x, 0.02, fromData=self.node.get_x(self.node), toData=-heft),
            Func(self.node.set_x, self.node, 0),
        )
    
    def die(self):
        base.interface.say("It dies.")
        self.meet()
        self.node.name = "dead " + self.name
        self.text.node().text = "dead " + self.name
        self.text.node().text_color = (0.5,0,0,1)
        self.freeze = False
        base.sounds["down"].play()
        base.interface.room.freeze = False
        base.play_music(None)
        self.empty();self.empty()
        self.selection = 0
        self.add(Return("nevermind", "you leave it"))
        self.add(Return("feel", self.death_description))

    def hurt(self, color):
        base.transition.setFadeColor(*color)
        base.transition.fadeOut(0)
        base.transition.fadeIn(0.04)
        base.sounds["hit1"].play()

    def turn(self):
        ap = 1
        for bodypart in base.interface.equipment:
            item = base.interface.equipment[bodypart]
            if item:
                ap += item.armor
                if item.element:
                    if item.element == self.sensitivity:
                        ap *= 1.5
        attack = int(self.attack/ap)
        base.interface.hp -= attack
        base.start_sequence(            
            Wait(1.0),
            Func(base.interface.say, "It attacks!"),
            Func(self.hurt, (1,0,0)),
            Func(base.interface.say, "It hits you for {} points.".format(attack)),
        )
        if base.interface.hp < 0:
            base.interface.die()
        self.player_is_defending = False

    def defend(self):
        self.player_is_defending = True
        self.turn()

    def attack(self):
        attack = 0
        for bodypart in base.interface.equipment:
            item = base.interface.equipment[bodypart]
            if item:
                attack += item.attack
                if item.element:
                    if item.element == self.sensitivity:
                        attack *= 1.5
        attack = int(attack/self.ap)+1
        self.hp -= attack
        base.interface.say("You do {} damage.".format(attack))        
        base.start_sequence(
            Func(self.hurt, (1,1,1)),
            Wait(0.25),
        )
        self.cam_shake(attack/10)
        if self.hp <= 0:
            self.die()
        else:
            self.turn()

    def init(self):
        if self.name in base.interface.creature_codex:
            self.text.node().text = self.name
        if self.hp > 0:
            base.transition.setFadeColor(1, 0, 0)
            base.transition.fadeOut(0)
            base.transition.fadeIn(0.1)
            base.play_music("battlesong")
            # TODO: If speed > playerspeed: fight first
            base.interface.say("Oh my goooood! It's a "+self.node.name)
    