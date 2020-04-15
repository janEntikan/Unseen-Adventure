from panda3d.core import TextNode
from panda3d.core import NodePath


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
        self.node = NodePath(name)
        self.description = description
        self.options = []
        self.parent = None
        self.text = make_text(name)
        self.text.reparent_to(self.node)

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

    def activate(self):
        if self.description:
            base.interface.say(self.description)

    def update(self, context):
        pass


class ReturnOption(Option):
    def __init__(self, name="return", description="You leave it."):
        Option.__init__(self, name, description=description)
    
    def activate(self):
        base.interface.current = self.parent.parent
        if self.description:
            base.interface.say(self.description)


class MenuOption(Option):
    def __init__(self, name):
        Option.__init__(self, name)
        self.selection = 0
        self.menu = self.node.attach_new_node("menu")
        self.time = 0
        self.add(ReturnOption("nevermind"))

    def add(self, option):
        self.options.append(option)
        option.text.set_scale(0.4)
        option.text.node().text_color = (0.2, 0.2, 0.2, 1)
        option.node.set_z(-len(self.options)/1.5)
        option.node.reparent_to(self.text)
        option.parent = self
        self.hide()
        return option

    def activate(self):
        if len(self.options) > 0:
            base.interface.current = self
            self.show()
        elif self.description:
            base.interface.say(self.description)

    def select(self):
        self.hide()
        self.options[self.selection].activate()     
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


class RolodexOption(Option):
    def __init__(self, name):
        Option.__init__(self, name)
        self.center = NodePath(name+"_center")
        self.partition = 0
        self.focus = 0
        self.speed = 0.05
        self.rotation = 0

    def add(self, option):
        option.parent = self
        self.options.append(option)
        self.partition = 360*(1/(len(self.options)))
        for o, option in enumerate(self.options):
            option.node.reparent_to(self.center)
            option.node.set_h(-(o*self.partition))
            option.text.set_y(50)

    def rotate(self, move):
        speed = self.partition*self.speed
        focus = self.focus*self.partition
        self.rotation%=360
        if in_margin(self.rotation, focus-1, focus+1):
            if move > 0:
                self.focus -= 1
                base.sounds["rotate"].play()
            elif move < 0:
                self.focus += 1
                base.sounds["rotate"].play()
            if self.focus >= len(self.options):
                self.focus = 0
            elif self.focus < 0:
                self.focus = len(self.options)-1
        elif self.rotation > focus:
            if abs(self.rotation-focus)<=180:
                self.rotation -= speed
            else:
                self.rotation += speed
        elif self.rotation < focus:
            if abs(self.rotation-focus)<=180:
                self.rotation += speed
            else:
                self.rotation -= speed

    def select(self):
        base.sounds["accept"].play()
        self.rotation = self.partition*self.focus
        self.center.set_h(self.rotation)
        self.options[self.focus].activate()

    def update(self, context):
        self.rotate(context["lr"])      
        self.center.set_h(self.rotation)
        if context["select"]:
            self.select()
