from options import *


def scene1():
    start_room = bedroom = RolodexOption("bedroom")
    closet = RolodexOption("closet")
    hallway = RolodexOption("hallway")
    # BEDROOM
    bedroom.node.reparent_to(render)
    bed = MenuOption("bed")
    bed.add(ReturnOption("look", "You just woke up from this bed."))
    bedroom.add(bed)
    bedroom_hallway_door = DoorOption(
        name="door", destination=hallway, 
        description="a plain white door"
    )
    bedroom.add(bedroom_hallway_door)
    bedroom_closet_door = DoorOption(
        name="closet", destination=closet, 
        description ="The oak closet holding your wardrobe."
    )
    bedroom.add(bedroom_closet_door)
    desk = MenuOption("desk")
    desk.add(ReturnOption("look", "Your computer's here."))
    bedroom.add(desk)

    # HALLWAY
    hallway.add(Option("statue", "It's a statue of an angel."))
    hallway.add(Option("staircase", "Stairs go downwards here."))
    hallway.add(Option("painting", "an ugly painting"))
    hallway.add(DoorOption(destination=bedroom, mimic=bedroom_hallway_door))

    # CLOSET
    closet.add(DoorOption(destination=bedroom, mimic=bedroom_closet_door))
    closet.add(Option("clothing", "all sort of clothing"))

    return start_room