import glicko2
import pickle
from os import path

env = glicko2.Glicko2()

class Player(object):
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

players = []

# Load players
if path.exists("ratings.pkl"):
    with open("ratings.pkl", "rb") as input:
        players = pickle.load(input)

# Print out player rankings
for player in players:
    print(f"{player.name} : {player.rating.mu}")

# Save players
with open("ratings.pkl", "wb") as output:
    pickle.dump(players, output, pickle.HIGHEST_PROTOCOL)