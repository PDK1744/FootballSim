from team import generate_teams
from database import (
    assign_teams_to_conferences,
    save_teams,
    load_teams,
    create_tables,
    create_conferences
)

def main():
    # Generate teams
    teams = generate_teams(num_teams=24, num_players_per_team=24)

    # Check if the database and tables need to be created
    if create_tables():  # Only create tables if the database does not already exist
        print("Saving new teams to the database.")
        save_teams(teams)
        # Create conferences if the database was just created
        create_conferences()
    else:
        print("Database already exists. No new teams will be saved.")

    # Assign teams to conferences
    assign_teams_to_conferences(teams)

    # Load teams from the database
    loaded_teams = load_teams()

    # Print loaded teams to verify
    for team in loaded_teams:
        print(team)
        for player in team.roster:
            print(f"  {player}")

if __name__ == "__main__":
    main()
