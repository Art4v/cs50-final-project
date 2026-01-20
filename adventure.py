# ----------
# libraries
# ----------

from groq import Groq
from os import getenv
from random import randint, choice
from sys import stdout, exit
from time import sleep

# --------------
# api key setup
# --------------

api_key = getenv("GROQ_API_KEY")
if not api_key:
    print("Error: GROQ_API_KEY not set.")
    print("Please provide your Groq API key, or set as an environment variable.")
    if input("Would you like to provide your Groq API Key? (y/n) ").lower() == "y":
        api_key = input("Enter your Groq API key: ").strip()
    else:
        exit(1)

client = Groq(api_key=api_key)

# -----------------
# global variables
# -----------------

# delay
speed = 1

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
            sleep(speed / 5)
    sleep(speed)
    print("!!!\n")
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
def build_prompt(current_scene, inventory, hazards, win, lose, option, history, turn_count):
    # get current scene summary (compressed memory)
    history.append(summarise_scene(current_scene, option, turn_count))

    # win condition prompt
    if win:
        return f"""
        You are a text-based adventure game narrator.

        GAME STATE:
        - The player has achieved a WIN condition.

        STORY MEMORY (CHRONOLOGICAL):
        {history}

        PLAYER INVENTORY:
        {', '.join(inventory) if inventory else 'empty'}

        ACTIVE HAZARDS:
        {', '.join(hazards) if hazards else 'empty'}

        TASK:
        - Write the FINAL victory scene in 2–3 sentences using a second person narration style.
        - The player must successfully find the lost treasure AND escape the forest.
        - The scene must logically follow the MOST RECENT player choice.
        - Maintain continuity with the story memory above.
        - Be conclusive and final.

        RULES:
        - Do NOT present options.
        - Do NOT introduce new items or hazards.
        - Do NOT contradict past events.
        """


    # loss condition prompt
    elif lose:
        return f"""
        You are a text-based adventure game narrator.

        GAME STATE:
        - The player has reached a LOSS condition.

        STORY MEMORY (CHRONOLOGICAL):
        {history}

        PLAYER INVENTORY:
        {', '.join(inventory) if inventory else 'empty'}

        ACTIVE HAZARDS:
        {', '.join(hazards) if hazards else 'empty'}

        TASK:
        - Write the FINAL failure or death scene in 2–3 sentences using a second person narration style.
        - The outcome must be permanent and conclusive.
        - The scene must logically follow the MOST RECENT player choice.
        - Maintain continuity with the story memory above.

        RULES:
        - Do NOT present options.
        - Do NOT introduce new items or hazards.
        - Do NOT contradict past events.
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

        STORY MEMORY (CHRONOLOGICAL):
        {history}

        PLAYER INVENTORY:
        {', '.join(inventory) if inventory else 'empty'}

        ACTIVE HAZARDS:
        {', '.join(hazards) if hazards else 'empty'}

        TASK:
        - Continue the story in 2–4 sentences using a second person narration style.
        - The scene MUST be a direct consequence of the player’s MOST RECENT choice.
        - Maintain a tense, mysterious forest atmosphere.
        {f"- Introduce the newly discovered item: {gained_item}." if gained_item else ""}
        {f"- Introduce the newly encountered hazard: {gained_hazard}." if gained_hazard else ""}

        RULES:
        - Present EXACTLY four numbered options (1–4).
        - ONLY ONE option may be dangerous.
        - At least ONE option must meaningfully reference the player’s inventory (if not empty).
        - Do NOT contradict previous events.
        - Do NOT mention the word “summary”.

        FORMAT (STRICT — FOLLOW EXACTLY):

        <consequence of the player's most recent choice>

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
def summarise_scene(scene, option, turn_count):
    # scaffold prompt
    prompt = f"""
    You are compressing memory for a text-based adventure game.

    TASK:
    - Summarise ONE turn in 1–2 sentences.
    - Include ONLY events that occurred and the player’s chosen action.
    - Ignore all unchosen options.
    - Do NOT invent or infer new information.
    - Be factual and concise.

    TURN NUMBER:
    {turn_count}

    INPUT SCENE:
    {scene}

    PLAYER ACTION:
    Option {option}

    OUTPUT FORMAT (STRICT):

    Turn {turn_count}: <brief factual summary>
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
    type("This is an AI-powered text-adventure game where your mission is to find the lost treasure of the forest. Select options by inputting the digits 1, 2, 3, or 4 when prompted. To exit at any time, type 'exit'")
    while True:
        # get user input
        start = typed_input("Would you like to begin your journey? (y/n) ")
        # start or exit game based on input
        if start.lower() == "y":
            sleep(speed)
            type("Loading Journey...")
            load()
            type("Good luck!")
            print("\n***")
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

    # initialise turn count, win and loss trackers, inventory, and history
    turn_count = 1
    win = False
    lose = False
    inventory = []
    hazards = []
    history = []

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
        # print(f"\nWin:{win}, Lose: {lose}\n")        
        # type out scenario
        print()
        type(scene)
        if win == True:
            print()
            print("CONGRATULATIONS ON FINDING THE LOST TREASURE AND ESCAPING THE FOREST!")
            print()
            break
        if lose == True:
            print()
            print("GAME OVER!")
            print()
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
            chance_win = 30 - 2 * turn_count
            chance_lose = 25 - 2 * turn_count

            # win probability (increasing with turn_count)
            if randint(1, chance_win) == 1 and turn_count != 1:
                win = True
                lose = False

            # loss probability (increasing with turn_count)
            if randint(1, chance_lose) == 1  and turn_count != 1:
                lose = True
                win = False

            # if at turn 10, neither win or loss:
            if turn_count == 10:
                if randint(0, 1) == 1:
                    win = True
                    lose = False
                else:
                    # lose
                    win = False
                    lose = True
                
            # build prompt
            prompt = build_prompt(scene, inventory, hazards, win, lose, choice, history, turn_count)
            scene = get_next_scene(prompt)

            # change turn 
            turn_count += 1
        
        if choice == "exit":
            sleep(speed)
            print()
            type("Come Back Soon!")
            print()
            exit()

# -----------------------------
# call functions to start game
# -----------------------------

start()
