from team import generate_teams
from database import save_teams, load_teams, create_tables

def main():
    # Generate teams
    teams = generate_teams(num_teams=1, num_players_per_team=24)

    # Check if the database needs to be created
    if create_tables():  # Only create tables if the database does not already exist
        print("Saving new teams to the database.")
        save_teams(teams)
    else:
        print("Database already exists. No new teams will be saved.")

    # Load teams from the database
    loaded_teams = load_teams()

    # Print loaded teams to verify
    for team in loaded_teams:
        print(team)
        for player in team.roster:
            print(f"  {player}")

if __name__ == "__main__":
    main()
