# functions for assigning rounds

def main():
    pass

def assign_rounds(list_of_dicts):
    """
    Assign rounds to each of the dictionaries in list_of_dicts by adding "Round number"
    and "Round name" keys along with the value determined for each

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Tournament," "Round robin tournament," "Winner", "Loser,"
        "Player 1," and "Player 2"

    Returns
    -------
    None.
    """
    
    # initialise variables
    start = 0
    end = None
    
    for i in range(1, len(list_of_dicts)):
        
        current_tournament = list_of_dicts[start]["Tournament"]
        
        # check if we have passed through all matches in the current tournament
        if list_of_dicts[i]["Tournament"] != current_tournament:
            end = i - 1
            
        # check if we have reached the last row in the data
        elif i == len(list_of_dicts) - 1:
            end = i
            
        # if either of the above happens, we know the start and end indices for
        # one whole tournament, and we can assign rounds
        if end != None:
            
            # calculate wins and losses
            wins_losses_dict = calculate_wins_losses(list_of_dicts, start, end)
            
            # assign rounds for a tournament with a round robin group stage
            if list_of_dicts[start]["Round robin tournament"]:
                assign_rounds_round_robin(list_of_dicts, start, end, wins_losses_dict)
                start = i
                end = None
                current_tournament = list_of_dicts[start]["Tournament"]
                continue
            
            # calculate some parameters for single elimination tournaments
            has_third_place_match = check_third_place_match(wins_losses_dict)
            num_players = len(wins_losses_dict)
            num_byes = number_of_byes(num_players)
            
            # assign rounds for a single elimination tournament with no byes or 
            # third place match
            if num_byes == 0 and not has_third_place_match:
                elimination_tournament_standard(list_of_dicts, start, end, wins_losses_dict)
                
            # assign rounds for a single elimination tournament with no byes but 
            # with a third place match
            elif num_byes == 0 and has_third_place_match:
                third_place_no_byes(list_of_dicts, start, end, wins_losses_dict)
            
            # assign rounds for a single elimination tournament with byes but no 
            # third place match
            elif num_byes > 0 and not has_third_place_match:
                num_matches_per_round = calc_num_matches_per_round(num_players)
                byes_no_third_place(list_of_dicts, start, end, wins_losses_dict, 
                        num_byes, num_matches_per_round)
            
            # assign rounds for a single elimination tournament with byes and a 
            # third place match
            elif num_byes > 0 and has_third_place_match:
                num_matches_per_round = calc_num_matches_per_round(num_players,
                                                                   has_third_place_match = True)
                byes_and_third_place(list_of_dicts, start, end, wins_losses_dict, 
                                     num_byes, num_matches_per_round)
            
            # reset start and end indices
            start = i
            end = None

def calculate_wins_losses(list_of_dicts, start, end):
    """
    Calculates the number of wins and losses for each player that played in a
    match in the list_of_dicts from the start index to the end index (inclusive).
    Returns a dictionary where each player name is a key and the corresponding
    value is a list of length two with number of wins at position 0 and number
    of losses at position 1.

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        List of dictionaries that all have a "Winner" key and a "Loser" key
    start : int
        An integer representing the index of the list_of_dicts at which to start
    end : int
        An integer representing the index of the list_of_dicts at which to end
        (inclusive)

    Returns
    -------
    wins_losses : dictionary
        dictionary with key: value pairs in the form of 
        "Player Name": [number of matches the player won, number of matches the player lost]
        for each player in the specified range of the given data
    """
    # initialise dictionary
    wins_losses = {}
    
    # add to the dictionary
    for i in range(start, end + 1):
        if list_of_dicts[i]["Winner"] in wins_losses.keys():
            wins_losses[list_of_dicts[i]["Winner"]][0] += 1
        else:
            wins_losses[list_of_dicts[i]["Winner"]] = [1, 0]
        if list_of_dicts[i]["Loser"] in wins_losses.keys():
            wins_losses[list_of_dicts[i]["Loser"]][1] += 1
        else:
            wins_losses[list_of_dicts[i]["Loser"]] = [0, 1]
    
    return wins_losses

def number_of_byes(num_players):
    """
    Calculates the number of byes awarded in a single elimination tournament
    based on the number of players that played in the tournament

    Parameters
    ----------
    num_players : int or float
        Positive whole number stored as an int or float representing the number
        of players that played in a tournament

    Returns
    -------
    int
        Number of players that would have need to get a bye in the tournament 
        based on the number players that played
    """
    
    count = 1
    number_of_players = num_players
    
    # check if a power of 2, and if not, what the next power of 2 is
    while number_of_players > 2:
        number_of_players /= 2
        count += 1
    
    # if the number of players is a power of 2, there are no byes
    if number_of_players == 2:
        return 0
    
    # if the number of players is not a power of 2, then the number of byes
    # awarded equals the difference between the number of players and the next
    # power of 2
    return 2 ** count - num_players

def calc_num_matches_per_round(num_players, has_third_place_match = False):
    """
    Calculates the number of matches that should have been played each round
    of a single elimination tournament (including those with byes and/or a 
    third place match). Returns the calculations as a list where each index i 
    holds the number of matches played in round number i + 1

    Parameters
    ----------
    num_players : int or float
        Positive whole number stored as an int or float

    Returns
    -------
    num_matches_per_round : list
        List of floats representing the number of matches played in each round 
        where a given round's number of matches is stored at index round number
        minus 1
    """
    
    num_matches_per_round = []
    num_byes = number_of_byes(num_players)
    # number of matches in the first round
    num_matches = (num_players - num_byes) / 2
    num_matches_per_round.append(num_matches)
    
    while num_matches > 1:
        if len(num_matches_per_round) > 1:
            # number of matches per round after the first two rounds
            num_matches /= 2
        else:
            # number of matches in the second round
            num_matches = (num_matches + num_byes) / 2
        num_matches_per_round.append(num_matches)
    
    assert num_matches == 1, "didn't get down to one match"
    
    # add a match in the last round if there is a third place match
    if has_third_place_match:
        num_matches_per_round[-1] += 1
    
    return num_matches_per_round

def check_third_place_match(wins_losses_dict):
    """
    Determines whether a third place match was played in a single elimination
    tournament
    
    Parameters
    ----------
    wins_losses_dict : dictionary
        dictionary with key: value pairs in the form of 
        "Player Name": [number of matches the player won, number of matches the player lost]
        for each player in a single elimination tournament

    Returns
    -------
    Boolean
        True if the a third place match was played in the tournament and False
        otherwise
    """
    # if someone lost twice
    return 2 in [wins_losses_dict[key][1] for key in wins_losses_dict.keys()]

def elimination_tournament_standard(list_of_dicts, start, end, wins_losses_dict):
    """
    Assigns rounds for a single elimination tournament with no byes or third
    place match. Modifies the list of dictionaries to include round numbers under 
    "Round number" keys and corresponding round names under "Round name" keys

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have "Loser" key
    start : int
        starting index of rows for matches in the current tournament
    end : int
        ending index (inclusive) of rows for matches in the current tournament
    wins_losses_dict : dictionary
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]

    Returns
    -------
    None.
    """
    
    number_rounds = max([sum(wins_losses_dict[player]) for player
                         in wins_losses_dict.keys()])
    
    # make list of players' last rounds
    players_last_rounds = [[] for i in range(number_rounds)]
    for player in wins_losses_dict.keys():
        players_last_rounds[sum(wins_losses_dict[player]) -1].append(player)
    
    round_names = get_round_names(number_rounds)
    
    # assign rounds based on players' last rounds
    for i in range(start, end + 1):
        for j in range(len(players_last_rounds)):
            if list_of_dicts[i]["Loser"] in players_last_rounds[j]:
                list_of_dicts[i]["Round number"] = j + 1
                list_of_dicts[i]["Round name"] = round_names[j + 1]
                break
            
def third_place_no_byes(list_of_dicts, start, end, wins_losses_dict):
    """
    Assigns rounds for a single elimination tournament that has a third place
    match but does not have byes. Modifies the list of dictionaries to include 
    round numbers under "Round number" keys and corresponding round names under
    "Round name" keys

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Loser" and "Start date"
    start : int
        starting index of rows for matches in the current tournament
    end : int
        ending index (inclusive) of rows for matches in the current tournament
    wins_losses_dict : dictionary
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]

    Returns
    -------
    None.
    """
    
    number_rounds =  max([sum(wins_losses_dict[player]) for player
                          in wins_losses_dict.keys()])
    
    # last rounds for players that were eliminated in or before the quarterfinals
    players_last_rounds = [[] for i in range(number_rounds - 2)]
    
    for player in wins_losses_dict.keys():
        # for players that didn't play in the last two rounds
        if sum(wins_losses_dict[player]) <= number_rounds - 2:
            players_last_rounds[sum(wins_losses_dict[player]) - 1].append(player)
    
    round_names = get_round_names(number_rounds)
    
    # keep list of indices of matches that did not happen in or before quarterfinals
    last_two_rounds = []
    
    # assign rounds for all but the last two rounds and keep list of matches
    # that happened in the last two rounds
    for i in range(start, end + 1):
        for j in range(len(players_last_rounds)):
            if list_of_dicts[i]["Loser"] in players_last_rounds[j]:
                list_of_dicts[i]["Round number"] = j + 1
                list_of_dicts[i]["Round name"] = round_names[j + 1]
                break
        if "Round number" not in list_of_dicts[i].keys():
            last_two_rounds.append(i)
    
    # last_two_rounds should have the indices for the two semifinals matches,
    # the third place match, and the final match
    assertion_msg = (str(len(last_two_rounds)) + " matches have been assigned" +
                     " to the last two rounds instead of 4 for the tournament " +
                     list_of_dicts[start]["Tournament"] + " with start date " +
                     str(list_of_dicts[start]["Start date"]))
    assert len(last_two_rounds) == 4, assertion_msg
    
    assign_last_rounds(list_of_dicts, wins_losses_dict, last_two_rounds, number_rounds)

def assign_last_rounds(list_of_dicts, wins_losses_dict, indices_of_last_matches,
                       number_rounds):
    """
    Assign the rounds to semifinals, final, and third place matches for tournaments
    with a third place match and no byes

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Winner," "Loser," "Tournament," and "Start date"
    wins_losses_dict : dicionary
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]
    indices_of_last_matches : list of non-negative ints
        the indices of list_of_dicts that have been identified as corresponding
        to a match in one of the last two rounds
    number_rounds : positive int
        number of rounds in the tournament

    Returns
    -------
    None.
    """
    
    # find champion and the person that lost the third place match
    lost_third_found = False
    champion_found = False
    for player in wins_losses_dict.keys():
        if wins_losses_dict[player][1] == 2:
            lost_third_place = player
            lost_third_found = True
        if wins_losses_dict[player][1] == 0:
            champion = player
            champion_found = True
        if lost_third_found and champion_found:
            break
    
    # rounds to assign and number of matches for each
    to_assign = {"Final": 1, "Third Place Match": 1, "Semifinals": 2}
    
    # find the champion's opponents from the rounds and be sure there are two of them
    champion_opponents = {list_of_dicts[index]["Loser"]: index for 
                          index in indices_of_last_matches if 
                          list_of_dicts[index]["Winner"] == champion}
    assertion_msg = ("Champion played " + str(len(champion_opponents)) +
                     " opponents in the last two rounds of " + 
                     list_of_dicts[indices_of_last_matches[0]]["Tournament"] + 
                     " with start date " + 
                     str(list_of_dicts[indices_of_last_matches[0]]["Start date"]))
    assert len(champion_opponents) == 2, assertion_msg
    
    # if the champion played the third place match loser, that match was a
    # semifinal and the champion's other match was the final
    if lost_third_place in champion_opponents.keys():
        semifinal1_index = champion_opponents[lost_third_place]
        list_of_dicts[semifinal1_index]["Round number"] = number_rounds - 1
        list_of_dicts[semifinal1_index]["Round name"] = "Semifinals"
        to_assign["Semifinals"] -= 1
        del champion_opponents[lost_third_place]
        final_index = list(champion_opponents.values())[0]
        list_of_dicts[final_index]["Round number"] = number_rounds
        list_of_dicts[final_index]["Round name"] = "Final"
        finalist = list_of_dicts[final_index]["Loser"]
        to_assign["Final"] -= 1
    else:
        # semifinal opponent and final opponent both won and lost the same
        # number of matches (or wins differ by 1 if one player had a bye), 
        # so differentiate based on ordering of the data
        semifinal1_index = min(champion_opponents.values())
        list_of_dicts[semifinal1_index]["Round number"] = number_rounds - 1
        list_of_dicts[semifinal1_index]["Round name"] = "Semifinals"
        to_assign["Semifinals"] -= 1
        final_index = max(champion_opponents.values())
        list_of_dicts[final_index]["Round number"] = number_rounds
        list_of_dicts[final_index]["Round name"] = "Final"
        finalist = list_of_dicts[final_index]["Loser"]
        to_assign["Final"] -= 1
    
    # assign rounds to the remaining semifinal and the third place match
    for index in indices_of_last_matches:
        if list_of_dicts[index]["Winner"] == finalist:
            list_of_dicts[index]["Round number"] = number_rounds - 1
            list_of_dicts[index]["Round name"] = "Semifinals"
            to_assign["Semifinals"] -= 1
        elif (list_of_dicts[index]["Loser"] == lost_third_place and 
              list_of_dicts[index]["Winner"] != champion): 
            list_of_dicts[index]["Round number"] = number_rounds
            list_of_dicts[index]["Round name"] = "Third Place Match"
            to_assign["Third Place Match"] -= 1
    
    # be sure two semifinals, one final, and one third place match have been assigned
    assertion_msg = ("incorrect distribution of rounds assigned for the last " +
                     "two rounds in the tournament" + 
                     list_of_dicts[indices_of_last_matches[0]]["Tournament"] + 
                     " with start date " + 
                     str(list_of_dicts[indices_of_last_matches[0]]["Start date"]) +
                     "; set of the number of remaining matches was supposed to " +
                     "be {0}, but it is " + str(set(to_assign.values())))
    assert set(to_assign.values()) == {0}
        
def byes_no_third_place(list_of_dicts, start, end, wins_losses_dict, 
                        number_of_byes, num_matches_per_round):
    """
    Assigns rounds to matches in tournaments that have byes but no third palce
    match

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Winner," "Loser," "Tournament," and "Start date"
    start : positive int
        index of list_of_dicts of the first match in the current tournament
    end : positive int
        index of list_of_dicts of the last match in the current tournament
    wins_losses_dict : dict
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]
    number_of_byes : positive int
        number of byes given in the tournament
    num_matches_per_round : list of ints
        number of matches that take place in each round, stored in the list at
        index round - 1

    Returns
    -------
    None.
    """
    
    # get number of rounds
    num_rounds = len(num_matches_per_round)
    # initialise a list of lists to hold people eliminated in each round
    players_last_rounds = [[] for i in range(num_rounds)]
    # keep list of players given byes
    players_awarded_byes = []
    
    # find the tournament champion, the player with 0 losses
    for key in wins_losses_dict.keys():
        if wins_losses_dict[key][1] == 0:
            champion = key
            break
    players_last_rounds[num_rounds - 1].append(champion)
    assign_final_for_champion = True
    
    # assign rounds until all matches have been assigned a round
    while sum(num_matches_per_round) != 0:
        for i in range(num_rounds, 0, -1):
            if len(players_last_rounds[i - 1]) != 0:
                player_to_examine = players_last_rounds[i - 1].pop()
                player_last_round = i
                break
        # get the last rounds of the current player's opponents and any players
        # assigned byes while assinging the round's of the current player's matches
        opponents_last_rounds, players_with_byes = assign_rounds_byes(list_of_dicts, 
                                                                      start, end,
                                                                      player_to_examine,
                                                                      wins_losses_dict,
                                                                      player_last_round,
                                                                      assign_final_for_champion)
        assign_final_for_champion = False

        # add the people eliminated to the last rounds list indicating which
        # round they were eliminated in; update the number of matches still to
        # be assigned to each round
        for opponent, last_round in opponents_last_rounds.items():
            players_last_rounds[last_round - 1].append(opponent)
            num_matches_per_round[last_round - 1] -= 1
            assertion_msg = ("too many matches assigned to round " + str(last_round) +
                             " for tournament " + list_of_dicts[start]["Tournament"] +
                             " With start date " + str(list_of_dicts[start]["Start date"]))
            assert num_matches_per_round[last_round - 1] >= 0, assertion_msg
            
        # add new players with byes to the list
        players_awarded_byes.extend(players_with_byes)
        assertion_msg = ("too many byes awarded in " + list_of_dicts[start]["Tournament"] +
                         " starting " + str(list_of_dicts[start]["Start date"]))
        assert len(players_awarded_byes) <= number_of_byes, assertion_msg
    
    # map the round numbers to round names
    round_names = get_round_names(num_rounds)
    for i in range(start, end + 1):
        list_of_dicts[i]["Round name"] = round_names[list_of_dicts[i]["Round number"]]

def assign_rounds_byes(list_of_dicts, start, end, player_name, wins_losses_dict,
                       player_last_round, assign_final_for_champion):
    """
    Assigns rounds for a player in a single elimination tournament with byes

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Winner" and "Loser"
    start : positive int
        index of list_of_dicts of the first match in the tournament
    end : positive int
        index of list_of_dicts of the last match in the tournament
    player_name : string
        name of the player whose rounds are to be assigned
    wins_losses_dict : dict
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]
    player_last_round : int
        the round number of the last round the player has had assigned so far
    assign_final_for_champion : Boolean
        whether the round still needs to be assigned for the final match

    Returns
    -------
    opponents_top_rounds : dictionary
        dictionary with key: value pairs of opponent name: their last round in
        the tournament
    players_awarded_byes : list of strings
        list of the names of the players awarded byes
    """
    # list of the match's index in the data and list of the number of matches 
    # played by the player beaten in that match
    indices_of_matches = []
    opponents_num_matches = []
    opponents_top_rounds = {}
    
    # players awarded byes while looking at matches of current player
    players_awarded_byes = []
    
    # find the current player's matches that have not been assigned rounds
    for i in range(start, end + 1):
        if (list_of_dicts[i]["Winner"] == player_name and "Round number" not in
            list_of_dicts[i].keys()):
            beaten_player = list_of_dicts[i]["Loser"]
            indices_of_matches.append(i)
            opponents_num_matches.append(sum(wins_losses_dict[beaten_player]))
    
    number_matches_won = len(indices_of_matches)
    
    if not assign_final_for_champion:
        # their highest round was already assigned when they lost
        rounds_to_assign = range(player_last_round - 1, 
                                 player_last_round - 1 - number_matches_won, -1)
    else:
        # highest round still needs to be assigned
        rounds_to_assign = range(player_last_round, 
                                 player_last_round - number_matches_won, -1)
    
    for i in rounds_to_assign:
        
        # one of the player's opponents played as many matches as the current
        # round number
        if i in opponents_num_matches:
            position = opponents_num_matches.index(i)
            current_round_index = indices_of_matches[position]
            bye_awarded = False
        
        # none of the opponents played in every round up until current round
        else:
            possible_match_indices = [indices_of_matches[j] for j in 
                                      range(len(opponents_num_matches)) if 
                                      opponents_num_matches[j] == i - 1]
            current_round_index = max(possible_match_indices)
            position = indices_of_matches.index(current_round_index)
            bye_awarded = True
        
        # assign round and keep track of eliminated player's name and round
        list_of_dicts[current_round_index]["Round number"] = i
        eliminated = list_of_dicts[current_round_index]["Loser"]
        opponents_top_rounds[eliminated] = i
        
        if bye_awarded:
            players_awarded_byes.append(eliminated)
            
        del indices_of_matches[position]
        del opponents_num_matches[position]
    
    return opponents_top_rounds, players_awarded_byes

def byes_and_third_place(list_of_dicts, start, end, wins_losses_dict, 
                         number_of_byes, num_matches_per_round):
    """
    Assign rounds to matches in single elimination tournaments with byes and
    a third place match

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Winner," "Loser," "Player 1," "Player 2," "Tournament," and
        "Start date"
    start : positive int
        index of list_of_dicts of the first match in the tournament
    end : positive int
        index of list_of_dicts of the last match in the tournament
    wins_losses_dict : dict
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]
    number_of_byes : positive int
        number of byes awarded in the tournament
    num_matches_per_round : list of ints
        number of matches that take place in each round, stored in the list at
        index round - 1

    Returns
    -------
    None.
    """
    # get number of rounds
    num_rounds = len(num_matches_per_round)
    # initialise a list of lists to hold people's current lowest round assigned
    current_rounds_assigned = [[] for i in range(num_rounds)]
    # keep list of players given byes
    players_awarded_byes = []
    
    top_four, byes = assign_last_rounds_byes(list_of_dicts, start, end,
                                            wins_losses_dict, num_matches_per_round)
    
    # update variables after assigning rounds to last two rounds
    current_rounds_assigned[-2].extend(top_four)
    players_awarded_byes.extend(byes)
    num_matches_per_round[-1] -= 2
    num_matches_per_round[-2] -= 2
    
    # assign rounds until all matches have been assigned a round
    while sum(num_matches_per_round) != 0:
        for i in range(num_rounds, 0, -1):
            if len(current_rounds_assigned[i - 1]) != 0:
                player_to_examine = current_rounds_assigned[i - 1].pop()
                current_round_assigned = i
                break
        # get the last rounds of the current player's opponents and any players
        # assigned byes while assinging the round's of the current player's matches
        opponents_last_rounds, players_with_byes = assign_rounds_byes(list_of_dicts, 
                                                                      start, end,
                                                                      player_to_examine,
                                                                      wins_losses_dict,
                                                                      current_round_assigned,
                                                                      False)
        
        # add the people eliminated to the last rounds list indicating which
        # round they were eliminated in; update the number of matches still to
        # be assigned to each round
        for opponent, last_round in opponents_last_rounds.items():
            current_rounds_assigned[last_round - 1].append(opponent)
            num_matches_per_round[last_round - 1] -= 1
            assertion_msg = ("too many matches assigned to round " + str(last_round) +
                             " for tournament " + list_of_dicts[start]["Tournament"] +
                             " With start date " + str(list_of_dicts[start]["Start date"]))
            assert num_matches_per_round[last_round - 1] >= 0, assertion_msg
            
        # add new players with byes to the list
        players_awarded_byes.extend(players_with_byes)
        assertion_msg = ("too many byes awarded in " + list_of_dicts[start]["Tournament"] +
                         " starting " + str(list_of_dicts[start]["Start date"]))
        assert len(players_awarded_byes) <= number_of_byes, assertion_msg
    
    # map the round numbers to round names
    round_names = get_round_names(num_rounds)
    for i in range(start, end + 1):
        if "Round name" not in list_of_dicts[i].keys():
            list_of_dicts[i]["Round name"] = round_names[list_of_dicts[i]["Round number"]]

def assign_last_rounds_byes(list_of_dicts, start, end, wins_losses_dict,
                            num_matches_per_round):
    """
    Assigns rounds for semifinals, final, and third place matches for tournaments
    with byes and a third place match

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Player 1," "Player 2," "Tournament," and
        "Start date"
    start : positive int
        index of list_of_dicts of the first match in the tournament
    end : positive int
        index of list_of_dicts of the last match in the tournament
    wins_losses_dict : dict
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]
    num_matches_per_round : list of ints
        number of matches that take place in each round, stored in the list at
        index round - 1

    Returns
    -------
    top_four_finishers : list of strings
        list of the names of players that played in semifinals and then a final
        or third place match
    players_given_byes : list of strings
        list of the names of players that were awarded byes while assigning
        the last two rounds
    """
    
    number_rounds = len(num_matches_per_round)
    last_matches_indices = []
    players_given_byes = []
    top_four_finishers = []
    
    # anyone that got to the semifinals, also played in the next round, and, 
    # therefore played a total number of matches at least equal to the number
    # of rounds minus 1; no one else would have
    for i in range(start, end + 1):
        player1 = list_of_dicts[i]["Player 1"]
        player2 = list_of_dicts[i]["Player 2"]
        if ((sum(wins_losses_dict[player1]) == number_rounds or
            sum(wins_losses_dict[player1]) == number_rounds - 1) and
            (sum(wins_losses_dict[player2]) == number_rounds or
            sum(wins_losses_dict[player2]) == number_rounds - 1)):
            last_matches_indices.append(i)
            if (sum(wins_losses_dict[player1]) == number_rounds - 1 and
                player1 not in players_given_byes):
                players_given_byes.append(player1)
            if (sum(wins_losses_dict[player2]) == number_rounds - 1 and
                player2 not in players_given_byes):
                players_given_byes.append(player2)
            if player1 not in top_four_finishers:
                top_four_finishers.append(player1)
            if player2 not in top_four_finishers:
                top_four_finishers.append(player2)
    
    assertion_msg = ("There were " + str(len(last_matches_indices)) + " matches " +
                     "between people that played number_rounds or number_rounds - 1 " +
                     "matches, not four in " + list_of_dicts[start]["Tournament"] + 
                     " with start date " + str(list_of_dicts[start]["Start date"]))
    assert len(last_matches_indices) == 4, assertion_msg
    
    assign_last_rounds(list_of_dicts, wins_losses_dict, last_matches_indices,
                       number_rounds)
    
    return top_four_finishers, players_given_byes

def assign_rounds_round_robin(list_of_dicts, start, end, wins_losses_dict):
    """
    Assigns rounds to matches in tournaments with a round robin group stage

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "Player 1," "Player 2," "Tournament," and
        "Start date"
    start : positive int
        index of list_of_dicts of the first match in the tournament
    end : positive int
        index of list_of_dicts of the last match in the tournament
    wins_losses_dict : dict
        dictionary of the number of wins and losses for each player with 
        key: value pairs in the form of player name: [number of wins, number of losses]

    Returns
    -------
    None.
    """
    
    max_matches = max([sum(record) for record in wins_losses_dict.values()])
    
    finalists = [player for player in wins_losses_dict.keys() if 
                 sum(wins_losses_dict[player]) == max_matches]
    
    # there should be two players that played this many matches
    assertion_msg = (str(len(finalists)) + " played the maximum number of matches " +
                     "not two in the round robin tournament " +
                     list_of_dicts[start]["Tournament"] + " with start date " +
                     str(list_of_dicts[start]["Start date"]))
    assert len(finalists) == 2, assertion_msg
    
    # get the index(es) of the match(es) in which the finalists played against 
    # each other
    indices_matches_between_finalists = []
    for i in range(start, end + 1):
        if (list_of_dicts[i]["Player 1"] in finalists and 
            list_of_dicts[i]["Player 2"] in finalists):
            indices_matches_between_finalists.append(i)
    
    if len(indices_matches_between_finalists) == 1:
        # that match is the final
        final_index = indices_matches_between_finalists[0]
    else:
        # they played each other twice, so differentiate based on the order of 
        # the data
        max_index = max(indices_matches_between_finalists)
        final_index = indices_matches_between_finalists.index(max_index)
        
    # assign the round to the final
    list_of_dicts[final_index]["Round number"] = 3
    list_of_dicts[final_index]["Round name"] = "Final"
    
    # get opponents and indices of matches that may be semifinals
    finalist1_potential_semis = {}
    finalist2_potential_semis = {}
    for i in range(start, end + 1):
        if (list_of_dicts[i]["Winner"] == finalists[0] and 
            sum(wins_losses_dict[list_of_dicts[i]["Loser"]]) == max_matches - 1):
            finalist1_potential_semis[list_of_dicts[i]["Loser"]] = i
        elif (list_of_dicts[i]["Winner"] == finalists[1] and 
            sum(wins_losses_dict[list_of_dicts[i]["Loser"]]) == max_matches - 1):
            finalist2_potential_semis[list_of_dicts[i]["Loser"]] = i
    
    # check if either only has one possibility
    if len(finalist1_potential_semis) == 1:
        semi1_index = list(finalist1_potential_semis.values())[0]
        list_of_dicts[semi1_index]["Round number"] = 2
        list_of_dicts[semi1_index]["Round name"] = "Semifinals"
        finalist1_semi_found = True
        if list_of_dicts[semi1_index]["Loser"] in finalist2_potential_semis.keys():
            del finalist2_potential_semis[list_of_dicts[semi1_index]["Loser"]]
    else:
        finalist1_semi_found = False
        
    if len(finalist2_potential_semis) == 1:
        semi2_index = list(finalist2_potential_semis.values())[0]
        list_of_dicts[semi2_index]["Round number"] = 2
        list_of_dicts[semi2_index]["Round name"] = "Semifinals"
        finalist2_semi_found = True
        if list_of_dicts[semi2_index]["Loser"] in finalist1_potential_semis.keys():
            del finalist1_potential_semis[list_of_dicts[semi2_index]["Loser"]]
    else:
        finalist2_semi_found = False
    
    # check finalist 1 again after a possibility may have been deleted
    if not finalist1_semi_found and len(finalist1_potential_semis) == 1:
        semi1_index = list(finalist1_potential_semis.values())[0]
        list_of_dicts[semi1_index]["Round number"] = 2
        list_of_dicts[semi1_index]["Round name"] = "Semifinals"
        finalist1_semi_found = True
    
    # assign based on order of the data if semis still have not been identified
    if not finalist1_semi_found:
        semi1_index = max(finalist1_potential_semis.values())
        list_of_dicts[semi1_index]["Round number"] = 2
        list_of_dicts[semi1_index]["Round name"] = "Semifinals"
    if not finalist2_semi_found:
        semi2_index = max(finalist2_potential_semis.values())
        list_of_dicts[semi2_index]["Round number"] = 2
        list_of_dicts[semi2_index]["Round name"] = "Semifinals"
    
    # assign the rest of the matches to round 1, the round robin group stage
    for i in range(start, end + 1):
        if "Round number" not in list_of_dicts[i].keys():
            list_of_dicts[i]["Round number"] = 1
            list_of_dicts[i]["Round name"] = "Round Robin"

def get_round_names(number_of_rounds):
    """
    Creates a dictionary that maps round numbers to names for single elimination
    tournaments that do not have a third place match.
    
    Parameters
    ----------
    number_of_rounds : non-negative integer
        number of rounds in a single elimination tournament with no third place
        match

    Returns
    -------
    round_names : dictionary
        dictionary with round numbers as keys and their corresponding names as 
        values
    """
    ordinal_number_terms = ["First Round", "Second Round", "Third Round",
                            "Fourth Round", "Fifth Round", "Sixth Round",
                            "Seventh Round", "Eighth Round", "Ninth Round",
                            "Tenth Round"]
    finals_terms = ["Final", "Semifinals", "Quarterfinals"]
    
    round_names = {}
    
    for i in range(number_of_rounds):
        # last three rounds
        if i <= 2:
            round_names[number_of_rounds - i] = finals_terms[i]
        # rounds before the last three
        else:
            round_names[number_of_rounds - i] = ordinal_number_terms[number_of_rounds - i - 1]
    
    return round_names

if __name__ == "__main__":
    main()