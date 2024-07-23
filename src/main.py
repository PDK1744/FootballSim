from team import generate_teams

def main():
    teams = generate_teams(num_teams=24, num_players_per_team=24)
    for team in teams:
        print(team)
        for player in team.roster:
            print(f"  {player}")

if __name__ == "__main__":
    main()
