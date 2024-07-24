import sqlite3
import os
from player import Player
from team import Team

def create_connection():
    #Define path for database folder
    db_folder = os.path.join('..', 'data')
    db_path = os.path.join(db_folder, 'football_sim.db')

    
    conn = sqlite3.connect(db_path)
    return conn

def create_tables():
    conn = create_connection()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS teams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    skill_level INTEGER NOT NULL,
                    team_id INTEGER,
                    FOREIGN KEY (team_id) REFERENCES teams (id)
                )''')
    conn.commit()
    conn.close()

def save_team(team):
    conn = create_connection()
    c = conn.cursor()

    # Insert team
    c.execute('INSERT INTO teams (name) VALUES (?)', (team.name,))
    team_id = c.lastrowid

    # Insert players
    for player in team.roster:
        c.execute('INSERT INTO players (name, position, skill_level, team_id) VALUES (?, ?, ?, ?)',
                  (player.name, player.position, player.skill_level, team_id))

    conn.commit()
    conn.close()

def save_teams(teams):
    create_tables()
    for team in teams:
        save_team(team)

def load_teams():
    conn = create_connection()
    c = conn.cursor()

    c.execute('SELECT * FROM teams')
    team_rows = c.fetchall()

    teams = []
    for team_row in team_rows:
        team_id, team_name = team_row
        team = Team(team_name)

        c.execute('SELECT * FROM players WHERE team_id = ?', (team_id,))
        player_rows = c.fetchall()

        for player_row in player_rows:
            _, name, position, skill_level, _ = player_row
            player = Player(name, position, skill_level)
            team.add_player(player)

        teams.append(team)

    conn.close()
    return teams
