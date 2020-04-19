from options import *


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
