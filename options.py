from panda3d.core import TextNode
from panda3d.core import NodePath
from direct.interval.IntervalGlobal import LerpFunctionInterval, Func


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
        self.freeze = False
        self.mimic = None
        self.node = NodePath(name)
        self.description = description
        self.options = []
        self.parent = None
        self.function = None
        self.text = make_text(name)
        self.text.reparent_to(self.node)

    def init(self):
        pass

    def deactivate(self):
        base.interface.current = self.parent.parent

    def update_mimic(self):
        pass

    def add(self, option):
        option.node.reparent_to(self.node)
        self.options.append(option)
        return option

    def hide(self):
        for option in self.options:
            option.node.hide()

    def show(self):
        for option in self.options:
            option.node.show()

    def empty(self):
        for option in self.options:
            option.node.detach_node()
            self.options.remove(option)

    def activate(self, activator):
        if self.description:
            base.interface.say(self.description)
        if self.function:
            self.function(self, activator)

    def update(self, context):
        pass


class Stay(Option):
    def __init__(self, name="return", description="You leave it."):
        Option.__init__(self, name, description=description)
    
    def activate(self, activator):
        base.interface.current = self.parent
        if self.description:
            base.interface.say(self.description)
        if self.function:
            self.function()
        base.interface.current.show()

         
class Return(Option):
    def __init__(self, name="return", description="You leave it.", function=None):
        Option.__init__(self, name, description=description)
        self.function = function

    def activate(self, activator):
        self.deactivate()
        if self.description:
            base.interface.say(self.description)
        if self.function:
            self.function()


class Menu(Option):
    def __init__(self, name):
        Option.__init__(self, name)
        self.selection = 0
        self.menu = self.node.attach_new_node("menu")
        self.time = 0
        self.add(Return("nevermind"))

    def realign(self):
        self.options.reverse()
        for o, option in enumerate(self.options):
            option.text.set_scale(0.6)
            option.text.node().text_color = (0.2, 0.2, 0.2, 1)
            option.node.set_z(-(1+o))

    def add(self, option):
        self.options.reverse()
        self.options.append(option)
        option.node.reparent_to(self.text)
        option.parent = self
        self.hide()
        self.realign()
        return option

    def deactivate(self):
        self.hide()
        self.selection = 0

    def activate(self, activator):
        if len(self.options) > 0:
            base.interface.current = self
            self.show()
        elif self.description:
            base.interface.say(self.description)
        if self.function:
            self.function()

    def select(self):
        base.sounds["accept"].play()
        sel = self.selection
        self.deactivate()
        self.options[sel].activate(self)     

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


class Item(Menu):
    def __init__(self, name, taken=False):
        Menu.__init__(self, name)
        self.taken = taken        
        if not self.taken:
            self.take_option = self.add(Option("take"))
            self.take_option.function = self.take

    def add_to_inventory(self):
        base.interface.inventory.add(self)

    def take(self, activated, activator):
        base.interface.say("You take the " + self.node.name)
        base.interface.current = base.interface.room
        self.parent.remove(self)
        self.add_to_inventory()
        self.options.remove(self.take_option)
        self.take_option.node.detach_node()
        self.realign()


class Money(Item):
    def __init__(self, quantity, taken=False):
        Item.__init__(self, "gold", taken=taken)
        self.quantity = quantity
        self.add(Return("look", str(self.quantity)+" gold pieces"))

    def add_to_inventory(self):
        base.interface.money.quantity += self.quantity


class Move(Option):
    def __init__(self, name, destination=None, description=None, keep_rotation=True, mimic=None):
        Option.__init__(self, name, description=description)
        self.destination = destination
        self.keep_rotation = keep_rotation
        self.mimic = mimic
        if self.mimic:
            self.mimic.mimic = self
        # keep_rotation: 
        #	True = Keep the rotation from when you last exit this room
        # 	False = Face the same direction as previous room
        #	None = Rotate to first option

    def go(self):
        if self.destination:
            if self.description:
                base.interface.say(self.description)
            base.start_sequence(
                LerpFunctionInterval(base.camLens.set_fov, 0.2, fromData=base.camLens.get_fov()[0], toData=2, blendType='easeIn'),
                Func(self.swap),
                LerpFunctionInterval(base.camLens.set_fov, 0.2, fromData=base.camLens.get_fov()[0], toData=50, blendType='easeIn'),
            )

    def activate(self, activator):
        self.go()

    def rotate(self):
        if self.keep_rotation == None:
            self.parent.rotation = 0
            self.parent.selection = 0
        elif self.keep_rotation == False:
            if self.mimic:
                for o, option in enumerate(self.destination.options):
                    if option == self.mimic:
                        self.destination.selection = int(o+(len(self.destination.options)/2))
            elif self.parent.mimic:
                for o, option in enumerate(self.destination.options):
                    if option == self.parent.mimic:
                        self.destination.selection = int(o+(len(self.destination.options)/2))
            else:
                self.destination.get_closest_selection(base.interface.room.rotation)

    def swap(self):
        base.interface.room.node.detach_node()
        self.rotate()
        if self.destination.song:
            base.play_music(self.destination.song)
        self.destination.snap()
        self.destination.update_mimic()
        base.interface.room = self.destination
        base.interface.current = base.interface.room
        base.interface.current.node.reparent_to(render)


class Nevermind(Move):
    def __init__(self, destination, description):
        Move.__init__(self, "nevermind", destination, description, keep_rotation=None)


class Use(Return):
    def __init__(self, name, description="That doesn't work.", working_option=None, function=None):
        Return.__init__(self, name, description)
        self.working_option = working_option
        self.function = function
        self.single_use = False

    def activate(self, activator):
        if (self.working_option == None or 
                self.working_option == base.interface.room.get_current()):
            if self.function:
                self.function(self, activator)
                if self.single_use:
                    self.function = None
            else:
                base.interface.say(self.description)
        else:
            base.interface.say(self.description)
        self.deactivate()
        base.interface.inventory.deactivate()


class Door(Menu):
    def __init__(self, destination, name="door", description="a boring old door", mimic=None):
        if mimic:
            name = mimic.name
            description = mimic.description
        Menu.__init__(self, "closed "+name)
        self.mimic = mimic
        if self.mimic:
            self.mimic.mimic = self
        self.locked = None # Set this to "it's locked!" string to lock
        self.name = name
        self.description = description
        self.add(Return("look", description))
        self.action = Return("open", "you take the handle...")
        self.action.function = self.open
        self.add(self.action)
        self.destination = destination
        self.movement = Move("enter", self.destination, keep_rotation=False)

    def update_mimic(self): # This makes the other side open too in a very shitty way
        if self.mimic:
            if self.mimic.action.function == self.mimic.close:
                if self.action.function == self.open:
                    self.open(True)
            else:
                if self.action.function == self.close:
                    self.close(True)

    def open(self, quietly=False):
        if not self.locked:
            self.text.node().text = "open {}".format(self.name)
            self.action.text.node().text = "close {}".format(self.name)
            self.action.function = self.close
            self.add(self.movement)
            if not quietly:
                base.interface.say("...and open the {}.".format(self.name))
        else:
            base.interface.say(self.locked)

    def close(self, quietly=False):
        self.text.node().text = "closed {}".format(self.name)
        self.action.text.node().text = "open {}".format(self.name)
        self.action.function = self.open
        self.movement.node.detach_node()
        self.options.remove(self.movement)
        if not quietly:
            base.interface.say("...and close the {}.".format(self.name))


class Rolodex(Option):
    def __init__(self, name, song=None):
        Option.__init__(self, name)
        self.partition = 0
        self.selection = 0
        self.speed = 0.05
        self.rotation = 0
        self.rotating = False
        self.song = song
    
    def get_current(self):
        return self.options[self.selection]

    def update_mimic(self):
        for option in self.options:
            option.update_mimic()

    def remove(self, option):
        self.options.remove(option)
        option.node.detach_node()
        self.realign()
        self.selection = 0
        self.snap()

    def realign(self):
        self.partition = 360*(1/(len(self.options)))
        for o, option in enumerate(self.options):
            option.node.set_h(-(o*self.partition))
            option.text.set_y(50)

    def add(self, option):
        option.parent = self
        self.options.append(option)
        option.node.reparent_to(self.node)
        self.realign()
        return option

    def rotate(self, move):
        speed = self.partition*self.speed
        selection = self.selection*self.partition
        self.rotation%=360
        if in_margin(self.rotation, selection-5, selection+5):
            self.snap()
            if not self.freeze:
                if move > 0 :
                    self.selection -= 1
                    base.sounds["rotate"].play()
                elif move < 0:
                    self.selection += 1
                    base.sounds["rotate"].play()
                if self.selection >= len(self.options):
                    self.selection = 0
                elif self.selection < 0:
                    self.selection = len(self.options)-1
                if self.rotating:
                    current = self.get_current()
                    current.init()
                    self.rotating = False
                    if current.freeze:
                        self.freeze = True
        elif self.rotation > selection:
            self.rotating = True
            if abs(self.rotation-selection)<180:
                self.rotation -= speed
            else:
                self.rotation += speed
        elif self.rotation < selection:
            self.rotating = True
            if abs(self.rotation-selection)<180:
                self.rotation += speed
            else:
                self.rotation -= speed
    
    def get_closest_selection(self, rotation):
        self.selection = round(rotation/self.partition)-1

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


class Inventory(Rolodex):
    def __init__(self):
        Rolodex.__init__(self, "inventory")
        back = self.add(Return("exit inventory", ""))
        back.function = self.deactivate
        self.node.set_z(12)
        self.node.reparent_to(render)
        self.selection = 1

    def deactivate(self):
        base.interface.current = base.interface.room
        self.hide()

    def hide(self):
        self.node.hide()

    def show(self):
        self.node.show()


def make_path(a, b):
    m = a.add(Move("to "+b.node.name, b, keep_rotation=False))
    b.add(Move("to "+a.node.name, a, keep_rotation=False, mimic=m))


def make_open_door(a, b, name, description="a regular wooden door"):
    door = a.add(Door(name=name, destination=b, description=description))
    b.add(Door(destination=a, name=name, mimic=door))
    return door

def looker(location, name, description):
    location.add(Menu(name)).add(Return("look", description))