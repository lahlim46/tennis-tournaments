# functions for creating rankings

import rounds
import math
from datetime import timedelta

def main():
    pass

def get_win_rankings_year(list_of_dicts, year):
    """
    Ranks players that played in one year by number of wins, with rank #1 being
    the player with the most wins

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "End date," "Winner," and "Loser"
    year : int
        the year for which you want rankings

    Returns
    -------
    list of tuples
        list of (player, rank) tuples sorted in reverse order by rank
    """
    applicable_data = [dic for dic in list_of_dicts if dic["End date"].year == year]
    wins_losses_dict = rounds.calculate_wins_losses(applicable_data, 0,
                                                    len(applicable_data) - 1)
    return sorted([(player, wins_losses_dict[player][0]) for 
            player in wins_losses_dict], key = lambda tup: tup[1], reverse = True)

def get_win_rankings_years(list_of_dicts, years):
    """
    Ranks players that played over a range of years by cummulative number of wins
    over the years, with rank #1 being the player with the most wins

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "End date," "Winner," and "Loser"
    years : an iterable type holding integers
        the range of years for which you want rankings

    Returns
    -------
    list of tuples
        list of (player, rank) tuples sorted in reverse order by rank
    """
    applicable_data = [dic for dic in list_of_dicts if dic["End date"].year in years]
    wins_losses_dict = rounds.calculate_wins_losses(applicable_data, 0,
                                                    len(applicable_data) - 1)
    return sorted([(player, wins_losses_dict[player][0]) for 
            player in wins_losses_dict], key = lambda tup: tup[1], reverse = True)
    
def get_win_rankings_all(list_of_dicts):
    """
    Ranks the players in all of the data in list_of_dicts by cumulative number 
    of wins over the years, with rank #1 being the player with the most wins

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "End date," "Winner," and "Loser"

    Returns
    -------
    list of tuples
        list of (player, rank) tuples sorted in reverse order by rank
    """
    wins_losses_dict = rounds.calculate_wins_losses(list_of_dicts, 0,
                                                    len(list_of_dicts) - 1)
    return sorted([(player, wins_losses_dict[player][0]) for 
            player in wins_losses_dict], key = lambda tup: tup[1], reverse = True)

def calculate_loss_penalty_scores(list_of_dicts):
    """
    Calculates scores for players based on match results and the match round numbers

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "Winner," "Loser," and "Round number"

    Returns
    -------
    scores : dictionary
        dictionary with key: value pairs of player: score
    """
    
    scores = {}
    
    for i in range(len(list_of_dicts)):
        if list_of_dicts[i]["Winner"] in scores.keys():
            scores[list_of_dicts[i]["Winner"]] += list_of_dicts[i]["Round number"]
        else:
            scores[list_of_dicts[i]["Winner"]] = list_of_dicts[i]["Round number"]
        if list_of_dicts[i]["Loser"] in scores.keys():
            scores[list_of_dicts[i]["Loser"]] -= 1 / list_of_dicts[i]["Round number"]
        else:
            scores[list_of_dicts[i]["Loser"]] = -1 / list_of_dicts[i]["Round number"]
    
    return scores

def loss_penalty_ranking_year(list_of_dicts, year):
    """
    Ranks the players that played in one year by scores based on their match
    results and round numbers of those matches. Rank #1 is the highest score (the
    best player)

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "End date," "Winner," "Loser," and "Round number"
    year : int
        the year for which to make rankings

    Returns
    -------
    list of tuples
        list of (player, rank) tuples sorted in reverse order by rank
    """
    applicable_data = [dic for dic in list_of_dicts if dic["End date"].year == year]
    scores_dict = calculate_loss_penalty_scores(applicable_data)
    return sorted([(player, score) for player, score in 
            scores_dict.items()], key = lambda tup: tup[1], reverse = True)

def loss_penalty_ranking_years(list_of_dicts, years):
    """
    Ranks the players that played over a range of years by scores based on their
    match esults and round numbers of those matches. Rank #1 is the highest score 
    (the best player)

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "End date," "Winner," "Loser," and "Round number"
    years : an iterable type storing integers
        the range of years to use to make the rankings

    Returns
    -------
    list of tuples
        list of (player, rank) tuples sorted in reverse order by rank
    """
    applicable_data = [dic for dic in list_of_dicts if dic["End date"].year in years]
    scores_dict = calculate_loss_penalty_scores(applicable_data)
    return sorted([(player, score) for player, score in 
            scores_dict.items()], key = lambda tup: tup[1], reverse = True)

def loss_penalty_ranking_all(list_of_dicts):
    """
    Ranks the players in all of the list_of_dicts by scores based on their
    match esults and round numbers of those matches. Rank #1 is the highest score 
    (the best player)

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "End date," "Winner," "Loser," and "Round number"

    Returns
    -------
    list of tuples
        list of (player, rank) tuples sorted in reverse order by rank
    """
    scores_dict = calculate_loss_penalty_scores(list_of_dicts)
    return sorted([(player, score) for player, score in 
            scores_dict.items()], key = lambda tup: tup[1], reverse = True)

def wbw_one_iteration(list_of_dicts, num_players, initial_scores):
    """
    Performs one iteration of calculating scores based on who a player beat

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - all dictionaries must
        have the keys "Winner" and "Loser," 
    num_players : int
        the number of players present in list_of_dicts
    initial_scores : dictionary
        dictionary with key: value pairs of player: initial score

    Returns
    -------
    new_scores : dictionary
        new dictionary with key: value pairs of player: new score
    list of tuples
        list of (player, new score) tuples in reverse order by new score
    """
    
    # initialise new scores
    new_scores = {player: 0 for player in initial_scores.keys()}
    
    # find who each player lost to
    defeated_by = {player: [] for player in initial_scores.keys()}
    for match in list_of_dicts:
        defeated_by[match["Loser"]].append(match["Winner"])
    
    # pass the shares to create the new scores
    for player in defeated_by.keys():
        number_lost_to = len(defeated_by[player])
        if number_lost_to > 0:
            for i in range(number_lost_to):
                winner = defeated_by[player].pop()
                new_scores[winner] += initial_scores[player] / number_lost_to
        else:
            new_scores[player] += initial_scores[player]
    
    # return both the dictionary holding the players and scores as well as a
    # sorted list
    return new_scores, sorted([(player, new_scores[player] * 0.85 + 0.15 / num_players) 
                               for player in new_scores.keys()], 
                              key = lambda x: x[1], reverse = True)

def wbw(list_of_dicts, initial_scores_dict = None):
    """
    A recursive ranking system assigning scores based on who beats who, giving 
    more weight to beating players with high scores

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        List of dictionaries representing the rows in the data. Each dictionary
        must have keys "Player 1", "Player 2", "Winner", and "Loser"
    initial_scores : dictionary, optional
        Dictionary in the form of player: score. The scores are used to initialise 
        the new score estimates. Under the default, None, each player is assigned 
        an initial score equal to 1/n, where n is the number of unique players.

    Returns
    -------
    new_rankings : list of tuples
        New list of (player, score) tuples sorted in reverse order by new score
    new_scores: dictionary
        New dictionary with key: value pairs of player: new score
    """
    # get all players
    players = []
    for dic in list_of_dicts:
        if dic["Player 1"] not in players:
            players.append(dic["Player 1"])
        if dic["Player 2"] not in players:
            players.append(dic["Player 2"])
    
    # get unique players and number of unique players
    unique_players = set(players)
    num_players = len(unique_players)
    
    # no initial rankings given
    if initial_scores_dict == None:

        # initialise scores and ranking order
        initial_scores_dict = {player: 1/num_players for player in unique_players}
        initial_rankings = sorted([(player, initial_scores_dict[player]) for player in 
                                   initial_scores_dict.keys()], key = lambda x: x[1], 
                                  reverse = True)
        initial_ranking_order = [player for player, score in initial_rankings]
    
    # initial rankings given
    else:
        # delete any players that are in the previous ranking but did not play
        # in the previous 52 weeks
        non_current_players = []
        for player in initial_scores_dict.keys():
            if player not in unique_players:
                non_current_players.append(player)
        for player in non_current_players:
            del initial_scores_dict[player]
        # add any players that hadn't played yet by the time the last rankings 
        # were made
        for player in unique_players:
            if player not in initial_scores_dict.keys():
                initial_scores_dict[player] = 0
        
        initial_rankings = sorted([(player, initial_scores_dict[player]) for player 
                                   in initial_scores_dict.keys()], key = lambda x: x[1], 
                                  reverse = True)
        initial_ranking_order = [player for player, score in initial_rankings]
    
    # initialise convergence count
    convergence_count = 0
    
    # loop until the ranking order stays the same 3 times in a row
    while convergence_count < 3:
        new_scores, new_rankings = wbw_one_iteration(list_of_dicts, num_players, 
                                                     initial_scores_dict)
        new_ranking_order = [player for player, score in new_rankings]
        if new_ranking_order == initial_ranking_order:
            convergence_count += 1
        else:
            convergence_count = 0
        # update old values
        initial_ranking_order = new_ranking_order
        initial_scores_dict = new_scores
    
    return new_rankings, new_scores

def assign_wbw_rankings(list_of_dicts):
    """
    Updates wbw rankings before each tournament using the previous 52 weeks of
    results and assigns them to each player by adding "WbW 1" and "WbW 2" keys
    and their respective value at each tournament to dictionaries representing
    matches that happened in or after 2008

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary must
        have keys "End date," "Tournament," "Start date," "Player 1," "Player 2,"
        "Winner," and "Loser"

    Returns
    -------
    None.

    """
    matches_from_2007 = [dic for dic in list_of_dicts if 
                         dic["End date"].year == 2007]
    initial_rankings, initial_scores = wbw(matches_from_2007)
    initial_ranks = {initial_rankings[i][0]: i + 1 for i in range(len(initial_rankings))}
    
    current_tournament = None
    current_date = None
    
    for i in range(len(list_of_dicts)):
        
        # reached a new tournament with a different start date
        if (list_of_dicts[i]["Tournament"] != current_tournament and 
            list_of_dicts[i]["Start date"].year >= 2008 and
            list_of_dicts[i]["Start date"] != current_date):
            # update current tournament and date
            current_tournament = list_of_dicts[i]["Tournament"]
            current_date = list_of_dicts[i]["Start date"]
            # get new ranks
            year_ago = current_date - timedelta(weeks = 52)
            last_52_weeks = [dic for dic in list_of_dicts if dic["End date"] > year_ago and
                             dic["Start date"] < current_date]
            new_rankings, new_scores = wbw(last_52_weeks, initial_scores_dict = initial_scores)
            new_ranks = {new_rankings[i][0]: i + 1 for i in range(len(new_rankings))}
            # assign new ranks
            if list_of_dicts[i]["Player 1"] in new_ranks.keys():
                list_of_dicts[i]["WbW 1"] = new_ranks[list_of_dicts[i]["Player 1"]]
            else:
                list_of_dicts[i]["WbW 1"] = math.nan
            if list_of_dicts[i]["Player 2"] in new_ranks.keys():
                list_of_dicts[i]["WbW 2"] = new_ranks[list_of_dicts[i]["Player 2"]]
            else:
                list_of_dicts[i]["WbW 2"] = math.nan
            # update initial ranks
            initial_rankings = new_rankings
            initial_ranks = new_ranks
            initial_scores = new_scores
        
        # reached a new tournament with same start date
        elif (list_of_dicts[i]["Tournament"] != current_tournament and 
            list_of_dicts[i]["Start date"].year >= 2008 and
            list_of_dicts[i]["Start date"] == current_date):
            # assign ranks
            if list_of_dicts[i]["Player 1"] in initial_ranks.keys():
                list_of_dicts[i]["WbW 1"] = initial_ranks[list_of_dicts[i]["Player 1"]]
            else:
                list_of_dicts[i]["WbW 1"] = math.nan
            if list_of_dicts[i]["Player 2"] in initial_ranks.keys():
                list_of_dicts[i]["WbW 2"] = initial_ranks[list_of_dicts[i]["Player 2"]]
            else:
                list_of_dicts[i]["WbW 2"] = math.nan
        
        # not a new tournamment, but rank should be assigned
        elif (list_of_dicts[i]["Tournament"] == current_tournament and 
            list_of_dicts[i]["Start date"].year >= 2008):
            # assign ranks
            if list_of_dicts[i]["Player 1"] in initial_ranks.keys():
                list_of_dicts[i]["WbW 1"] = initial_ranks[list_of_dicts[i]["Player 1"]]
            else:
                list_of_dicts[i]["WbW 1"] = math.nan
            if list_of_dicts[i]["Player 2"] in initial_ranks.keys():
                list_of_dicts[i]["WbW 2"] = initial_ranks[list_of_dicts[i]["Player 2"]]
            else:
                list_of_dicts[i]["WbW 2"] = math.nan

def get_rankings_for_plot(list_of_dicts):
    """
    Builds a list of WTA rankings and a list of WbW rankings with the same player's
    rankings for the same tournament at the same index in both lists

    Parameters
    ----------
    list_of_dicts : list of dictionaries
        list of dictionaries representing rows of data - each dictionary for
        matches in or after 2008 should have keys "Tournament," "WbW 1," "WbW 2,"
        "Rank 1," "Rank 2," "Player 1," and "Player 2"

    Returns
    -------
    wta_ranks : list of floats
        list of WTA ranks for each player before each tournament in and after
        2008; indices lined up with wbw_ranks
    wbw_ranks : list of floats
        list of WbW ranks for each player before each tournament in and after
        2008; indices lined up with wta_ranks
    """
    
    # initialise variables
    wta_ranks = []
    wbw_ranks = []
    current_tournament = None
    
    # build the wta_ranks and wbw_ranks lists
    for i in range(len(list_of_dicts)):
        
        # next tournament
        if ("WbW 1" in list_of_dicts[i].keys() and list_of_dicts[i]["Tournament"] !=
            current_tournament):
            players_current_tournament = []
            current_tournament = list_of_dicts[i]["Tournament"]
            wta_ranks.append(list_of_dicts[i]["Rank 1"])
            wbw_ranks.append(list_of_dicts[i]["WbW 1"])
            players_current_tournament.append(list_of_dicts[i]["Player 1"])
            wta_ranks.append(list_of_dicts[i]["Rank 2"])
            wbw_ranks.append(list_of_dicts[i]["WbW 2"])
            players_current_tournament.append(list_of_dicts[i]["Player 2"])
            
        # same tournament
        elif ("WbW 1" in list_of_dicts[i].keys() and list_of_dicts[i]["Tournament"] ==
            current_tournament):
            if list_of_dicts[i]["Player 1"] not in players_current_tournament:
                wta_ranks.append(list_of_dicts[i]["Rank 1"])
                wbw_ranks.append(list_of_dicts[i]["WbW 1"])
                players_current_tournament.append(list_of_dicts[i]["Player 1"])
            if list_of_dicts[i]["Player 2"] not in players_current_tournament:
                wta_ranks.append(list_of_dicts[i]["Rank 2"])
                wbw_ranks.append(list_of_dicts[i]["WbW 2"])
                players_current_tournament.append(list_of_dicts[i]["Player 2"])
    
    return wta_ranks, wbw_ranks

if __name__ == "__main__":
    main()
    