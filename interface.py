from panda3d.core import TextNode

from options import *
from world import world


class Interface():
    def __init__(self):
        self.output = render2d.attach_new_node(TextNode("output text"))
        self.output.node().text = ""
        self.output.node().align = 2
        self.output.node().font = base.font
        self.output.set_scale(0.025, 0.025, 0.045)
        self.output.set_z(-0.75)
        self.to_output = ["","","", ""]
        self.inventory = Inventory()
        self.money = self.inventory.add(Money(20000, True))
        self.inventory.hide()
        self.say("press i for inventory")
        self.say("press c to check yourself")
        self.room, self.checkpoint = world()  
        self.room.node.reparent_to(render)
        base.play_music(self.room.song)
        self.current = self.room

        self.location = render2d.attach_new_node(TextNode("location text"))
        self.location.node().text = self.room.node.name
        self.location.node().align = 2
        self.location.node().font = base.font
        self.location.set_scale(0.025, 0.025, 0.045)
        self.location.set_z(0.1)

        self.hp = 1
        self.status = "normal"
        self.level = 1
        self.xp = 0
        self.equipment = {}
        self.creature_codex = []

        self.character = Inventory()
        self.character.hide()
        def get_health(a,b): return base.interface.say("You have {} hp.".format(self.hp))
        def get_status(a,b): return base.interface.say("Your status is {}.".format(self.status))
        def get_level(a,b): return base.interface.say("Your level is {}.".format(self.level))
        def get_xp(a,b): return base.interface.say("You have {} xp.".format(self.xp))
        self.character.add(Option("health")).function=get_health
        self.character.add(Option("status")).function=get_status
        self.character.add(Option("level")).function=get_level
        self.character.add(Option("experience")).function=get_xp

    def die(self):
        self.say("You die...")
        self.money.quantity = int(self.money.quantity/4)
        base.transition.setFadeColor(0.1,0,0)
        base.end_sequence()
        base.start_sequence(
            Func(base.transition.fadeOut, 2),
            Wait(3),
            Func(change_room, self.checkpoint),
            Func(base.transition.fadeIn, 2),
            Func(self.say, "...and wake up!")
        )
        
    def say(self, output_string):
        self.to_output.append(output_string)
        while len(self.to_output) > 4:
            self.to_output = self.to_output[1:]
        output = ""
        for s, string in enumerate(self.to_output):
            if s == len(self.to_output)-1:
                output += "> "
            output+=string+"\n"
        self.output.node().text = output

    def update(self):
        context = base.device_listener.read_context('ta')
        if context["inventory"] and not self.current == self.character:
            if self.current == self.inventory:
                base.sounds["back"].play()
                self.inventory.hide()
                self.current = self.room
            else:
                if not self.room == self.current:
                    self.current.deactivate()
                base.sounds["back"].play()
                self.inventory.show()
                self.current = self.inventory
        if context["character"] and not self.current == self.inventory:
            if not self.current == self.character:
                base.sounds["back"].play()
                self.current = self.character
                self.character.show()
            else:
                base.sounds["back"].play()
                self.character.hide()
                self.current = self.room

        self.current.update(context)
