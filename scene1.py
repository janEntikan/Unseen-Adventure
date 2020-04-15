from options import *


def scene1():
    bedroom = RolodexOption("bedroom")
    bedroom.center.reparent_to(render)

    bed = MenuOption("bed")
    bed.add(ReturnOption("look", "You just woke up from this bed."))
    bedroom.add(bed)

    door = MenuOption("door")
    door.add(ReturnOption("look", "A regular old door."))
    door.add(ReturnOption("open", "it's locked"))
    bedroom.add(door)

    closet = MenuOption("closet")
    closet.add(ReturnOption("look", "The oak closet holding your wardrobe."))
    closet.add(ReturnOption("open", "You can't open this door yet."))
    bedroom.add(closet)

    desk = MenuOption("desk")
    desk.add(ReturnOption("look", "Your computer's here."))
    bedroom.add(desk)

    start_room = bedroom

    return start_room