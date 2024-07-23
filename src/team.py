import random
import names
from player import Player
from faker import Faker

fake = Faker()

# List of random mascot names
MASCOTS = [
    "Thunderclaws",
    "Iron Hawks",
    "Storm Raptors",
    "Steel Titans",
    "Firewolves",
    "Shadow Knights",
    "Blaze Dragons",
    "Golden Lions",
    "Frost Giants",
    "Phantom Panthers",
    "Mystic Bears"
]


class Team:
  def __init__(self, name):
    self.name = name
    self.roster = []

  def add_player(self, player):
    self.roster.append(player)

  def __str__(self):
    return f"{self.name} with {len(self.roster)} players"

def generate_random_team_name(length=8):
    city = fake.city()
    mascot = random.choice(MASCOTS)
    return f"{city} {mascot}"

def generate_random_player():    
    name = fake.name()
    position = random.choice(['QB', 'RB', 'WR', 'TE', 'OL', 'DL', 'LB', 'CB', 'S', 'K', 'P'])
    skill_level = random.randint(50, 100)
    return Player(name, position, skill_level)

def generate_teams(num_teams, num_players_per_team):
  teams = []
  for _ in range(num_teams):
      team_name = generate_random_team_name()
      team = Team(team_name)
      for _ in range(num_players_per_team):
          player = generate_random_player()
          team.add_player(player)
      teams.append(team)
  return teams
