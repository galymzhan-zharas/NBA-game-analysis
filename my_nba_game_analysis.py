import re
import csv 

def loader(file_name):
    play_by_play_moves = []
    with open(file_name, "r") as file:
        reader_object = csv.reader(file, delimiter='|')
        # reader_object contains arrays of rows
        # 'each' is an array containing first row elements
        play_by_play_moves = [each for each in reader_object]
    return play_by_play_moves

def player_index(result, team_players, player, action=0):
    if player not in team_players:
        #if action and player == "K. Durant":
            #print("{} is NOT found".format(player))
        profile = {"player_name": player, "FG": 0, "FGA": 0, "FG%": 0, "3P": 0, "3PA": 0, "3P%": 0, "FT": 0, "FTA": 0, "FT%": 0, "ORB": 0, "DRB": 0, "TRB": 0, "AST": 0, "STL": 0, "BLK": 0, "TOV": 0, "PF": 0, "PTS": 0}
        result.append(profile)
        team_players[player] = len(result) - 1
    #elif player in team_players and action and player == "K. Durant":
        #print("{} IS found".format(player))
    #print(team_players.keys())
    return team_players[player]

def statistics(play_by_play_moves, team):
    result = [] # array of dictionaries: each dictionary is to contain the player name and relevant scores

    # the pair : 
        # key : a string, a player name
        # value : the location of his profile information in the array 'result' 
        # I want to store this to retrieve and modify the relevant profile information 

    team_players = dict()
    # identifying their actions 
    for play in play_by_play_moves:
        action = play[-1]
        name = re.search(r"(\w\. \w+)", action)
        two_pt = re.search(r"(\w\. \w+) makes 2-pt", action) # select the first person who performs the action
        two_pt_at = re.search(r"(\w\. \w+) misses 2-pt", action)
        three_pt = re.search(r"(\w\. \w+) makes 3-pt", action)
        three_pt_at = re.search(r"(\w\. \w+) misses 3-pt", action)
        free_throw = re.search(r"(\w\. \w+) makes free throw", action)
        free_throw_clear = re.search(r"(\w\. \w+) makes clear path free throw", action)
        free_throw_at = re.search(r"(\w\. \w+) misses free throw", action)
        free_throw_clear_at = re.search(r"(\w\. \w+) misses clear path free throw", action)
        def_reb = re.search(r"Defensive rebound by (\w\. \w+)", action)
        off_reb = re.search(r"Offensive rebound by (\w\. \w+)", action)
        assists = re.search(r"(assist by) (\w\. \w+)", action)
        turnover = re.search(r"Turnover by (\w\. \w+)", action)
        steal = re.search(r"(steal by) (\w\. \w+)", action)
        block = re.search(r"(block by) (\w\. \w+)", action)
        foul = re.search(r"foul by (\w\. \w+)", action) 
           
        #shooting_foul = re.search(r"Shooting foul by (\w\. \w+)", action) 

        # if a player performs an action worth 2 points AND the person belongs to our team (relevant team == team)...

        if two_pt and play[2] == team:
            index = player_index(result, team_players, two_pt.group(1))
            result[index]["FG"] += 1
            result[index]["FGA"] += 1
            result[index]["PTS"] += 2

        if two_pt_at and play[2] == team: 
            index = player_index(result, team_players, two_pt_at.group(1))
            result[index]["FGA"] += 1

        if three_pt and play[2] == team:
            index = player_index(result, team_players, three_pt.group(1))
            result[index]["3P"] += 1
            result[index]["3PA"] += 1
            result[index]["FG"] += 1
            result[index]["FGA"] += 1
            result[index]["PTS"] += 3

        if three_pt_at and play[2] == team:
            index = player_index(result, team_players, three_pt_at.group(1))
            result[index]["3PA"] += 1
            result[index]["FGA"] += 1

        if free_throw and play[2] == team:
            index = player_index(result, team_players, free_throw.group(1))
            result[index]["FT"] += 1
            result[index]["FTA"] += 1
            result[index]["PTS"] += 1

        if free_throw_clear and play[2] == team:
            index = player_index(result, team_players, free_throw_clear.group(1))
            result[index]["FT"] += 1
            result[index]["FTA"] += 1
            result[index]["PTS"] += 1

        if free_throw_at and play[2] == team:
            index = player_index(result, team_players, free_throw_at.group(1))
            result[index]["FTA"] += 1

        if free_throw_clear_at and play[2] == team:
            index = player_index(result, team_players, free_throw_clear_at.group(1))
            result[index]["FTA"] += 1

        if def_reb and play[2] == team: 
            index = player_index(result, team_players, def_reb.group(1))
            result[index]["DRB"] += 1
            result[index]["TRB"] += 1

        if off_reb and play[2] == team: 
            index = player_index(result, team_players, off_reb.group(1))
            result[index]["ORB"] += 1
            result[index]["TRB"] += 1

        if foul:
            #different types of fouls add scores differently
            # shooting foul; personal foul; loose ball foul; offensive foul; clear path foul; 
            
            # personal foul     by X drawn by Y,   Y -> relevant team 
            # shooting foul     by X drawn by Y,   Y -> relevant team 
            # clear path foul   by X,              Y -> relevant team

            # offensive foul    by X drawn by Y,   X -> relevant team 
            # loose ball foul   by X drawn by Y,   X -> relevant team

            # PF's are given to X's 
            if re.search(r"Personal foul", action) or re.search(r"Shooting foul", action) or re.search(r"Clear path foul", action) :
                if play[2] != team: 
                    index = player_index(result, team_players, foul.group(1))
                    result[index]["PF"] += 1
            else: 
                # for offensive and loose ball foul
                if play[2] == team: 
                    index = player_index(result, team_players, foul.group(1))
                    result[index]["PF"] += 1

        if turnover and play[2] == team: 
            index = player_index(result, team_players, turnover.group(1))
            result[index]["TOV"] += 1

        if assists and play[2] == team:
            index = player_index(result, team_players, assists.group(2))
            result[index]['AST'] += 1
        # the one who steals belongs to our team
        if steal and play[2] != team:
            index = player_index(result, team_players, steal.group(2))
            result[index]['STL'] += 1

        if block and play[2] != team:
            index = player_index(result, team_players, block.group(2))
            result[index]['BLK'] += 1
        
    for profile in result: 
        try: 
            #profile['FG%'] = profile['FG']/profile['FGA']
            profile['FG%'] = float("{:.3f}".format(profile['FG']/profile['FGA']))
        except ZeroDivisionError:
            profile['FG%'] = 0

        try: 
            profile['3P%'] = float("{:.3f}".format(profile['3P']/profile['3PA']))
        except ZeroDivisionError: 
            profile['3P%'] = 0

        try: 
            profile['FT%'] = float("{:.3f}".format(profile['FT']/profile['FTA']))
        except ZeroDivisionError: 
            profile['FT%'] = 0

    return result

            
def analyse_nba_game(play_by_play_moves):
    home_team_data = statistics(play_by_play_moves, play_by_play_moves[0][4])
    away_team_data = statistics(play_by_play_moves, play_by_play_moves[0][3])

    updated_data = {"home_team": {"name": play_by_play_moves[0][4], "players_data": home_team_data}, "away_team": {"name": play_by_play_moves[0][3], "players_data": away_team_data}}
    return updated_data

def print_table(dict_data):
    keys = ["player_name", "FG", "FGA", "FG%", "3P", "3PA", "3P%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK", "TOV", "PF", "PTS"]
    total_points = [0]*(len(keys)-1)
    
    print(*keys, sep='\t')
    print()
    for profile in dict_data:
        print(*profile.values(), sep='\t')
        total_points = [i+j for i, j in zip(total_points, list(profile.values())[1:])]
        print()

    # FG% = FG/FGA
    total_points[2] = float("{:.3f}".format(total_points[0]/total_points[1]))
    # 3P% = 3P/3PA
    total_points[5] = float("{:.3f}".format(total_points[3]/total_points[4]))
    # FT% = FT / FTA
    total_points[8] = float("{:.3f}".format(total_points[6]/total_points[7]))

    print("Team Totals", end='\t')
    print(*total_points, sep='\t')

#reformats team_dict
def print_nba_game_stats(team_dict):
    #team_dict contains the summary of both teams performance. 
    #access the value 'DATA' of each team
    home_team_data = team_dict["home_team"]["players_data"]
    away_team_data = team_dict["away_team"]["players_data"]
    # home_team_data and away_team_data are lists of dictionaries representing each player
    # home_team_data[0] is the first dictionary
    print_table(home_team_data)
    print("\n")
    print_table(away_team_data)

def _main():
    play_by_play_moves = loader("nba_game_warriors_thunder_20181016.txt")
    dictionary = analyse_nba_game(play_by_play_moves)
    print_nba_game_stats(dictionary)

_main()