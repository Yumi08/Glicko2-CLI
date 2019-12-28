import glicko2
import pickle
from os import path
import shlex

DEBUG = True

env = glicko2.Glicko2()
players = {}

# Commands
def command_match(player1, player2):
    if (not player1 in players) or (not player2 in players):
        print("Player unknown.")
        return
    
    rank1_initial = players[player1]
    rank2_initial = players[player2]

    result = env.rate_1vs1(players[player1], players[player2])
    players[player1] = result[0]
    players[player2] = result[1]

    rank1_final = players[player1]
    rank2_final = players[player2]

    print(f"{player1} wins against {player2}!")
    print(f"{player1}: +{round(rank1_final.mu - rank1_initial.mu)} to {round(rank1_final.mu)}")
    print(f"{player2}: -{abs(round(rank2_final.mu - rank2_initial.mu))} to {round(rank2_final.mu)}")

    if DEBUG:
        print(f"[PLAYER 1: {rank1_initial} -> {rank1_final}]")
        print(f"[PLAYER 2: {rank2_initial} -> {rank2_final}]")
def command_info(player):
    if not player in players:
        print("Player unknown.")
        return
    
    print(f"-- {player}\'s Info --")
    print(f"Rating: {round(players[player].mu)}")
    print(f"Deviation: {round(players[player].phi)}")
def command_add(name, mu=None):
    if mu == None:
        mu = 1500
    players[name] = env.create_rating(mu=mu)
    print("Adding player.")
def command_ranks():
    ranks = {k: v for k, v in sorted(players.items(), key=lambda item: item[1].mu, reverse=True)}
    i = 1
    for player in ranks:
        print(f"{i}. {player} - {round(players[player].mu)}")
        i += 1
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

while True:
    command = input("Enter command: ")

    # Execute commands
    if command != "":
        if shlex.split(command)[0] == "match":
            command_match(shlex.split(command)[1], shlex.split(command)[2])
        elif shlex.split(command)[0] == "info":
            command_info(shlex.split(command)[1])
        elif shlex.split(command)[0] == "add":
            if len(shlex.split(command)) == 2:
                command_add(shlex.split(command)[1])
            else:
                command_add(shlex.split(command)[1], shlex.split(command)[2])
        elif shlex.split(command)[0] == "ranks":
            command_ranks()
        elif shlex.split(command)[0] == "remove":
            command_remove(shlex.split(command)[1])
        elif shlex.split(command)[0] == "reset":
            command_reset()
        elif shlex.split(command)[0] == "exit":
            break
        else:
            print("Unknown command.")
    else:
        print("Nevermind.")

    # Save players
    with open("ratings.pkl", "wb") as output:
        pickle.dump(players, output, pickle.HIGHEST_PROTOCOL)

# Save players
with open("ratings.pkl", "wb") as output:
    pickle.dump(players, output, pickle.HIGHEST_PROTOCOL)
