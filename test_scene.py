from options import *
from battle import Mob


def scene1():
    start_room = bedroom = Rolodex("bedroom")
    closet = Rolodex("closet")
    hallway = Rolodex("hallway")
    livingroom = Rolodex("livingroom")

    # BEDROOM
    bedroom.node.reparent_to(render)
    bed = Menu("bed")
    bed.add(Return("look", "You just woke up from this bed."))
    bedroom.add(bed)
    bedroom_hallway_door = Door(
        name="door", destination=hallway, 
        description="a plain white door"
    )
    bedroom_hallway_door.locked = "It won't open. It's locked."
    bedroom.add(bedroom_hallway_door)

    bedroom_closet_door = bedroom.add(
        Door(
            name="closet", destination=closet, 
            description ="The oak closet holding your wardrobe."
        )
    )
    # DESK
    desk = Rolodex("desk")
    bedroom.add(Move("desk", desk, "You look closer at the desk."))
    desk.add(Option("computer", "It's old and crappy"))
    def unlock_bedroom_door(activated, activator):
        if bedroom_hallway_door.locked:
            bedroom_hallway_door.locked = None
            base.interface.say("You unlock the door with a satisfying click.")
        else:
            base.interface.say("It's already unlocked.")
    key = desk.add(Item("key"))
    key.add(Return("look", "It's an old and crappy key"))
    key.add(
        Use(
            "use", "That doesn't work.", 
            bedroom_hallway_door, unlock_bedroom_door
        )
    )
    desk.add(Move("nevermind", bedroom, "You stop looking at the desk.", keep_rotation=None))

    # HALLWAY
    hallway.add(Option("statue", "It's a statue of an angel."))
    staircase_down = hallway.add(Menu("staircase"))
    staircase_down.add(Return("look", "Stairs go downwards here."))
    staircase_down.add(Move("go down", livingroom, "You descend the stairs.", keep_rotation=False))
    hallway.add(Mob("zombie", "It's all sticky and oogy.", "a puddle of meat and bones."))
    hallway.add(Option("painting", "an ugly painting"))
    hallway.add(Door(destination=bedroom, mimic=bedroom_hallway_door))

    # LIVINGROOM
    livingroom.add(Option("front door", "The front door to the house."))
    livingroom.add(Option("television", "The tv. It's turned off."))
    livingroom.add(Option("sofa", "The sofa. You hate this thing."))
    staircase_up = livingroom.add(Menu("staircase"))
    staircase_up.add(Return("look", "Stairs go upwards here."))
    staircase_up.add(Move("go up", hallway, "You ascend the stairs.", keep_rotation=False))

    # CLOSET
    closet.add(Door(destination=bedroom, mimic=bedroom_closet_door))
    closet.add(Option("clothing", "all sort of clothing"))

    return start_room