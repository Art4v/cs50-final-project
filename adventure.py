# libraries
from random import randint
from time import sleep


# loading animation
def load(n, speed):
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


# greeting function
def start(speed):
    print("*** WELCOME TO YOUR FOREST ADVENTURE ***")
    sleep(speed)
    print("This is a text-based AI-powered adventure game where your mission is to find the lost treasure of the forest. Select options by inputting the digits 1, 2, 3, or 4 when prompted. To exit at any time, type 'exit'")
    sleep(speed)
    while True:
        # get user input
        start = input("Would you like to begin your journey? (y/n) ")
        # start or exit game based on input
        if start.lower() == "y":
            sleep(speed)
            print("Loading Journey...")
            load(3, speed)
            print("Good luck!")
            print("\n***\n")
            sleep(speed)
            break
        elif start.lower() in ["n", "exit"]:
            print("Come Back Soon!")
            exit()
        
    game()
    return  
     
# game start function
def game():
    print("Journey Under Construction")
    return


# call function
start(1)



