import sqlite3
import os
from player import Player
from team import Team

def create_connection():
    try:
        # Define path for database folder
        db_folder = os.path.join('..', 'data')
        db_path = os.path.join(db_folder, 'football_sim.db')
        # Create folder if it doesn't exist
        if not os.path.exists(db_folder):
            os.makedirs(db_folder)

        conn = sqlite3.connect(db_path)
        return conn
    except Exception as e:
        print(f"Error creating connection to the database: {e}")
        raise

def create_tables():
    db_path = os.path.join('..', 'data', 'football_sim.db')

    if not os.path.exists(db_path):
        try:
            conn = create_connection()
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS conferences (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL)''')

            c.execute('''CREATE TABLE IF NOT EXISTS teams (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            power_level INTEGER,
                            conference_id INTEGER,
                            FOREIGN KEY (conference_id) REFERENCES conferences(id)
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
            print("Database created and tables initialized.")
            return True  # Indicate that the tables were created
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise
    else:
        print("Database already exists. Skipping table creation.")
        return False  # Indicate that the tables were not created

def create_conferences():
    try:
        conn = create_connection()
        c = conn.cursor()

        conferences = [f"Conference {chr(65 + i)}" for i in range(8)]
        for conf in conferences:
            c.execute('INSERT INTO conferences (name) VALUES (?)', (conf,))

        conn.commit()
        conn.close()
        print("Conferences have been created.")
    except Exception as e:
        print(f"Error creating conferences: {e}")
        raise

def save_team(team):
    conn = create_connection()
    c = conn.cursor()

    # Insert team
    c.execute('INSERT INTO teams (name, power_level, conference_id) VALUES (?, ?, ?)', (team.name, team.power_level, team.conference_id))
    team_id = c.lastrowid

    # Insert players
    for player in team.roster:
        c.execute('INSERT INTO players (name, position, skill_level, team_id) VALUES (?, ?, ?, ?)',
                  (player.name, player.position, player.skill_level, team_id))

    conn.commit()
    conn.close()

def assign_teams_to_conferences(teams):
    try:
        conn = create_connection()
        c = conn.cursor()

        c.execute('SELECT * FROM conferences')
        conference_rows = c.fetchall()

        if not conference_rows:
            print("No conferences found. Cannot assign teams.")
            return

        conference_ids = [row[0] for row in conference_rows]

        if not conference_ids:
            print("Conference IDs list is empty.")
            return

        conference_index = 0
        num_conferences = len(conference_ids)

        for team in teams:
            conference_id = conference_ids[conference_index]
            c.execute('UPDATE teams SET conference_id = ? WHERE id = ?', (conference_id, team.id))

            conference_index = (conference_index + 1) % num_conferences

        conn.commit()
        conn.close()
        print("Teams have been assigned to conferences.")
    except Exception as e:
        print(f"Error assigning teams to conferences: {e}")
        raise

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
        team_id, team_name, power_level, conference_id = team_row
        team = Team(team_name, team_id)
        team.power_level = power_level
        team.conference_id = conference_id

        c.execute('SELECT * FROM players WHERE team_id = ?', (team_id,))
        player_rows = c.fetchall()

        for player_row in player_rows:
            _, name, position, skill_level, _ = player_row
            player = Player(name, position, skill_level)
            team.add_player(player)

        teams.append(team)

    conn.close()
    return teams

def view_all_teams():
    try:
        conn = create_connection()
        c = conn.cursor()

        # Retrieve teams
        c.execute('SELECT * FROM teams')
        team_rows = c.fetchall()

        for team_row in team_rows:
            team_id, team_name, power_level, conference_id = team_row
            c.execute('SELECT name FROM conferences WHERE id = ?', (conference_id,))
            conference_name = c.fetchone()[0]
            print(f"Team: {team_name} | Power Level: {power_level} | Conference: {conference_name}")

            # Retrieve players
            c.execute('SELECT * FROM players WHERE team_id = ?', (team_id,))
            player_rows = c.fetchall()

            for player_row in player_rows:
                _, name, position, skill_level, _ = player_row
                print(f" Player: {name} Position: {position} Skill Level: {skill_level}")

            print()

        conn.close()
    except Exception as e:
        print(f"Error retrieving team rosters: {e}")
        raise
