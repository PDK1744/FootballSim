from team import generate_teams
from database import save_teams, load_teams

def main():
    # Generate teams
    teams = generate_teams(num_teams=24, num_players_per_team=24)

    # Save teams to the database
    save_teams(teams)

    # Load teams from the database
    loaded_teams = load_teams()

    # Print loaded teams to verify
    for team in loaded_teams:
        print(team)
        for player in team.roster:
            print(f"  {player}")

if __name__ == "__main__":
    main()
