import os
import time


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait(sec):
    time.sleep(sec)


def options():
    print("Welcome to the strat helper!")
    wait(1.5)
    print("Note you do need to be connected to the internet to use the program")
    wait(2)
    input("Press Enter to continue")
    clear()
    print("Options:")
    print("1. Look up stats for one team for one season")
    print("2. Look up the stats for one team for every season they have ever particpated in")
    print("3. Compare two teams")
    print("4. Predict who will win between two teams")
    print("5. Get match data")
    print("6. Get event data")
    return int(input("Please select an option(1-6): "))