import sys
import pman.shim

from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions
from direct.interval.IntervalGlobal import Sequence, Func
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
        self.transition = Transitions(loader)
        self.font = loader.load_font("probe.ttf")
        self.load_sounds()
        self.interface = Interface()
        self.playing = None
        self.sequence = None
        self.sequence_end = Func(self.end_sequence)
        taskMgr.add(self.update)

    def load_sounds(self):
        self.sounds = {}
        self.music = {}
        sounds = (
            "accept", "back", "error", 
            "rotate", "select", "move",
            "hit0", "hit1", "hit2", "hit3",
            "down", "upup",
        )
        musics = (
            "home", "town", "shop", "tension",
            "forrest", "battlesong", "battlestart",
        )
        for sound in sounds:
            self.sounds[sound] = loader.load_sfx("sound/{}.wav".format(sound))
        for music in musics:
            self.music[music] = loader.load_sfx("music/{}.wav".format(music))

    def play_music(self, music=None):
        if not music == self.playing:
            for song in self.music:
                self.music[song].stop()
            if music:
                self.music[music].set_loop(True)
                self.music[music].play()
            self.playing = music

    def start_sequence(self, *kwargs):
        if not self.sequence:
            self.sequence = Sequence()
        while self.sequence_end in self.sequence:
            self.sequence.remove(self.sequence_end)
        for item in kwargs:
            self.sequence.append(item)
        self.sequence.append(self.sequence_end)
        self.sequence.start()

    def end_sequence(self):
        if self.sequence:
            self.sequence.finish()
            self.sequence = None

    def update(self, task):
        self.dt = globalClock.get_dt()
        if not self.sequence:
            self.interface.update()
        return task.cont


def main():
    app = GameApp()
    app.run()

if __name__ == '__main__':
    main()
