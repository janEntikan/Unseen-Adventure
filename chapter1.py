from options import *
from battle import Mob
from npc import NPC

def chapter1():
    start_room = bedroom = Rolodex("bedroom", "home")
    closet = Rolodex("closet")
    hallway = Rolodex("hallway")
    livingroom = Rolodex("livingroom", "home")
    garden = Rolodex("your home", "home")
    road = Rolodex("town road", "town")
    neighbour = Rolodex("miss tover's house")
    tover_house = Rolodex("tove house")
    inn = Rolodex("inn")
    alley = Rolodex("dark alley")
    well = Rolodex("town well")
    town_center = Rolodex("town center", "town")
    bakery = Rolodex("bakery", "shop")
    magicshop = Rolodex("magicshop", "shop")
    armory = Rolodex("armory", "shop")
    training = Rolodex("training", "shop")
    castle_gate = Rolodex("castle gate", "town")
    bank = Rolodex("bank", "shop")
    castle = Rolodex("castle")
    town_bridge = Rolodex("town bridge", "forrest")
    crossroads = Rolodex("crossroads")
    long_road = Rolodex("long road")
    dunes = Rolodex("dunes")
    sea = Rolodex("sea")
    harbor = Rolodex("the harbor")
    forrest_path = Rolodex("forrest path")
    bench = Rolodex("streetbench")
    river = Rolodex("river")
    forrest = Rolodex("forrest")
    lake = Rolodex("the lake")
    clearing = Rolodex("clearing")
    waterfall = Rolodex("waterfall")
    cave = Rolodex("cave")
    bonfire = Rolodex("bonfire")
    tower = Rolodex("wizard tower")
    forrest_cabin = Rolodex("cabin")
    deep_forrest = Rolodex("deep forrest")
    strange_rock = Rolodex("strange rock")
    candy_house = Rolodex("candy house")
    ufo = Rolodex("crashlanded ufo")
    mountain_path = Rolodex("mountain path")
    canyon = Rolodex("canyon")
    canyon_path = Rolodex("canyon path")
    mountain_cabin = Rolodex("cabin")
    mines = Rolodex("the mines")
    #BEDROOM
    
    bedroom.node.reparent_to(render)
    looker(bedroom, "bed", "It is not very soft.")
    bedroom_livingroom_door = bedroom.add(Door(
        name="door", destination=livingroom, 
        description="a damaged wooden door"))
    bedroom_closet_door = bedroom.add(Door(
        name="closet", destination=closet, 
        description ="The dark oak closet holding your wardrobe."))
    # CLOSET
    closet.add(Door(destination=bedroom, mimic=bedroom_closet_door))
    closet.add(Item("plain clothes", "very boring looking clothes"))
    # DESK
    desk = Rolodex("writing desk")
    bedroom.add(Move("writing desk", desk, "you inspect the writing desk."))
    desk.add(Option("writing feather", "There's no ink."))
    desk.add(Nevermind(bedroom, "You stop looking at the writing desk."))
    # WALL HOOKS
    hooks = Rolodex("wall hooks")
    bedroom.add(Move("wall hooks", hooks, "you inspect the wall hooks."))
    hat = hooks.add(Item("hat"))
    hat.add(Return("look", "a brown stitson hat."))
    looker(hooks, "stain", "there's a brown stain on the wall")
    hooks.add(Nevermind(bedroom, "You stop looking at the wall hooks."))
    # LIVINGROOM
    looker(livingroom, "window", "it's a beautiful day outside")
    front_door = livingroom.add(Door(garden, "front door"))
    front_door.locked = "It won't open. It's locked."
    looker(livingroom, "wall", 
        "covered in greasy, brown flower patterned wallpaper")
    # front door and it's key
    def unlock_front_door(activated, activator):
        if front_door.locked:
            front_door.locked = None
            base.interface.say("You unlock the door with a satisfying click.")
        else:
            base.interface.say("It's already unlocked.")
    key = hooks.add(Item("key"))
    key.add(Return("look", "It's a bit rusty."))
    key.add(Use(
        "use", "That doesn't work.", 
        front_door, unlock_front_door))
    livingroom_chair = livingroom.add(Menu("chair"))
    livingroom_chair.add(Return("look", "your trusty chair"))
    livingroom_chair.add(Return("sit", "You sit down for a few, and stand up again."))
    livingroom.add(Door(destination=bedroom, name="door", mimic=bedroom_livingroom_door))
    livingroom_bookcase = livingroom.add(Menu("bookcase"))
    livingroom_bookcase.add(Return("look", "All the books you've ever read."))
    livingroom_bookcase.add(Return("read", "you've read all of these already."))
    # GARDEN
    looker(garden, "flowerbed", "vibrant and colorful flowers")
    garden.add(Door(destination=livingroom, name="front door", mimic=front_door))
    looker(garden, "shrub", "a deep green shrubbery")
    make_path(road, garden)
    make_path(town_bridge, road)   
    make_path(road, neighbour)
    # MISS TOVER
    looker(neighbour, "flowers", "Miss Tover likes flowers almost as much as you do")
    make_open_door(neighbour, tover_house, "front door")
    looker(neighbour, "small tree", "A regular old pine tree.")
    tover_house.add(NPC("miss tover", [
        "Hello young man. Can I get you anything?",
        "I haven't left the city in over 30 years.",
        "How are things outside of the city?",
        "My son David works in the mines.",
    ]))
    # TOWN CENTER
    make_open_door(town_center, bakery, "bakery door")
    bakery.add(NPC("baker", [
        "Good day, friend. What will it be?",
        "Take a look around!",
        "I start baking at 4AM.",
        "Don't you just love the smell of bread?",
    ]))
    make_path(town_center, road)
    make_open_door(town_center, armory, "armory door")
    bakery.add(NPC("smith", [
        "What will it be, huh?",
        "Finest steel in the land!",
        "Bending steel is hard work.",
        "We have a special offer on wooden swords today.",
    ]))
    make_path(town_center, well)
    make_path(town_center, alley)
    make_open_door(town_center, inn, "inn door")
    inn.add(NPC("innkeeper", [
        "Come in! Have a seat!",
        "What can I get you?",
        "A room is 25 gold a night.",
        "This mead comes all the way from Albaden.",
    ]))
    make_open_door(town_center, magicshop, "magicshop door")
    magicshop.add(NPC("magician", [
        "Spells and curses for sale.",
        "Careful, that's very unstable!",
        "I can tell you have a good eye for magic.",
        "Magic, ladies and gentlemen.",
    ]))
    make_open_door(town_center, training, "trainer door")
    training.add(NPC("trainer", [
        "Need some training?",
        "That's the ticket!",
        "Feel the burn.",
        "Are you pumped for the day?",
    ]))
    # CASTLE
    make_open_door(castle_gate, bank, "banker door") 
    bank.add(NPC("banker", [
        "Need someone to hold on to that?",
        "Interest makes the world go round.",
        "Sorry, we're all out of loans.",
        "Life insurance perhaps?",
    ]))
    make_path(castle_gate, town_center)
    make_open_door(castle_gate, castle, "castle door") 
    castle.add(NPC("guard", [
        "You can't just walk into the castle like that.",
        "The king is too busy to see the likes of you.",
        "What makes you think you can just barge in here?",
    ]))
    # BRIDGE
    looker(town_bridge, "river", "the river flows under the bridge")
    make_path(town_bridge, crossroads)
    looker(town_bridge, "river", "the river flows under the bridge")
    # CROSSROADS
    make_path(crossroads, forrest_path)
    make_path(crossroads, long_road)
    make_path(crossroads, mountain_path)
    make_path(long_road, forrest_cabin)
    make_path(long_road, dunes)
    make_path(long_road, canyon)
    # SEA
    looker(dunes, "seashell", "a colorfull seashell lies on the floor")
    make_path(dunes, sea)
    make_path(dunes, harbor)
    # MOUNTAINS
    make_path(mountain_path, canyon)
    make_path(mountain_path, canyon_path)
    make_path(canyon_path, mines)
    make_path(canyon_path, mountain_cabin)
    # FORREST
    looker(forrest_path, "big tree", 
        "a majestic tree points to the sky")
    make_path(forrest_path, bench)
    make_path(forrest_path, lake)
    make_path(forrest_path, forrest_cabin)
    make_path(lake, river)
    make_path(lake, forrest)
    make_path(lake, tower)
    make_path(forrest, deep_forrest)
    make_path(forrest, candy_house)
    make_path(forrest, waterfall) 
    make_path(bench, river)
    make_path(river, deep_forrest)
    make_path(deep_forrest, clearing)
    make_path(clearing, strange_rock)
    make_path(clearing, bonfire)
    make_path(clearing, candy_house)
    make_path(waterfall, cave)

    return start_room