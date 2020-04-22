from random import randint
from options import *
from enemies import _bunny, _crab, _goat, _wizard, _unicorn


def world():
    checkpoint = bedroom = Rolodex("bedroom", "home", True)
    closet = Rolodex("closet", "home", True)
    hallway = Rolodex("hallway", "home", True)
    livingroom = Rolodex("livingroom", "home", True)
    garden = Rolodex("your home", "home", True)
    road = Rolodex("town road", "town", True)
    neighbour = Rolodex("miss tover's house", "home", True)
    tover_house = Rolodex("tover house", "home")
    inn = Rolodex("inn", "shop")
    inn_seat = Rolodex("seat", "shop")
    alley = Rolodex("alley", "tension")
    town_center = Rolodex("town square", "town", True)
    bakery = Rolodex("bakery", "shop")
    magicshop = Rolodex("magicshop", "shop")
    armory = Rolodex("armory", "shop")
    training = Rolodex("training", "shop")
    castle_gate = Rolodex("castle gate", "town", True)
    bank = Rolodex("bank", "shop")
    castle = Rolodex("castle","tension")
    start_room = town_bridge = Rolodex("town bridge", "forrest", True)
    crossroads = Rolodex("crossroads", "forrest", True, spawn=_bunny)
    long_road = Rolodex("long road", "forrest", spawn=_bunny)
    dunes = Rolodex("dunes", "forrest", spawn=_crab)
    sea = Rolodex("sea", "forrest", spawn=_crab)
    harbor = Rolodex("the harbor", "tension", spawn=_crab)
    forrest_path = Rolodex("forrest path", "forrest", spawn=_bunny)
    river = Rolodex("river", "forrest", spawn=_bunny)
    forrest = Rolodex("forrest", "forrest", spawn=_bunny)
    lake = Rolodex("the lake", "forrest")
    clearing = Rolodex("clearing", "forrest",spawn=_bunny)
    waterfall = Rolodex("waterfall", "forrest")
    cave = Rolodex("cave", "tension")
    bonfire = Rolodex("bonfire", "tension")
    tower = Rolodex("wizard tower", "tension",spawn=_wizard)
    forrest_cabin = Rolodex("cabin", "forrest", spawn=_bunny)
    in_forrest_cabin = Rolodex("cabin", "tension")
    deep_forrest = Rolodex("deep forrest", "forrest", spawn=_unicorn)
    strange_rock = Rolodex("strange rock", "tension", spawn=_unicorn)
    candy_house = Rolodex("candy house", "tension")
    ufo = Rolodex("crashlanded ufo")
    mountain_path = Rolodex("canyon path", "forrest", spawn=_goat)
    canyon_path = Rolodex("mountain path", "forrest", spawn=_goat)
    mountain_cabin = Rolodex("cabin", spawn=_goat)
    in_mountain_cabin = Rolodex("cabin", spawn=_goat)
    mines = Rolodex("the mines", "tension")
    
    #BEDROOM
    def sleep():
        base.interface.say("good night!")
        base.transition.setFadeColor(0,0,0)
        base.start_sequence(
            Func(base.transition.fadeOut, 2),
            Wait(4),
            Func(base.transition.fadeIn, 2),
            Func(base.interface.say, "...and wake up!"),
            Func(base.interface.say, "you feel refreshed!"),
        )
        
        base.interface.hp = base.interface.max_hp
    bed = verb(bedroom, "bed", "It is not very soft.")
    bed.add(Return("sleep", "you step in the bed")).function = sleep
    bedroom_livingroom_door = bedroom.add(Door(
        name="door", destination=livingroom, 
        description="a damaged wooden door"))
    bedroom_closet_door = bedroom.add(Door(
        name="closet", destination=closet, 
        description ="The wooden closet holding your wardrobe."))
        # CLOSET
    closet.add(Door(destination=bedroom, mimic=bedroom_closet_door))
    closet.add(Equipment("plain clothes", "armor", 0, 0, 2))
        # DESK
    desk = Rolodex("work bench", explored=True)
    bedroom.add(Move("work bench", desk, "you inspect the bench."))
    verb(desk, "broken watch",  "you were supposed to fix this a long time ago")
    desk.add(Money(150))
    verb(desk, "jeweler tools",  "tools of your trade...once upon a time")
    desk.add(Nevermind(bedroom, "You stop inspecting the bench."))
    # LIVINGROOM
    verb(livingroom, "window", "you bathe in the sun's warmth")
    front_door = livingroom.add(Door(garden, "front door"))
    front_door.locked = "It won't open. It's locked."
        # WALL HOOKS
    hooks = Rolodex("wall hooks", explored=True)
    livingroom.add(Move("wall hooks", hooks, "you inspect the wall hooks."))
    verb(hooks, "wet spot", "a broken rainpipe will do that to you", has_money=False)
    hooks.add(Nevermind(livingroom, "You stop inspecting the wall hooks."))
        # FRONT DOOR AND KEY
    def unlock_front_door(activated, activator):
        if front_door.locked:
            front_door.locked = None
            base.interface.say("You unlock the door with a satisfying click.")
        else:
            base.interface.say("It's already unlocked.")
    key = hooks.add(Item("key"))
    key.add(Return("feel", "It's a bit rusty."))
    key.add(Use(
        "use", "That doesn't work.", 
        front_door, unlock_front_door))
    livingroom_chair = livingroom.add(Menu("chair"))
    livingroom_chair.add(Return("feel", "A good balance between softness and support"))
    livingroom_chair.add(Return("sit", "You sit down for a few, and stand up again."))
    livingroom.add(Door(destination=bedroom, name="door", mimic=bedroom_livingroom_door))
    livingroom_bookcase = livingroom.add(Menu("piano"))
    livingroom_bookcase.add(Return("listen", "B2 is a little flat. Could use another tune up."))
    livingroom_bookcase.add(Return("feel", "The keys are nice and weighty."))
    livingroom_bookcase.add(Return("play", "You play the first three notes of toccata et fugue."))
    # GARDEN
    verb(garden, "flowerbed", "they smell so good", verb="smell")
    garden.add(Door(destination=livingroom, name="front door", mimic=front_door))
    verb(garden, "shrub", "a fresh smelling shrubbery", verb="smell")
    make_path(road, garden)
    make_path(town_bridge, road)   
    make_path(road, neighbour)
    make_path(town_center, road)
    # MISS TOVER
    verb(neighbour, "flowers", "Miss Tover likes flowers almost as much as you do")
    make_open_door(neighbour, tover_house, "front door")
    verb(neighbour, "small tree", "a very dry old pine tree.")
    tover_house.add(NPC("miss tover", [
        "Ah it's you. Can do anything for you?",
        "I haven't stepped outside this town in over 30 years.",
        "Did you ever leave the city?",
        "My son David works in the mines.",
    ]))
    # TOWN CENTER
        #BAKERY
    make_open_door(town_center, bakery, "bakery door")
    bakery.add(Item("oven", cost=50000)) 
    bakery.add(Item("flour", cost=50)) 
    bakery.add(Item("yeast", cost=50)) 
    bakery.add(NPC("baker", [
        "Good day, friend. What will it be?",
        "Take a look...euh smell around!",
        "I start baking at 4AM.",
        "Don't you just love the smell of bread?",
    ]))
    bakery.add(Item("baguette", cost=250)) 
    bakery.add(Item("broodje", cost=250)) 
    bakery.add(Item("bretzel", cost=250)) 
        # ARMORY
    make_open_door(town_center, armory, "armory door")
    armory.add(Equipment("wooden sword", "weapon", 50, 2, 0))
    armory.add(Equipment("iron sword", "weapon", 200, 5, 0))
    armory.add(Equipment("steel sword", "weapon", 1000, 10, 0))
    armory.add(NPC("smith", [
        "What will it be, huh?",
        "Finest steel in the land!",
        "Bending steel is hard work.",
        "We have a special offer on wooden swords today.",
    ]))
    armory.add(Equipment("leather armor", "armor", 250, 0, 5))
    armory.add(Equipment("chain armor", "armor", 1000, 0, 10))
    armory.add(Equipment("plate armor", "armor", 2500, 0, 25))
    verb(town_center, "well", "dank stones. the town's water supply.")
        # ALLEY
    make_path(town_center, alley)
    alley.add(NPC("thug", [
        "what the hell are you staring at!?",
        "get the hell out of my face, boy.",
        "you're getting on my nerves.",
    ]))
        # INN
    make_open_door(town_center, inn, "inn door")
            # seat
    verb(inn_seat, "menu", "A flat foldable square.", verb="feel")
    verb(inn_seat, "table", "You drum a little rythm.", verb="drum")
    verb(inn_seat, "candle", "It's sitting on a sturdy candle holder.")
            # chairs
    inn.add(Move("seat", inn_seat, "you take a seat"))
    inn.add(Move("seat", inn_seat, "you take a seat"))
    inn.add(Move("seat", inn_seat, "you take a seat"))
    inn_seat.add(Move("stand back up", inn, "you stand up again"))
    inn.add(NPC("innkeeper", [
        "Come in! Have a seat!",
        "What can I get you?",
        "A room is 30 gold a night.",
        "This mead comes all the way from Albaden.",
    ]))
    inn.add(Move("seat", inn_seat, "you take a seat")) 
    inn.add(Move("seat", inn_seat, "you take a seat")) 
    inn.add(Move("seat", inn_seat, "you take a seat")) 
    # MAGIC SHOP
    make_open_door(town_center, magicshop, "magicshop door")  
    magicshop.add(Item("red potion", cost=50))
    magicshop.add(Item("green potion", cost=50))
    magicshop.add(Item("blue potion", cost=50))
    magicshop.add(NPC("magician", [
        "Spells and curses for sale.",
        "Careful, that's very unstable!",
        "I can tell you have a good ear for magic.",
        "Magic, ladies and gentlemen.",
    ]))
    magicshop.add(Equipment("blue pendant", "necklace", cost=500))
    magicshop.add(Equipment("green pendant", "necklace", cost=500))
    magicshop.add(Equipment("red pendant", "necklace", cost=500))
    # TRAINER
    make_open_door(town_center, training, "trainer door")
    training.add(NPC("trainer", [
        "Need some training?",
        "Just walk up to the equipment!",
        "Don't you want to feel the burn?",
        "Are you pumped yet?",
    ]))
    # CASTLE
    make_open_door(castle_gate, bank, "banker door") 
    bank.add(NPC("banker", [
        "Need someone to hold on to your money?",
        "Interest makes the world go round.",
        "Sorry, we're all out of loans.",
        "Life insurance perhaps?",
    ]))
    make_path(castle_gate, town_center)
    make_open_door(castle_gate, castle, "castle door") 
    castle.add(NPC("castle guard", [
        "You can't just walk into the castle like that.",
        "The king is too busy to see the likes of you.",
        "What makes you think you can just barge in here?",
    ]))
    # BRIDGE
    verb(town_bridge, "river", "the river flows under the bridge", verb="listen")
    make_path(town_bridge, crossroads)
    verb(town_bridge, "river", "the river flows under the bridge", verb="listen")
    # CROSSROADS
    make_path(crossroads, forrest_path)
    make_path(crossroads, long_road)
    make_path(crossroads, mountain_path)
    make_path(long_road, forrest_cabin)
    make_path(long_road, dunes)
    verb(long_road, "street lantern", "provides illumination to those who need it")
    # SEA DIRECTION
    verb(dunes, "seashell", "it emulates the ocean sound", verb="listen")
    make_path(dunes, sea)
    verb(dunes, "grass patch", "a patch of grass surrounded by warm sand")
        # SEA
    verb(sea, "seaweed", "a bit of seaweed washed ashore")
    make_path(sea, harbor)
    verb(sea, "sea", "you hear crashing ocean waves", verb="listen")
    verb(sea, "seagul", "a seagul squeeks at you", verb="listen")
        # HARBOR
    make_path(dunes, harbor)
    verb(harbor, "the harbor", "You smell a lot of fish! All ashore!", verb="listen")
    # MOUNTAIN DIRECTION
    verb(mountain_path, "canyon view", "You throw a pebble. Long way down.", verb="listen")
    make_path(mountain_path, canyon_path)
    verb(mountain_path, "cliff face", "an vertical, cold cliff face")
    verb(canyon_path, "stack of rocks", "someone has stacked some rocks on top of eachother")
    make_path(canyon_path, mountain_cabin)
    make_open_door(mountain_cabin, in_mountain_cabin, "cabin door")
    verb(in_mountain_cabin, "broken table", "this table is missing two legs")
    verb(in_mountain_cabin, "hole in floor", "the hole exposes a crack in the foundation")
    verb(in_mountain_cabin, "torn wallpaper", "there's a tear in the wallpaper here")
    make_path(canyon_path, mines)
    mines.add(NPC("miner", [
        "Sorry, but this mine is off limits."
    ]))
    # FORREST DIRECTION
    verb(forrest_path, "big tree", 
        "you can't quite put your arms around it")
    make_path(forrest_path, lake)
    verb(forrest_path, "bench", "A park bench for the resting of tired legs.")
    # FORREST CABIN
    verb(forrest_cabin, "birdhouse", "No birds.", verb="listen")
    make_path(forrest_path, forrest_cabin)
    make_open_door(forrest_cabin, in_forrest_cabin, "cabin door")
    verb(in_forrest_cabin, "dresser", "probably contains the old man's clothes")
    in_forrest_cabin.add(NPC("old man", [
        "Who's there?",
        "Get out of my house!",
        "Who do you think you are?",
        "...scaring an old man like that.",
        "Wait, what was I talking about?",
    ]))
    verb(in_forrest_cabin, "grandfather clock", "that's quite a clock. It's not ticking.")
    verb(in_forrest_cabin, "bunk bed", "three beds stacked on top of eachother.")
    # LAKE
    make_path(lake, river)
    verb(lake, "lake", "the water is very cold, but not deep.")
    make_path(lake, forrest)
    verb(lake, "walnut tree", "The fruit feel like wallnuts.")
    make_path(lake, tower)
    verb(lake, "berry bush", "better leave them alone, might be poisonous.", verb="taste")
    make_path(forrest, deep_forrest)
    # WIZARD TOWER
    tower_door = verb(tower, "tower entrance", "the seams betrays a large stone door")
    tower_door.add(Return("open", "it is magically sealed"))
    verb(tower, "fern", "these leafs are unmistakenly fern-like")
    # LIGHT FORREST
    verb(forrest, "tree", "Not quite sure what kind of tree this is.")
    make_path(forrest, candy_house)
    verb(forrest, "mushrooms", "a small group of mushrooms")
    make_path(forrest, waterfall) 
    verb(forrest, "boulder", "a decently sized boulder sticking out of the dirt")
    verb(river, "river", "Riverrun, past Eve and Adam's, from swerve of shore to bend of bay")
    # DEEP FORREST
    verb(deep_forrest, "foliage", "a cluster of trees and shrubs")
    verb(deep_forrest, "foliage", "a cluster of trees and shrubs")
    make_path(river, deep_forrest)
    verb(deep_forrest, "foliage", "a cluster of trees and shrubs")
    verb(deep_forrest, "foliage", "a cluster of trees and shrubs")
    make_path(deep_forrest, clearing)
    verb(deep_forrest, "foliage", "a cluster of trees and shrubs")
    verb(deep_forrest, "foliage", "a cluster of trees and shrubs")
    # STRANGE ROCK
    make_path(clearing, strange_rock)
    verb(strange_rock, "strange rock", "An enormous strange, vibrating stone")
    # BONFIRE
    make_path(clearing, bonfire)
    verb(bonfire, "bonfire", "there's a fire here, someone must have been here only recently")
    # CANDY HOUSE
    make_path(clearing, candy_house)
    verb(candy_house, "candy mailbox", "it tastes like candy", verb="taste")
    verb(candy_house, "candy house", "A house made of candy but you don't taste an entrance.", verb="taste")
    verb(candy_house, "candy fence", "a picket fence made of...candy", verb="taste")
    # WATERFALL
    #make_path(waterfall, cave) # TODO: Cave is behind the waterfall
    verb(waterfall, "puddle", "you go splish splash", verb="splash")
    verb(waterfall, "waterfall", "A fog of water tickles your face. sparkles!")
    verb(waterfall, "wet boulder", "water from the waterfall moistens this boulder")
    return start_room, checkpoint
