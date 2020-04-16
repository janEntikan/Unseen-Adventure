from options import *


def scene1():
    start_room = bedroom = Rolodex("bedroom")
    closet = Rolodex("closet")
    hallway = Rolodex("hallway")

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
    bedroom.add(Move("desk", desk))
    desk.add(Option("computer", "It's old and crappy"))
    key = desk.add(Item("key"))
    key.add(Return("look", "It's an old and crappy key"))
    def unlock_bedroom_door(activated, activator):
        bedroom_hallway_door.locked = None
        base.interface.say("You unlock the door with a satisfying click.")
    key_use = key.add(
        Use(
            "use", "That doesn't work.", 
            bedroom_hallway_door, unlock_bedroom_door
        )
    )
    desk.add(Move("nevermind", bedroom, keep_rotation=None))

    # HALLWAY
    hallway.add(Option("statue", "It's a statue of an angel."))
    hallway.add(Option("staircase", "Stairs go downwards here."))
    hallway.add(Option("painting", "an ugly painting"))
    hallway.add(Door(destination=bedroom, mimic=bedroom_hallway_door))

    # CLOSET
    closet.add(Door(destination=bedroom, mimic=bedroom_closet_door))
    closet.add(Option("clothing", "all sort of clothing"))

    return start_room