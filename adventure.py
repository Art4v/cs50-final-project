# libraries
from groq import Groq
from random import randint
from sys import stdout
from time import sleep

# global variable for speed
speed = 1

# store api key
client = Groq(api_key="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")

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
    # introduction
    type("You wake beneath towering, ancient trees, their twisted branches knitting together to blot out the sky. A cold mist curls around your ankles, and the air smells of damp earth and pine. Your head throbs as you push yourself up from the forest floor, memories hazy—except for one thing: a legendary treasure is hidden somewhere in this forest, and finding it may be the only way out.")
    sleep(speed)
    type("To your left, you hear the faint sound of running water, steady and rhythmic. Ahead of you, half-hidden by vines, stands a crumbling stone archway carved with strange symbols. Behind you, the trees thin slightly, revealing a narrow path marked by broken branches, as if someone—or something—passed through recently. At your feet lies a rusted lantern, surprisingly intact.")
    sleep(speed)
    print()
    type("What do you do?")
    sleep(speed/2)
    type("1. Follow the sound of running water, hoping it leads to a river or civilization.")
    sleep(speed/2)
    type("2. Approach the stone archway and examine the strange symbols carved into it.")
    sleep(speed/2)
    type("3. Pick up the lantern and walk down the narrow path, staying alert for danger.")
    sleep(speed/2)
    type("4. Call out for help, listening carefully for any response from the forest.")
    sleep(speed/2)
    user_input = typed_input("Type the number of your choice. ")

        
    return

# call function
start()



