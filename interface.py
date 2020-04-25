import sys
from panda3d.core import TextNode, TextProperties, TextPropertiesManager

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
        self.money = self.inventory.add(Money(0, True))
        self.inventory.hide()
        self.say("press escape for menu")
        self.room, self.checkpoint, self.test = world()  
        self.room.node.reparent_to(render)
        base.play_music(self.room.song)
        self.current = self.room

        self.location = render2d.attach_new_node(TextNode("location text"))
        self.location.node().text = self.room.node.name
        self.location.node().align = 2
        self.location.node().font = base.font
        self.location.set_scale(0.025, 0.025, 0.045)
        self.location.set_z(0.1)

        self.hp = 10
        self.max_hp = 10
        self.stats = {
            "offence":0,
            "defence":0,
            "endurance":0,
        }
        self.equipment = {}
        self.creature_codex = []

        self.character = Inventory()
        self.character.hide()
        def get_health(): 
            base.interface.say("You have {}/{} hp.".format(self.hp, self.max_hp+self.stats["endurance"]))
        def get_stats(): 
            base.interface.say("Offence: {}.".format(self.stats["offence"]))
            base.interface.say("Defence: {}.".format(self.stats["defence"]))
            base.interface.say("Endurance: {}.".format(self.stats["endurance"]))

        manager = TextPropertiesManager.getGlobalPtr()
        tp = TextProperties()
        tp.setTextColor((0.2,0.2,0.2,1))
        manager.setProperties("grey", tp)
        tp = TextProperties()
        tp.setTextColor((1,1,1,1))
        manager.setProperties("white", tp)


        self.character.add(Option("inventory")).function=self.open_inventory
        self.character.add(Option("health")).function=get_health
        self.character.add(Option("stats")).function=get_stats
        quit = self.character.add(Menu("quit game"))
        quit.empty()
        quit.add(Return("yes, quit!", "")).function = sys.exit
        quit.add(Return("no, keep playing!", ""))
        self.dead = Rolodex("dead")
        self.dead.add(Option("You died."))

    def die(self):
        change_room(self.dead)
        base.play_music(None)
        base.sounds["youdie"].play()
        self.location.node().text = "dead"
        self.say("You die...")
        self.money.quantity = int(self.money.quantity/4)
        base.transition.setFadeColor(0.1,0,0)
        base.end_sequence()
        base.start_sequence(
            Func(base.transition.fadeOut, 2),
            Wait(3),
            Func(change_room, self.checkpoint),
            Func(base.transition.fadeIn, 2),
            Func(self.say, "...and wake up!"),
            Wait(1),
            Func(self.say, "...you lost most of your money!")
        )
        
    def say(self, output_string):
        self.to_output.append(output_string)
        while len(self.to_output) > 4:
            self.to_output = self.to_output[1:]
        output = ""
        for s, string in enumerate(self.to_output):
            if s == len(self.to_output)-1:
                output += "\1white\1> "
            else:
                output += "\1grey\1"
            output+=string+"\n"
        self.output.node().text = output

    def open_inventory(self):
        if not self.room == self.current:
            self.current.deactivate()
        base.sounds["back"].play()
        self.inventory.show()
        self.current = self.inventory


    def update(self):
        context = base.device_listener.read_context('ta')
        if context["inventory"] and not self.current == self.character:
            if self.current == self.inventory:
                base.sounds["back"].play()
                self.inventory.hide()
                self.current = self.room
            else:
                self.open_inventory()
        if (context["character"] or context["menu"]) and not self.current == self.inventory:
            if not self.current == self.character:
                base.sounds["back"].play()
                self.current = self.character
                self.character.show()
            else:
                base.sounds["back"].play()
                self.character.hide()
                self.current = self.room

        self.current.update(context)
