from random import randint
from panda3d.core import TextNode
from panda3d.core import NodePath
from direct.interval.IntervalGlobal import LerpFunctionInterval, Func, Wait


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


def change_room(destination):
    destination.init()
    base.interface.room.node.detach_node()
    if destination.song:
        base.play_music(destination.song)
    base.interface.location.node().text = destination.node.name
    destination.explored = True
    destination.snap()
    destination.update_mimic()
    for option in destination.options:
        option.is_known()
    base.interface.room = destination
    base.interface.current = base.interface.room
    base.interface.current.node.reparent_to(render)

    current = base.interface.current.get_current()
    current.init()
    if current.freeze:
        base.interface.current.freeze = True
    

class Option():
    def __init__(self, name, description=None):
        self.name = name
        self.freeze = False
        self.mimic = None
        self.node = NodePath(name)
        self.description = description
        self.options = []
        self.parent = None
        self.function = None
        self.text = make_text(name)
        self.text.reparent_to(self.node)
        self.function_once = False

    def init(self):
        pass

    def is_known(self):
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
            self.function()
            if self.function_once:
                self.function = None

    def realign(self):
        self.options.reverse()

    def remove(self, option):
        if option in self.options:
            self.options.remove(option)
            option.node.detach_node()
            self.options.reverse()
            self.realign()

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
            if self.function_once:
                self.function = None
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
            if self.function_once:
                self.function = None

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
            if self.function_once:
                self.function = None

    def select(self):
        base.sounds["accept"].play()
        sel = self.selection
        self.deactivate()
        self.options[sel].activate(self)     

    def update(self, context):
        self.options[self.selection]
        self.time -= base.dt
        ud = context["ud_a"]+context["ud_b"]
        if context["select_a"] or context["select_b"]:
            self.select()   
        elif not ud:
            self.time = 0
        elif self.time <= 0:
            self.time = 0.2
            if ud > 0:
                self.selection += 1
                base.sounds["select"].play()
            elif ud < 0:
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


class NPC(Menu):
    def __init__(self, name, lines=[]):
        Menu.__init__(self, name)
        self.name = name
        self.text.node().text_color = (1,0.2,0.5,1)
        self.line = 0
        self.lines = lines
        self.talk = self.add(Return("talk", "You begin a conversation."))
        self.talk.function = self.say

    def say(self):
        base.interface.say(self.name+": "+self.lines[self.line])
        self.line += 1
        if self.line >= len(self.lines):
            self.line = 0


class Item(Menu):
    def __init__(self, name, cost=0, taken=False):
        Menu.__init__(self, name)
        self.taken = taken
        self.cost = cost
        if cost > 0:
            self.price_option = self.add(Return("Ask for price", "It costs {} gold.".format(self.cost)))
            take_text = "buy"
        else:
           self.price_option = None
           take_text = "take"
        if not self.taken:
            self.take_option = self.add(Option(take_text))
            self.take_option.function = self.take

    def add_to_inventory(self):
        base.interface.inventory.add(self)

    def post_take(self):
        pass

    def take(self):
        if self.cost > 0:
            if base.interface.money.quantity >= self.cost:
                base.interface.say("You buy the " + self.node.name)
                self.options.remove(self.price_option)
                self.realign()
            else:
                base.sounds["error"].play()
                base.interface.say("You can't afford it.")
                self.deactivate()
                base.interface.current = base.interface.room
                return
        else:
            base.interface.say("You take the " + self.node.name)
        base.sounds["upup"].play()
        base.interface.current = base.interface.room
        self.parent.remove(self)
        self.add_to_inventory()
        self.options.remove(self.take_option)
        self.take_option.node.detach_node()
        self.realign()
        self.post_take()

class Money(Item):
    def __init__(self, quantity, taken=False):
        Item.__init__(self, "gold", taken=taken)
        self.quantity = quantity
        self.add(Return("count", "You count the gold.")).function=self.say_quantity

    def say_quantity(self):
        base.interface.say("There are "+str(self.quantity)+" gold pieces")

    def add_to_inventory(self):
        base.sounds["money"].play()
        base.interface.money.quantity += self.quantity


class Equipment(Item):
    def __init__(self, name, bodypart, cost, attack=0, defence=0):
        Item.__init__(self, name, cost, False)
        self.equipped = False
        self.equip_option = Option("equip")
        self.equip_option.function = self.equip
        self.bodypart = bodypart
        self.armor, self.attack = defence, attack
        self.element = None

    def post_take(self):
        self.add(self.equip_option)

    def equip(self, activator):
        if not self.bodypart in base.interface.equipment:
            base.interface.equipment[self.bodypart] = None
        if base.interface.equipment[self.bodypart]:
            base.interface.equipment[self.bodypart].text.node().text = self.name
        base.interface.equipment[self.bodypart] = self
        base.sounds["equip"].play()
        self.text.node().text = self.name+" (equipped)"
        base.interface.say("You equip the " + self.name)
        base.interface.inventory.deactivate()


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
        self.sound = "move"

    def is_known(self):
        if self.destination.explored:
            self.text.node().text = self.name
        else:
            self.text.node().text = "?"

    def go(self):
        if self.destination:
            base.sounds[self.sound].play()
            if self.description:
                base.interface.say(self.description)
            base.start_sequence(
                LerpFunctionInterval(base.camLens.set_fov, 0.2, fromData=base.camLens.get_fov()[0], toData=2, blendType='easeIn'),
                Func(self.swap),
                LerpFunctionInterval(base.camLens.set_fov, 0.2, fromData=base.camLens.get_fov()[0], toData=base.base_fov, blendType='easeInOut'),
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
        self.rotate()
        change_room(self.destination)


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
                self.function()
                if self.function_once:
                    self.function = None
                    base.interface.inventory.options.remove(self.parent)
                    self.parent.node.detach_node()
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
        self.name = name
        self.mimic = mimic
        if self.mimic:
            self.mimic.mimic = self
        self.locked = None # Set this to "it's locked!" string to lock
        self.description = description
        self.add(Return("feel", description))
        self.action = Return("open", "you take the handle...")
        self.action.function = self.open
        self.add(self.action)
        self.destination = destination
        self.movement = Move("enter", self.destination, keep_rotation=False)

    def update_mimic(self):
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
                base.sounds["door_open"].play()
                base.interface.say("...and open the {}.".format(self.name))
        else:
            base.sounds["error"].play()
            base.interface.say(self.locked)

    def close(self, quietly=False):
        self.text.node().text = "closed {}".format(self.name)
        self.action.text.node().text = "open {}".format(self.name)
        self.action.function = self.open
        self.movement.node.detach_node()
        self.options.remove(self.movement)
        if not quietly:
            base.sounds["door_close"].play()
            base.interface.say("...and close the {}.".format(self.name))


class Rolodex(Option):
    def __init__(self, name, song=None, explored=False, spawn=None):
        Option.__init__(self, name)
        self.partition = 0
        self.selection = 0
        self.speed = 0.05
        self.rotation = 0
        self.rotating = False
        self.song = song
        self.explored = explored
        self.spawn = spawn
        self.spawned = None

    def init(self):
        if self.spawn:
            if self.spawned:
                if self.spawned.dead:
                    self.remove(self.spawned)
                    self.spawned = None
            if not self.spawned:
                self.spawned = self.spawn()
                if self.spawned:
                    self.add(self.spawned, len(self.options))

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
            option.text.set_y(80)

    def add(self, option, index=None):
        option.parent = self
        if index:
            self.options.insert(index, option)
        else:
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
        self.rotate(context["lr_a"]+context["lr_b"])      
        self.node.set_h(self.rotation)
        if context["select_a"] or context["select_b"]:
            self.select()


class Inventory(Rolodex):
    def __init__(self):
        Rolodex.__init__(self, "inventory")
        back = self.add(Return("return", ""))
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


def amprand(min, max, rate=2):
    for i in range(max-min):
        min += 1
        if randint(0,int((max-min)/rate)) == 1:
            break
    return min

def find_money():
    amount = amprand(10,250, 4)
    base.sounds["money"].play()
    base.interface.money.quantity += amount
    base.interface.say("What's this!? There's {} gold here!".format(amount))

def verb(location, name, description, verb="feel", has_money=True):
    option = location.add(Menu(name))
    r = option.add(Return(verb, description))
    r.function_once = True
    if verb=="feel" and has_money:
        if randint(0,10) == 1:
            r.function = find_money
    
    return option
