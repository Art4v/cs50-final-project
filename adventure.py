# ------------
#  libraries
# ------------
from groq import Groq
from random import randint, choice
from sys import stdout
from time import sleep

# ------------
# global variables
# ------------

# speed
speed = 1

# api key
client = Groq(api_key="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")

# list of potential items
ITEMS = ["lantern", "old map", "rusty key", "silver dagger", "magic potion", "gold coin"]
HAZARDS = ["poisonous fog", "hidden snare", "falling branch", "wild animal", "quicksand", "spike trap"]

# -----------
# animations
# -----------

# loading animation
def load():
    for _ in range(randint(3, 8)):
            sleep(speed / 5)
            print(".", end="")
            sleep(speed / 5)
            print(".", end="")
            sleep(speed / 5)
            print(".")
    sleep(speed)
    print("\n!!!\n")
    sleep(speed / 2)

# typing animations
def type(text):
    delay = (speed/100)
    
    for char in text:
        stdout.write(char)
        stdout.flush()
        sleep(delay)

        if char in ".!?":
            sleep(delay * 6)
        elif char == ",":
            sleep(delay * 3)
        else:
            sleep(delay)
    print()
    sleep(speed)

def typed_input(text):
    delay = (speed/100)
    
    for char in text:
        stdout.write(char)
        stdout.flush()
        sleep(delay)
    return input()

# ------------------
# LLM functionality
# ------------------

# build prompt function
def build_prompt(current_scene, inventory, hazards, win, lose, option):
    # get current scene summary (compressed memory)
    summary = summarise_scene(current_scene, option)

    # win condition prompt
    if win:
        return f"""
    You are a text-based adventure game narrator.

    The player has reached a winning condition.

    PAST EVENTS (SUMMARY):
    {summary}

    INVENTORY:
    {', '.join(inventory) if inventory else 'empty'}

    CURRENT HAZARDS:
    {', '.join(hazards) if hazards else 'empty'}

    TASK:
    Describe the final victory scene in 2–3 sentences.
    Make it clear the player has found the lost treasure and escaped the forest.
    Ensure that scene is cohesive with the past events summary. 
    Do NOT present any further options.
    """

    # loss condition prompt
    elif lose:
        return f"""
    You are a text-based adventure game narrator.

    The player has reached a losing condition.

    PAST EVENTS (SUMMARY):
    {summary}

    INVENTORY:
    {', '.join(inventory) if inventory else 'empty'}

    CURRENT HAZARDS:
    {', '.join(hazards) if hazards else 'empty'}

    TASK:
    Describe the player's death or failure in 2–3 sentences.
    Make it final and conclusive.
    Ensure that scene is cohesive with the past events summary. 
    Do NOT present any further options.
    """

    # normal game continuation prompt
    else:
        # 1/4 chance of receiving an item
        available_items = [item for item in ITEMS if item not in inventory]
        gained_item = None

        if available_items and randint(1, 4) == 1:
            gained_item = choice(available_items)
            inventory.append(gained_item)
        else:
            gained_item = None
        # 1/4 chance of encountering a hazard:   
        available_hazard = [hazard for hazard in HAZARDS if hazard is not hazards]
        gained_hazard = None

        if available_hazard and randint(1, 4) == 1:
            gained_hazard = choice(available_hazard)
            hazards.append(gained_hazard)
        
        return f"""

     
    You are a text-based adventure game engine.

    PAST EVENTS (SUMMARY):
    {summary}

    INVENTORY:
    {', '.join(inventory) if inventory else 'empty'}

    CURRENT HAZARDS:
    {', '.join(hazards) if hazards else 'empty'}

    NEW EVENT:
    Continue the story in 2–4 sentences.
    Naturally incorporate the environment and tension of the forest.
    {f"The player finds a {gained_item}. Ensure this item discovery is properly implemented into the story." if gained_item else ""}. 
    {f"The player finds a {gained_hazard}. Ensure this hazard discovery is properly implemented into the story. " if gained_hazard else ""}. 


    INSTRUCTIONS:
    - Present exactly four numbered options (1–4).
    - Only ONE option may be dangerous.
    - Do NOT contradict past events.
    - Do NOT mention the word "summary".

    FORMAT EXACTLY LIKE THIS:

    <scene description>

    Options:
    1. ...
    2. ...
    3. ...
    4. ...
    """

# get next scene function
def get_next_scene(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a game engine"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8
    )
    return response.choices[0].message.content

# summarise current scene function
def summarise_scene(scene, option):
    # scaffold prompt
    prompt = f"""
    You are summarising a turn in a text-based adventure game.

    TASK:
    - Summarise the scene in 1–2 sentences.
    - Include ONLY what happened and the player's chosen action.
    - Ignore all other options that were not chosen.
    - Do NOT invent new events.
    - Keep it concise and factual.

    INPUT SCENE:
    {scene}

    PLAYER CHOICE:
    The player chose option {option}.

    OUTPUT FORMAT:
    <summary of what happened and the chosen action>
    """ 

    # request prompt for api
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You summarise game events for memory compression."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3     
    )

    return response.choices[0].message.content.strip()

# ---------------
# main functions
# ---------------

# greeting function
def start():
    type("*** WELCOME TO YOUR FOREST ADVENTURE ***")
    type("This is a text-based AI-powered adventure game where your mission is to find the lost treasure of the forest. Select options by inputting the digits 1, 2, 3, or 4 when prompted. To exit at any time, type 'exit'")
    while True:
        # get user input
        start = typed_input("Would you like to begin your journey? (y/n) ")
        # start or exit game based on input
        if start.lower() == "y":
            sleep(speed)
            type("Loading Journey...")
            load()
            type("Good luck!")
            print("\n***\n")
            sleep(speed)
            break
        elif start.lower() in ["n", "exit"]:
            sleep(speed)
            type("Come Back Soon!")
            exit()
        
    game()
    return    

# game start function
def game():

    # initialise turn count, win and loss trackers,, and inventory
    turn_count = 1
    win = False
    lose = False
    inventory = []
    hazards = []

    # initial scene
    scene = (
        "You wake beneath towering, ancient trees. A cold mist clings to the forest floor.\n"
        "Somewhere in this forest lies a lost treasure — and possibly your escape.\n\n"
        "Options:\n"
        "1. Follow the sound of running water\n"
        "2. Approach the stone archway\n"
        "3. Walk the narrow path\n"
        "4. Call out for help"
    )

    # game loop
    while True:
        # type out scenario
        print()
        type(scene)
        if win == True:
            print("CONGRATULATIONS ON FINDING THE LOST TREASURE AND ESCAPING THE FOREST!")
            break
        if lose == True:
            print("GAME OVER!")
            break


        # show inventory
        print(f"Inventory: {inventory}")

        # get choice
        choice = ""
        while choice not in {"1", "2", "3", "4", "exit"}:
            choice = typed_input("\n\nChoose an option (1–4), or type 'exit': ")

        # actions based on choice
        if choice in {"1", "2", "3", "4"}:
            # update global variables
            turn_count += 1
            chance_win = max(2, 15 - turn_count)
            chance_lose = max(2, 10 - turn_count)

            # win probability (increasing with turn_count)
            if randint(1, chance_win) == 1:
                win = True
                lose = False

            # loss probability (increasing with turn_count)
            if randint(1, chance_lose) == 1:
                lose = True
                win = False

            # if at turn 10, neither win or loss:
            if turn_count == 5:
                if randint(0, 1) == 1:
                    win = True
                    lose = False
                else:
                    # lose
                    win = False
                    lose = True
                
            # build prompt
            prompt = build_prompt(scene, inventory, hazards, win, lose, choice)
            scene = get_next_scene(prompt)

        if choice == "exit":
            sleep(speed)
            type("Come Back Soon!")
            exit()

# --------------
# call function
# --------------

start()
