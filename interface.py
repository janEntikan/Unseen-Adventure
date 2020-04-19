from panda3d.core import TextNode

from options import *
from chapter1 import chapter1


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
        self.money = self.inventory.add(Money(10, True))
        self.inventory.hide()
        self.say("press i for inventory")
        self.room = chapter1()  
        self.current = self.room

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
        if context["inventory"]:
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

        self.current.update(context)
