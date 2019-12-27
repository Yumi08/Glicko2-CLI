import glicko2
import pickle
from os import path
import shlex

env = glicko2.Glicko2()

players = {}

command = input("Enter command: ")

# Commands
def command_add(name):
    players[name] = env.create_rating()
    print("Adding player.")
def command_ranks():
    for player in players.items():
        print(f"{player[0]} - {player[1].mu}")
def command_remove(name):
    choice = input(f"Are you sure you want to remove player \"{name}\"? (YES or NO): ")
    if choice == "YES":
        del players[name]
        print(f"Removing player \"{name}\"...")
    else:
        print("Cancelling...")
def command_reset():
    choice = input("Are you sure you want to delete ALL player data? (YES or NO): ")
    if choice == "YES":
        players.clear()
        print("RESETTING ALL PLAYERS...")
    else:
        print("Cancelling...")

# Load players
if path.exists("ratings.pkl"):
    with open("ratings.pkl", "rb") as file:
        players = pickle.load(file)

# Execute commands
if command != "":
    if shlex.split(command)[0] == "add":
        command_add(shlex.split(command)[1])
    elif shlex.split(command)[0] == "ranks":
        command_ranks()
    elif shlex.split(command)[0] == "remove":
        command_remove(shlex.split(command)[1])
    elif shlex.split(command)[0] == "reset":
        command_reset()
    else:
        print("Unknown command.")
else:
    print("Nevermind.")

# Save players
with open("ratings.pkl", "wb") as output:
    pickle.dump(players, output, pickle.HIGHEST_PROTOCOL)