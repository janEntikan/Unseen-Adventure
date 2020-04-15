import sys
import pman.shim

from direct.showbase.ShowBase import ShowBase
from panda3d.core import load_prc_file
from panda3d.core import Filename
from panda3d.core import WindowProperties
from panda3d.core import CardMaker

from keybindings.device_listener import add_device_listener
from keybindings.device_listener import SinglePlayerAssigner

from interface import Interface


load_prc_file(
    Filename.expand_from('$MAIN_DIR/settings.prc')
)


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        pman.shim.init(self)
        self.win.set_clear_color((0,0,0,1))
        self.accept('escape', sys.exit)
        add_device_listener(
            config_file='keybindings.toml',
            assigner=SinglePlayerAssigner(),
        )
        self.dt = globalClock.get_dt()
        self.font = loader.load_font("probe.ttf")
        self.load_sounds()
        self.interface = Interface()
        taskMgr.add(self.update)

    def load_sounds(self):
        self.sounds = {}
        sounds = (
            "accept", "back", "error", 
            "rotate", "select",
        )
        for sound in sounds:
            self.sounds[sound] = loader.load_sfx("sound/{}.wav".format(sound))

    def update(self, task):
        self.dt = globalClock.get_dt()
        self.interface.update()
        return task.cont


def main():
    app = GameApp()
    app.run()

if __name__ == '__main__':
    main()
