# libraries
from time import sleep


# intro card
print("*** WELCOME TO YOUR FOREST ADVENTURE ***")
sleep(1)
print("This is a text-based adventure game where your mission is to find the lost treasure of the forest. Select options by inputting the digits 1, 2, 3, or 4 when prompted!")
sleep(1)
if input("Would you like to begin your journey? (y/n) ").lower() == "y":
    sleep(1)
    print("Good luck!")
    print("\n***\n")
    sleep(1)
else:
    print("Come Back Soon!")
    exit()

# main game
print("Journey Under Construction...")

