from panda3d.core import TextNode
from panda3d.core import NodePath
from direct.interval.IntervalGlobal import Sequence, LerpFunctionInterval, Func


def in_margin(n, min, max):
    return n > min and n < max


def make_text(text_string, color=(1,1,1,1)):
    text = TextNode(text_string[:8])
    text.font = base.font
    text.text = str(text_string)
    text.text_color = color
    text.align = 2
    text_node = NodePath(text)
    return text_node


class Option():
    def __init__(self, name, description=None):
        self.mimic = None
        self.node = NodePath(name)
        self.description = description
        self.options = []
        self.parent = None
        self.function = None
        self.text = make_text(name)
        self.text.reparent_to(self.node)

    def update_mimic(self):
        pass

    def add(self, option):
        option.node.reparent_to(self.node)
        self.options.append(option)

    def hide(self):
        for option in self.options:
            option.node.hide()

    def show(self):
        for option in self.options:
            option.node.show()

    def empty(self):      
        for option in self.options:
            self.options.remove(option)

    def activate(self, activator):
        if self.description:
            base.interface.say(self.description)
        if self.function:
            self.function(self, activator)

    def update(self, context):
        pass


class MoveOption(Option):
    def __init__(self, name, destination=None, description=None):
        Option.__init__(self, name, description=description)
        self.destination = destination

    def activate(self, activator):
        if self.destination:
            if self.description:
                base.interface.say(self.description)
            Sequence(
                LerpFunctionInterval(base.camLens.set_fov, 0.2, fromData=base.camLens.get_fov()[0], toData=2, blendType='easeIn'),
                Func(self.swap),
                LerpFunctionInterval(base.camLens.set_fov, 0.2, fromData=base.camLens.get_fov()[0], toData=50, blendType='easeIn'),

            ).start()

    def swap(self):
        base.interface.room.node.detach_node()
        self.destination.get_closest_selection(base.interface.room.rotation)
        self.destination.update_mimic()

        base.interface.room = self.destination
        base.interface.current = base.interface.room
        base.interface.current.node.reparent_to(render)

           
class ReturnOption(Option):
    def __init__(self, name="return", description="You leave it."):
        Option.__init__(self, name, description=description)
    
    def activate(self, activator):
        base.interface.current = self.parent.parent
        if self.description:
            base.interface.say(self.description)
        if self.function:
            self.function()


class MenuOption(Option):
    def __init__(self, name):
        Option.__init__(self, name)
        self.selection = 0
        self.menu = self.node.attach_new_node("menu")
        self.time = 0
        self.add(ReturnOption("nevermind"))

    def add(self, option):
        self.options.append(option)
        option.text.set_scale(0.6)
        option.text.node().text_color = (0.2, 0.2, 0.2, 1)
        option.node.set_z(-len(self.options)/1.5)
        option.node.reparent_to(self.text)
        option.parent = self
        self.hide()
        return option

    def activate(self, activator):
        if len(self.options) > 0:
            base.interface.current = self
            self.show()
        elif self.description:
            base.interface.say(self.description)
        if self.function:
            self.function()

    def select(self):
        self.hide()
        self.options[self.selection].activate(self)     
        base.sounds["accept"].play()
        self.selection = 0

    def update(self, context):
        self.options[self.selection]
        self.time -= base.dt
        if context["select"]:
            self.select()   
        elif not context["ud"]:
            self.time = 0
        elif self.time <= 0:
            self.time = 0.2
            if context["ud"] > 0:
                self.selection += 1
                base.sounds["select"].play()
            elif context["ud"] < 0:
                self.selection -= 1
                base.sounds["select"].play()
            if self.selection < 0:
                self.selection = len(self.options)-1
            elif self.selection >= len(self.options):
                self.selection = 0      
        for o, option in enumerate(self.options):
            if o == self.selection:
                option.text.node().text_color = (1,1,1,1)
            else:
                option.text.node().text_color = (0.2,0.2,0.2,1)


class DoorOption(MenuOption):
    def __init__(self, destination, name="door", description="a boring old door", mimic=None):
        if mimic:
            name = mimic.name
            description = mimic.description
        MenuOption.__init__(self, "closed "+name)
        self.mimic = mimic
        self.name = name
        self.description = description
        self.add(ReturnOption("look", description))
        self.action = ReturnOption("open", "you take the handle...")
        self.action.function = self.open
        self.add(self.action)
        self.destination = destination
        self.doption = MoveOption("enter", self.destination)

    def update_mimic(self): # This makes the other side open too in a very shitty way
        if self.mimic:
            if self.mimic.function == self.mimic.open:
                if self.action.function == self.close:
                    self.close(True)
            else:
                if self.action.function == self.open:
                    self.open(True)

    def open(self, quietly=False):
        self.text.node().text = "open {}".format(self.name)
        self.action.text.node().text = "close {}".format(self.name)
        self.action.function = self.close
        self.add(self.doption)
        if not quietly:
            base.interface.say("...and open the {}.".format(self.name))

    def close(self, quietly=False):
        self.text.node().text = "closed {}".format(self.name)
        self.action.text.node().text = "open {}".format(self.name)
        self.action.function = self.open
        self.doption.node.detach_node()
        self.options.remove(self.doption)
        if not quietly:
            base.interface.say("...and close the {}.".format(self.name))


class RolodexOption(Option):
    def __init__(self, name):
        Option.__init__(self, name)
        self.partition = 0
        self.selection = 0
        self.speed = 0.05
        self.rotation = 0

    def update_mimic(self):
        for option in self.options:
            option.update_mimic()

    def add(self, option):
        option.parent = self
        self.options.append(option)
        option.node.reparent_to(self.node)
        self.partition = 360*(1/(len(self.options)))
        for o, option in enumerate(self.options):
            option.node.set_h(-(o*self.partition))
            option.text.set_y(50)

    def rotate(self, move):
        speed = self.partition*self.speed
        selection = self.selection*self.partition
        self.rotation%=360
        if in_margin(self.rotation, selection-1, selection+1):
            if move > 0:
                self.selection -= 1
                base.sounds["rotate"].play()
            elif move < 0:
                self.selection += 1
                base.sounds["rotate"].play()
            if self.selection >= len(self.options):
                self.selection = 0
            elif self.selection < 0:
                self.selection = len(self.options)-1
        elif self.rotation > selection:
            if abs(self.rotation-selection)<=180:
                self.rotation -= speed
            else:
                self.rotation += speed
        elif self.rotation < selection:
            if abs(self.rotation-selection)<=180:
                self.rotation += speed
            else:
                self.rotation -= speed
    
    def get_closest_selection(self, rotation):
        self.selection = int(rotation/self.partition)
        self.snap()

    def snap(self):
        if self.selection >= len(self.options):
            self.selection = 0
        elif self.selection < 0:
            self.selection = len(self.options)-1
        self.rotation = self.partition*self.selection
        self.node.set_h(self.rotation)

    def select(self):
        base.sounds["accept"].play()
        self.snap()
        self.options[self.selection].activate(self)

    def update(self, context):
        self.rotate(context["lr"])      
        self.node.set_h(self.rotation)
        if context["select"]:
            self.select()


class Inventory(RolodexOption):
    def __init__(self):
        RolodexOption.__init__(self, "inventory")
        self.node.set_z(12)
        self.node.reparent_to(render)

    def hide(self):
        self.node.hide()

    def show(self):
        self.node.show()
