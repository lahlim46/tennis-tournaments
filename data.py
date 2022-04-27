# functions for parsing the data

import math
from datetime import datetime
import os
import csv

def main():
    pass

def parse_tennis_data_line(line_lst, col_names, year):
    """
    Makes each line into a dictionary with key value pairs of col_names: 
        corresponding line_lst values. Also changes data types, fixes data 
        errors and adds new keys, including winner and loser, and a round robin 
        key whose value says whether the tournament has a round robin group stage

    Parameters
    ----------
    line_lst : list of strings
        list of strings with each item in the list corresponding to the column
        name at the same index in col_names; same length as col_names
    col_names : list of strings
        list of strings with each column name in the list corresponding to the
        apprporiate values at the same index in line_lst; same length as line_lst
    year : int
        year the match happened

    Returns
    -------
    row_dict : dictionary
        a dictionary representation of the data with key: value pairs of
        col_names[i]: line_lst[i] for each i from 0 to the length of col_names
        line_lst minus one
    """
    
    # set up dictionary with the column names as the keys and the data as the
    # values
    row_dict = {col_names[i]: line_lst[i] for i in range(len(col_names))}
    
    # adjust data types
    row_dict["Best of"] = int(row_dict["Best of"])
    if row_dict["Rank 1"] != "":
        row_dict["Rank 1"] = float(row_dict["Rank 1"])
    else:
        row_dict["Rank 1"] = math.nan
    if row_dict["Rank 2"] != "":
        row_dict["Rank 2"] = float(row_dict["Rank 2"])
    else:
        row_dict["Rank 2"] = math.nan
    row_dict["Start date"] = datetime.strptime(row_dict["Start date"], "%Y-%m-%d")
    row_dict["End date"] = datetime.strptime(row_dict["End date"], "%Y-%m-%d")
    
    # name errors
    # Sun T.T. and Kucova K. were listed as playing after losing in single elimination 
    # tournaments with no third place match, and I learned one of the Sun T.T.s 
    # was supposed to be Sun S. and one of the Kucova K.s was wupposed to be Kucova Z.
    # I only noticed it when doing some tests the night before it was due and felt
    # like that was too late to report it and make other people stressed about
    # there being a change so late, so I'm sorry I didn't notice earlier and report it.
    if (year == 2007 and row_dict["Tournament"] == "Internationaux de Strasbourg" and
        row_dict["Player 1"] == "Sun T.T." and row_dict["Player 2"] == "Tanasugarn T."):
        row_dict["Player 1"] = "Sun S."
    if (year == 2010 and row_dict["Tournament"] == "Australian Open" and
        row_dict["Player 1"] == "Dulko G." and row_dict["Player 2"] == "Kucova K."):
        row_dict["Player 2"] = "Kucova Z."
    # Hantuchova D. was listed as playing in the third round, in the third place
    # match after loosing in the very first round, and it should have been Lisicki S.
    if (year == 2011 and row_dict["Tournament"] == "Commonwealth Bank Tournament of Champions" and
        row_dict["Player 1"] == "Hantuchova D." and row_dict["Player 2"] == "Petrova N."):
        row_dict["Player 1"] = "Lisicki S."
    
    # add winner and loser
    row_dict["Winner"], row_dict["Loser"] = get_winner_loser(row_dict)
    # Kurdermetova V. was the one to advance to the semifinals even though she 
    # retired in the quarterfinals
    if (year == 2020 and row_dict["Tournament"] == "Hobart International" and
        row_dict["Player 1"] == "Muguruza G." and row_dict["Player 2"] == "Kudermetova V."):
        row_dict["Winner"] = "Kudermetova V."
        row_dict["Loser"] = "Muguruza G."
    
    # add whether the tournament has round robin group stage
    row_dict["Round robin tournament"] = get_round_robin_status(row_dict["Tournament"], year)
    
    return row_dict

def get_and_parse_one_file(file_path, year, leftovers):
    """
    Makes each row in a csv file a dictionary, adjusts data types, fixes data
    errors, and adds new variables

    Parameters
    ----------
    file_path : string
        relative file path to a csv file to be parsed
    year : int
        year the matches in the file take place
    leftovers : list of dictionaries
        list of dictionaries representing the rows from a previous file that
        belong to tournaments that finish in this file

    Returns
    -------
    data_rows : list of dictionaries
        the rows of the csv file as dictionaries for the matches of tournaments
        that ended in year
    new_leftovers : list of dictionaries
        rows of the csv file as dictionaries for the matches of tournaments
        that end the next year
    """
    data_rows = []
    col_names = []
    old_leftovers = leftovers
    leftover_tournaments = set([dic["Tournament"] for dic in old_leftovers])
    new_leftovers = []
    
    with open(file_path) as f:
        
        reader = csv.reader(f)
        
        for row in reader:
        
            # col_names will be defined in the first line and then will be used for
            # the rest
            if row[0] != "Tournament":
                dict_to_append = parse_tennis_data_line(row, col_names, year)
            
                # add matches from tournaments that span this year and next year
                # to leftovers instead of the data
                if (dict_to_append["End date"].year == year and 
                    dict_to_append["End date"].month == 12 and 
                    dict_to_append["End date"].day == 31):
                    new_leftovers.append(dict_to_append)
                
                # if the match is a continuation of a tournament at the end of the 
                # previous year and the old matches haven't been added to the data
                # yet, add them first to preserve the order
                elif dict_to_append["Tournament"] in leftover_tournaments:
                    data_rows.extend([dic for dic in old_leftovers if dic["Tournament"] == 
                                 dict_to_append["Tournament"]])
                    leftover_tournaments.remove(dict_to_append["Tournament"])
                    data_rows.append(dict_to_append)
                
                else:
                    data_rows.append(dict_to_append)
        
            else:
                col_names = row
        
    return data_rows, new_leftovers

def get_and_parse_data(file_names, years):
    """
    Parses all csv files in file_names and returns the data as a list of 
    dictionaries
    
    Parameters
    ----------
    file_names : list of strings
        names of csv files to be parsed; one file corresponding to one year of
        tennis matches
    years : list of ints
        the years to be included in the analysis, where years[i] is the year
        in which the matches in file_names[i] took place

    Returns
    -------
    all_data : list of dictionaries
        list of dictionaries representing the rows of the data with the column
        names as keys
    """
    
    all_data = []
    leftovers = []
    
    for i in range(len(file_names)):
        # data should be stored in the assignment-final-data folder
        filepath = os.getcwd() + "/assignment-final-data/" + file_names[i]
        rows_to_extend, new_leftovers = get_and_parse_one_file(filepath, years[i], 
                                                                leftovers)
        all_data.extend(rows_to_extend)
        leftovers = new_leftovers
        print(years[i], "is done")
    
    print("All data done")
    
    return all_data

def get_set_winner(player1, player2, str_score):
    """
    Determines the winner of a tennis set

    Parameters
    ----------
    player1 : string
        name of player 1
    player2 : string
        name of player 2
    str_score : string
        score of the set in the form player1 score - player2 score

    Returns
    -------
    string
        name of the winning player
    """
    scores = str_score.split('-')
    player1_score = int(scores[0])
    player2_score = int(scores[1])
    
    if player1_score > player2_score:
        return player1
    else:
        return player2
    
def get_winner_loser(data_row):
    """
    Determines the winner of a tennis match

    Parameters
    ----------
    data_row : dictionary
        dictionary representing a row of data; must have keys "Player 1," 
        "Player 2," "Best of," "Comment," and "Set i" for each set i 1 - data_row["Best of"]

    Returns
    -------
    winner : string
        name of the winner
    loser : string
        name of the loser
    """
    # initialise variables
    player1 = data_row["Player 1"]
    player2 = data_row["Player 2"]
    player1_sets_won = 0
    player2_sets_won = 0
    need_to_win = data_row["Best of"] // 2 + 1
    
    # list of dictionary keys with values for the set scores
    score_col_names = ["Set " + str(i) for i in range(1, data_row["Best of"] + 1)]
    
    # iterate through the set scores until one player has won enough sets to 
    # win the match if the match was completed
    for col_name in score_col_names:
        if (data_row["Comment"] == "Completed" and 
            get_set_winner(player1, player2, data_row[col_name]) == player1):
            player1_sets_won += 1
            if player1_sets_won == need_to_win:
                winner = player1
                loser = player2
                break
        elif (data_row["Comment"] == "Completed" and 
              get_set_winner(player1, player2, data_row[col_name]) == player2):
            player2_sets_won += 1
            if player2_sets_won == need_to_win:
                winner = player2
                loser = player1
                break
    
    # if the match was not completed, find the winner and loser based on who
    # retired
    if data_row["Comment"] != "Completed":
        winner, loser = get_non_retiree(data_row, player1, player2)
        
    return winner, loser

def get_non_retiree(data_row, player1, player2):
    """
    Determines who retired and who did not

    Parameters
    ----------
    data_row : dictionary
        dictionary representing a row of data
    player1 : string
        name of player 1
    player2 : string
        name of player 2

    Returns
    -------
    non_retiree : string
        name of the player that did not retire
    retiree : string
        name of the player that retired
    """
    # find the retiree from the comment
    comment = data_row["Comment"]
    try:
        retiree = comment[:comment.index(" Retired")]
    except ValueError:
        print('"Retired" not a substring of ' + comment)
    else:
        assertion_msg = ("The Retired player, " + retiree + ", is not one of " +
                         "the players listed in the match between " + player1 + 
                         " and " + player2 + " at the " + data_row["Tournament"] +
                         " tournament.")
        assert retiree == player1 or retiree == player2, assertion_msg
        
        # find non-retiree
        if retiree == player1:
            non_retiree = player2
        else:
            non_retiree = player1
            
        return non_retiree, retiree

def get_round_robin_status(tournament_name, year):
    """
    Determines whether a match was part of a tournament with a round robin
    group stage

    Parameters
    ----------
    tournament_name : string
        name of the tournament that match was a part of
    year : int
        year the tournament took place

    Returns
    -------
    bool
        True if the match was part of a tournament with a round robin group
        stage and False otherwise
    """
    if (tournament_name == "Sony Ericsson Championships" and 
        year in range(2007, 2016)):
        return True
    if (tournament_name == "Commonwealth Bank Tournament of Champions" and
        year == 2009):
        return True
    if (tournament_name == "Qatar Airways Tournament of Champions Sofia" and
        year == 2012):
        return True
    if (tournament_name == "Garanti Koza WTA Tournament of Champions" and
        year in range(2013, 2015)):
        return True
    if (tournament_name == "BNP Paribas WTA Finals" and year in range(2016, 2019)):
        return True
    if (tournament_name == "WTA Elite Trophy" and year in range(2015, 2020)):
        return True
    if (tournament_name == "WTA Finals" and (year == 2019 or year == 2021)):
        return True
    return False
    
def sort(data, variable_name, for_each = None, in_place = False, descending = False,
         for_each_descending = False):
    """
    Sort list of dictionaries based on values at the variable_name key. Will sort
    based on variable_name for each sorted value of the for_each key if for_each != None.
    Control ascending/descending order of variable_name with the descending parameter.
    Control ascending/descending order of for_each with the for_each_descending
    parameter. The list can be sorted in place or a new sorted list can be created,
    leaving the original list unchanged.

    Parameters
    ----------
    data : list of dictionaries
        DESCRIPTION.
    variable_name : string
        Name of the variable in the data to sort by. Must be in all dictionaries
        in the list.
    for_each : string, optional
        DESCRIPTION. Must be in all dictionaries in the list.The default is None.
    in_place : Boolean, optional
        Sort in place if True and create a new sorted list if False. The default 
        is False.
    descending : Boolean, optional
        Sort in descending order if True and ascending order if False. The
        default is False.
    for_each_descending: Boolean, optional
        Sort the for_each variable in descending order if True and ascending order
        if False. The default is False.

    Returns
    -------
    Returns a new sorted list of dictionaries if in_place is set to False and
    returns None if in_place is set to True
    """
    # help with using lambdas to sort and sorting based on two elements from
    # https://linuxhint.com/sort-lambda-python/ and
    # https://stackoverflow.com/questions/5212870/sorting-a-python-list-by-two-fields
    if not in_place and for_each == None:
        return sorted(data, key = lambda dic: dic[variable_name], 
                      reverse = descending)
    
    elif not in_place and for_each != None:
        if not descending and not for_each_descending:
            return sorted(data, key = lambda dic: (dic[for_each], 
                                                   dic[variable_name]))
        elif not descending and for_each_descending:
            return sorted(data, key = lambda dic: (-dic[for_each], 
                                                   dic[variable_name]))
        elif descending and not for_each_descending:
            return sorted(data, key = lambda dic: (dic[for_each], 
                                                   -dic[variable_name]))
        else:
            return sorted(data, key = lambda dic: (-dic[for_each],
                                                   -dic[variable_name]))
        
    elif in_place and for_each != None:
        if not descending and not for_each_descending:
            data.sort(key = lambda dic: (dic[for_each], dic[variable_name]))
        elif not descending and for_each_descending:
            data.sort(key = lambda dic: (-dic[for_each], dic[variable_name]))
        elif descending and not for_each_descending:
            data.sort(key = lambda dic: (dic[for_each], -dic[variable_name]))
        else:
            data.sort(key = lambda dic: (-dic[for_each], -dic[variable_name]))
        
    else:
        data.sort(key = lambda dic: dic[variable_name], reverse = descending)

if __name__ == "__main__":
    main()