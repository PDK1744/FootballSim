import random
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

# Define position role
POSITIONS = {
  'offense': {
    'QB': 1,
    'RB': 1,
    'TE': 1,
    'WR': 3,
    'OL': 5,
  },
  'defense': {
    'DL': 4,
    'LB': 2,
    'CB': 3,
    'S': 2,
  },
  'special_teams': {
    'K': 1,
    'P': 1,
  }
}


class Team:
  def __init__(self, name, team_id=None):
    self.id = team_id
    self.name = name
    self.roster = []
    self.power_level = 0
    self.conference_id = None

  def add_player(self, player):
    self.roster.append(player)

  def calculate_power_level(self):
    if not self.roster:
      return 0
    total_skill_level = sum(player.skill_level for player in self.roster)
    average_skill_level = total_skill_level / len(self.roster)
    return average_skill_level

  def __str__(self):
    power_level = self.calculate_power_level()
    return f"{self.name} | Power Level: {power_level:.0f} | Conference ID: {self.conference_id} | Players: {len(self.roster)}"

def generate_random_team_name(length=8):
    city = fake.city()
    mascot = random.choice(MASCOTS)
    return f"{city} {mascot}"

def generate_random_player(position):    
    name = fake.name()
    skill_level = random.randint(50, 100)
    return Player(name, position, skill_level)

def generate_teams(num_teams, num_players_per_team):
  teams = []
  for _ in range(num_teams):
      team_name = generate_random_team_name()
      team = Team(team_name)
    #Generate offense players
      for position, count in POSITIONS['offense'].items():
        for _ in range(count):
          player = generate_random_player(position)
          team.add_player(player)
      #Generate defense players
      for position, count in POSITIONS['defense'].items():
        for _ in range(count):
          player = generate_random_player(position)
          team.add_player(player)

      #Generate special teams
      for position, count in POSITIONS['special_teams'].items():
        for _ in range(count):
            player = generate_random_player(position)
            team.add_player(player)
      team.calculate_power_level()
      teams.append(team)
  return teams
