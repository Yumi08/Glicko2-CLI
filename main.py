import glicko2
import pickle
import os
import shlex
import random
from dotenv import load_dotenv

VERSION = "1.5.1"

load_dotenv()

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

    if os.getenv("DEBUG") == "True":
        print(f"[PLAYER 1: {rank1_initial} -> {rank1_final}]")
        print(f"[PLAYER 2: {rank2_initial} -> {rank2_final}]")
def command_potential(player1, player2):
    if (not player1 in players) or (not player2 in players):
        print("Player unknown.")
        return
    
    rank1_initial = players[player1]
    rank2_initial = players[player2]

    result = env.rate_1vs1(players[player1], players[player2])

    rank1_final = result[0]
    rank2_final = result[1]

    print(f"If {player1} won against {player2}:")
    print(f"{player1}: +{round(rank1_final.mu - rank1_initial.mu)} to {round(rank1_final.mu)}")
    print(f"{player2}: -{abs(round(rank2_final.mu - rank2_initial.mu))} to {round(rank2_final.mu)}")

    if os.getenv("DEBUG") == "True":
        print(f"[PLAYER 1: {rank1_initial} -> {rank1_final}]")
        print(f"[PLAYER 2: {rank2_initial} -> {rank2_final}]")
def command_info(player):
    if not player in players:
        print("Player unknown.")
        return
    
    print(f"-- {player}\'s Info --")
    print(f"Rating: {round(players[player].mu)}")
    print(f"Deviation: {round(players[player].phi)}")
def command_ranks():
    ranks = {k: v for k, v in sorted(players.items(), key=lambda item: item[1].mu, reverse=True)}
    i = 1
    for player in ranks:
        print(f"{i}. {player} - {round(players[player].mu)}")
        i += 1
def command_recommend(player):
    ranks = {k: v for k, v in sorted(players.items(), key=lambda item: abs(players[player].mu - item[1].mu), reverse=False)}
    i = 0
    for player_ in ranks:
        if i == 0:
            i += 1
            continue
        print(f"{i}. {player_} - {round(players[player_].mu)} (Diff: {round(players[player_].mu - players[player].mu)})")
        i += 1
def command_recommendr():
    random_player = random.choice(list(players.keys()))
    ranks = {k: v for k, v in sorted(players.items(), key=lambda item: abs(players[random_player].mu - item[1].mu), reverse=False)}
    print(f"{random_player} vs {list(ranks)[1]}")
def command_add(name, mu=None):
    if mu == None:
        mu = 1500
    players[name] = env.create_rating(mu=mu)
    print("Adding player.")
def command_remove(name):
    choice = input(f"Are you sure you want to remove player \"{name}\"? (YES or NO): ")
    if choice == "YES":
        del players[name]
        print(f"Removing player \"{name}\"...")
    else:
        print("Cancelling...")
def command_rename(playername1, playername2):
    if not playername1 in players:
        print("Player unknown.")
        return
    
    if playername2 in players:
        print("Player name already taken.")
        return
    
    players[playername2] = players[playername1]
    del players[playername1]    
def command_reset():
    choice = input("Are you sure you want to delete ALL player data? (YES or NO): ")
    if choice == "YES":
        players.clear()
        print("RESETTING ALL PLAYERS...")
    else:
        print("Cancelling...")

# Load players
if os.path.exists("ratings.pkl"):
    with open("ratings.pkl", "rb") as file:
        players = pickle.load(file)

print(f"Welcome to Glicko2-CLI v{VERSION}")
if os.getenv("DEBUG") == "True":
    print("DEBUG MODE")

while True:
    command = input("Enter command: ")

    # Execute commands
    if command != "":
        if shlex.split(command)[0] == "help":
            print("""--- Help ---
match [winner] [loser] - Log a match between two players.
potential [winner] [loser] - Simulate a match between two players. Ranks will not be altered.
info [player] - Get information about a specific player.
ranks - Show the leaderboard.
recommend [player] - See who matchmaking thinks a certain player should play against.
recommendr - Allow matchmaking to make a random match.
add [player] [rating=1500] - Add a player.
remove [player] - Remove a player.
rename [player initial] [player final] - Rename a player.
reset - Reset everything.
exit - Exit.""")
        elif shlex.split(command)[0] == "match":
            command_match(shlex.split(command)[1], shlex.split(command)[2])
        elif shlex.split(command)[0] == "potential":
            command_potential(shlex.split(command)[1], shlex.split(command)[2])
        elif shlex.split(command)[0] == "info":
            command_info(shlex.split(command)[1])
        elif shlex.split(command)[0] == "ranks":
            command_ranks()
        elif shlex.split(command)[0] == "recommend":
            command_recommend(shlex.split(command)[1])
        elif shlex.split(command)[0] == "recommendr":
            command_recommendr()
        elif shlex.split(command)[0] == "add":
            if len(shlex.split(command)) == 2:
                command_add(shlex.split(command)[1])
            else:
                command_add(shlex.split(command)[1], shlex.split(command)[2])
        elif shlex.split(command)[0] == "remove":
            command_remove(shlex.split(command)[1])
        elif shlex.split(command)[0] == "rename":
            command_rename(shlex.split(command)[1], shlex.split(command)[2])
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
