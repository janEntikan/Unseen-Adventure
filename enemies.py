from random import randint
from battle import Mob


def _bunny():
    creature = Mob(
        "bomber bunny", 
        "you can hear sizzles and maniacal laughter...a bomber bunny!", 
        "it's completely mangled"
    )
    creature.hp = 3
    creature.ap = 2
    creature.xp = 25
    creature.cash = randint(2, 12)
    creature.attack = 2
    creature.sensitivity = "green"
    if randint(0,2)==1:
        return creature

def _crab():
    creature = Mob(
        "giant crab", 
        "it makes a click-clacking noise, almost like...a giant crab!", 
        "a pile of cans, claws and shells"
    )
    creature.hp = 5
    creature.ap = 2
    creature.xp = 15
    creature.cash = randint(2, 10)
    creature.attack = 2
    creature.sensitivity = "blue"
    if randint(0,1)==1:
        return creature

def _goat():
    creature = Mob(
        "demon goat", 
        "you can hear hoves on the rocks below, sounds almost like...a demon goat!", 
        "a human chest and the body of a goat, weird"
    )
    creature.hp = 5
    creature.ap = 1
    creature.xp = 25
    creature.cash = randint(10, 20)
    creature.attack = 5
    creature.sensitivity = None
    if randint(0,1)==1:
        return creature
    return creature

def _wizard():
    creature = Mob(
        "wizard", 
        "you can hear sparkles and magic...a wizard!", 
        "some dust and intestines under a robe"
    )
    creature.hp = 15
    creature.ap = 5
    creature.xp = 250
    creature.cash = randint(100, 200)
    creature.attack = 10
    creature.sensitivity = None
    return creature

def _unicorn():
    creature = Mob(
        "unicorn", 
        "you can hear hoves, sparkles and magic...a unicorn!", 
        "the blood is sticky and warm"
    )
    creature.hp = 50
    creature.ap = 50
    creature.xp = 1000
    creature.cash = randint(300, 500)
    creature.attack = 10
    creature.sensitivity = "green"
    if randint(0,5):
        return creature
