from random import randint, choice
from direct.interval.IntervalGlobal import Func, Wait, SoundInterval
from options import *


class Mob(Menu):
    def __init__(self, name, life_description, death_description):
        Menu.__init__(self, "?")
        self.name = name
        self.empty()
        self.freeze = True
        self.listen = self.add(Stay("listen", life_description))
        self.listen.function = self.meet
        self.death_description = death_description
        self.run = self.add(Return("run", "you try to run away!", self.run))
        self.defend = self.add(Return("defend", "you defend!", self.defend))
        self.attack = self.add(Return("attack", "you attack!", self.attack))
        self.text.node().text_color = (1,0,0,1)
        self.sensitivity = None
        self.hp = 1
        self.ap = 1
        self.cash = randint(0,10)
        self.attack = 1
        self.dead = False

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
        self.options.remove(self.listen)
        self.listen.node.detach_node()
        base.interface.say("It dies.")
        self.meet()
        self.dead = True
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
        self.cash += self.xp
        s = "You find {} gold".format(self.cash)
        base.interface.say(s)
        base.interface.money.quantity += self.cash

    def hurt(self, color):
        base.transition.setFadeColor(*color)
        base.transition.fadeOut(0)
        base.transition.fadeIn(0.04)

    def turn(self):
        ap = 1
        for bodypart in base.interface.equipment:
            item = base.interface.equipment[bodypart]
            if item:
                ap += item.armor
                if item.element:
                    if item.element == self.sensitivity:
                        ap *= 1.5
        attack = int(self.attack-ap)
        attack -= base.interface.stats["defence"]
        if attack < 1: attack = 1
        base.interface.hp -= attack
        base.start_sequence(            
            Wait(1.0),
            Func(base.interface.say, "It attacks!"),
            Func(self.hurt, (1,0,0)),
            Func(base.interface.say, "It hits you for {} points.".format(attack)),
            Func(base.sounds["hit0"].play),
            Func(self.kill_player),
        )
        self.player_is_defending = False

    def kill_player(self):
        maxhp = base.interface.max_hp + base.interface.stats["endurance"]
        if base.interface.hp < 0:
            base.interface.die()
        elif base.interface.hp < maxhp/5:
            base.interface.say("You're almost dying.")
        elif base.interface.hp < maxhp/4:
            base.interface.say("You're bleeding profusely.")
        elif base.interface.hp < maxhp/3:
            base.interface.say("You're in a lot of pain.")
        elif base.interface.hp < maxhp/2:
            base.interface.say("You're in some pain.")

    def run(self):
        if randint(0, 1) == 0:
            base.interface.say("You run away")
            self.parent.freeze = False
            self.parent.rotate(choice((-1,1)))            
        else:
            base.interface.say("...but you couldn't!")
            self.turn()

    def defend(self):
        self.player_is_defending = True
        self.turn()

    def attack(self):
        attack = 0
        for bodypart in base.interface.equipment:
            item = base.interface.equipment[bodypart]
            if item:
                attack += item.attack
                print(bodypart, item.attack)
                if item.element:
                    if item.element == self.sensitivity:
                        attack *= 1.5
        attack += base.interface.stats["offence"]
        attack = int(attack-self.ap)
        if attack < 1: attack = 1
        self.hp -= attack
        base.sounds["hit{}".format(randint(1,3))].play()
        base.interface.say("You do {} damage.".format(attack))        
        base.start_sequence(
            Func(self.hurt, (1,1,1)),
            Wait(0.25),
        )
        self.cam_shake(attack/10)
        if self.hp < 1:
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