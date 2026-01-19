# libraries
from groq import Groq
from random import randint, choice
from sys import stdout
from time import sleep

# global variable for speed
speed = 0.5

# store api key
client = Groq(api_key="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")

# list of potential items
ITEMS = ["lantern", "old map", "rusty key", "silver dagger", "magic potion", "gold coin"]
HAZARDS = ["poisonous fog", "hidden snare", "falling branch", "wild animal", "quicksand", "spike trap"]

# loading animation
def load(n):
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

def typed_input(prompt):
    delay = (speed/100)
    
    for char in prompt:
        stdout.write(char)
        stdout.flush()
        sleep(delay)
    return input()

# check death function
def is_player_dead(state):
    return state["health"] <= 0

# get player state
def parse_state_update(text, state):
    health_change = 0
    item = None
    win = False

    for line in text.splitlines():
        if line.startswith("health_change:"):
            health_change = int(line.split(":")[1].strip())
        elif line.startswith("item_gained:"):
            item = line.split(":")[1].strip()
        elif line.startswith("win:"):
            win = line.split(":")[1].strip().lower() == "yes"

    state["health"] += health_change

    if item and item.lower() != "none":
        state["inventory"].append(item)

    state["win"] = win
    return state

# build prompt function
def build_prompt(player_choice, state, turn_count, win_turn, death_turn):
    # decide random item and hazard for this turn
    item_this_turn = choice(ITEMS)
    hazard_this_turn = choice(HAZARDS)

    # win/death flags
    win_flag = "none"
    death_flag = "none"

    if turn_count == win_turn:
        win_flag = "true"
    if turn_count == death_turn:
        death_flag = "true"

    return f"""
You are a text-based adventure game engine.

SETTING:
The player is trapped in a mysterious forest searching for a lost treasure.
The forest contains random items and hazards: {item_this_turn} and {hazard_this_turn} may appear in this turn.

PLAYER STATE:
- Health: {state['health']}
- Inventory: {', '.join(state['inventory']) if state['inventory'] else 'empty'}

PLAYER CHOICE:
The player chose option: {player_choice}

INSTRUCTIONS:
1. Describe what happens next in 2–4 sentences.
2. Present exactly four numbered options (1–4).
3. Include a STATE UPDATE section.
4. Health changes must be between -50 and +20 normally.
5. Only add ONE item at most; if using the item_this_turn, it may appear in inventory.
6. The player may die if health reaches 0.
7. If win_flag is true, one option must lead to a win (win: yes).
8. If death_flag is true, one option must lead to immediate death (health_change <= -200).
9. Incorporate the random hazard {hazard_this_turn} and/or item {item_this_turn} into the scene naturally.

FORMAT EXACTLY LIKE THIS:

<scene description>

STATE UPDATE:
health_change: <integer>
item_gained: <item name or none>
win: <yes or no>

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
            load(3)
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
    # define state variables
    state = {
        "health": 100,
        "inventory": [],
        "win": False
    }

    # decide random turns for win and death
    win_turn = randint(2, 5)      # win must occur in 2–5 moves
    death_turn = randint(1, 5)    # death must occur in 1–5 moves
    turn_count = 0

    # initial scene
    scene = (
        "You wake beneath towering, ancient trees. A cold mist clings to the forest floor.\n"
        "Somewhere in this forest lies a lost treasure—and possibly your escape.\n\n"
        "Options:\n"
        "1. Follow the sound of running water\n"
        "2. Approach the stone archway\n"
        "3. Pick up the rusted lantern and walk the narrow path\n"
        "4. Call out for help"
    )

    # game loop
    while True:
        turn_count += 1
        
        # type out scenario
        print()
        type(scene)

        # show HUD
        type(f"\n[Turn {turn_count} | Health: {state['health']} | Inventory: {state['inventory']}]\n")

        # get choice
        choice = typed_input("\n\nChoose an option (1–4): ")

        if choice not in {"1", "2", "3", "4", "exit"}:
            print("\nInvalid choice. Try again.")
            continue

        if choice == "exit":
            sleep(speed)
            type("Come Back Soon!")
            exit()

        # build prompt with turn info
        prompt = build_prompt(choice, state, turn_count, win_turn, death_turn)
        scene = get_next_scene(prompt)

        # apply state changes and check for win
        state = parse_state_update(scene, state)

        if state.get("win", False):
            type("\nA brilliant light shines from the trees...")
            type("Congratulations! You have found the lost treasure and won the game!")
            break

        # check death
        if is_player_dead(state):
            type("\nYour vision fades as the forest grows silent...")
            type("You have died.")
            break

# call function
start()
