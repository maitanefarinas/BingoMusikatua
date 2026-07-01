# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 00:45:57 2023

@author: Maitane Fariñas Argoitia
"""

import numpy as np

# Other functions
def create_color(song: str):
    import hashlib
    import colorsys
    h = hashlib.md5(song.encode()).hexdigest()

    # evenly distributed hue (0–1)
    hue = int(h[:8], 16) / 0xffffffff

    # optional: shift hue slightly to avoid green dominance perception
    hue = (hue + 0.18) % 1.0

    # tighter, controlled ranges
    saturation = 0.25 + (int(h[8:12], 16) % 20) / 100  # 0.45–0.65
    lightness = 0.82 + (int(h[12:16], 16) % 8) / 100   # 0.82–0.90

    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)

    return "{:02x}{:02x}{:02x}".format(
        int(r * 255),
        int(g * 255),
        int(b * 255)
    )


###############################################
## READ SONG FILE
def read_file(song_filename: str):
    """
    It returns a dictionary
    """
    import re
    games = {}
    with open(song_filename, "r") as az:
        for line in az:
            line = line.strip()
            if not line:
                continue

            # Check number of game (if it has one)
            split_line = line.split(" ", 1)
            
            # If there is no number, we assume its a single game
            if not split_line[0].isdigit() or (split_line[0].isdigit() and len(split_line) == 1):
                index = 1
                song = line.strip()

            # Otherwise, classify songs in games (using provided number)
            else:
                index = int(split_line[0])
                song = split_line[1].strip()
            
            # Check if there is a specification of size
            size_match = re.match(r"\[(\w)\]", song.split()[-1].strip())
            if size_match:
                size_match = size_match.group(1)
                song = re.sub(r"\s*\[(\w)\]","",song)
                if   size_match.lower() == "s": song = "\small{"+song+"}"  # if [s] -> small
                elif size_match.lower() == "t": song = "\tiny{"+song+"}"   # if [t] -> tiny
            
            if index in games.keys():
                games[index].append(song)
            else:
                games[index] = [song]
    
    return games


###############################################
# GENERATE THE ACTUAL CARDS (WITH NUMBERS)

## Single card
def create_single_card(total_number_songs, songs_per_card):
    import random

    if songs_per_card > total_number_songs:
        raise ValueError()
    
    return set(random.sample(range(1, total_number_songs + 1), songs_per_card))

## Set of cards (all different)
def create_cards_for_game(number_of_cards, total_number_songs, songs_per_card):
    import math
    import random

    cards = set()

    if number_of_cards > math.comb(total_number_songs, songs_per_card):
        raise ValueError("There are not enough combinations to create different cards! Add more songs to the list, make the cards smaller or lower the number of cards.")
        
    while len(cards) < number_of_cards:
        card_i = frozenset(create_single_card(total_number_songs, songs_per_card))
        cards.add(card_i)
    
    return [random.sample(card, len(card)) for card in cards]

## Dictionary with the cards for all games
def create_card_dictionary(songs_of_game, songs_per_card, number_of_cards):
    number_of_games = len(songs_of_game)
    game_cards = {}
    for i in range(number_of_games):
        game = i+1
        total_number_songs = len(songs_of_game[game])
        game_cards[game] = create_cards_for_game(number_of_cards, total_number_songs, songs_per_card)
    
    return game_cards

###############################################
# GENERATE CODE FOR CARDS

## Write beginning of latex code
def write_beginning():
    intro = r"""
    \documentclass[12pt]{article}
    \usepackage[utf8]{inputenc}
    \usepackage{nunito}
    \usepackage{float}
    \usepackage[T1]{fontenc}
    \usepackage[table,xcdraw]{xcolor}
    \usepackage[left=0.5cm,right=0.5cm,top=2cm,bottom=1cm]{geometry}
    \pagenumbering{gobble}
    \begin{document}
    \renewcommand{\arraystretch}{1.6}
    \newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
    """
    return intro

# Code for each card
def write_card_code(title, game_index, card_i, songs_per_card, songs_of_game, add_game_index=False, add_colour=False):

    # Tablako kodian lelengo zatixa (beti iguala)
    izenburu_berria = title
    if add_game_index:
        izenburu_berria = f"{title} - {game_index+1}"

    new_code = (
    "\\begin{center}\n"
    "{\\Large\\textbf{" + izenburu_berria.strip() + "}}\n"
    "\\end{center}\n"
    "\\vspace{-7mm}\n"
    "\\begin{table}[H]\n"
    "\\centering\n"
    "\\begin{tabular}{|C{5.75cm}|C{5.75cm}|C{5.75cm}|}\n"
    "\\hline\n"
    )

    # Add song names
    for j in range(songs_per_card):

        song_name = songs_of_game[game_index+1][card_i[j]-1].strip()
        colour_code = ""
        if add_colour:
            colour_code = "{\cellcolor[HTML]{" + f"{create_color(song_name)}" + "}"
        else:
            if j%2 == 1: colour_code = "{\cellcolor{" + "gray!40" + "}"
            
        new_code += colour_code +"{\\textbf{" + song_name + "}}"
        if add_colour or j%2==1: new_code += "}"

        if (j+1)%3 == 0:
            new_code += "\\\\ \\hline"
        else:
            new_code += "&"

    new_code += """
    \\end{tabular}
    \\end{table}
    \\vspace{5mm}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    return new_code

## Generate whole code
def add_page(i, n_games, game_index, k):
    end_of_page = ""
    if ((i+1)%k == 0) and (i!=0):
        end_of_page += '\\newpage\n'
    if n_games%2 != 0 and game_index == n_games:
        end_of_page += '\\null\\newpage\n'

    return end_of_page

def write_cards(songs_per_card, number_of_cards,
                song_filename,
                output_filename='whole_latex_code.tex',
                add_colour = False,
                title: str = "MUSICAL BINGO"):

    songs_of_games = read_file(song_filename)
    number_of_games = len(songs_of_games)
    cards_of_games = create_card_dictionary(songs_of_games, songs_per_card, number_of_cards)

    # Make sure the number of songs is a multiple of 3
    if songs_per_card%3 != 0:
        raise ValueError(f"The number of songs per card has to be a multiple of 3! {songs_per_card} is not a valid number.")

    # To set the number of cards per page (depending on size)
    k = 5
    if songs_per_card > 12: k = 4
    
    # We start writing the whole code in variable "whole_code_bingo"
    whole_code_bingo = write_beginning()

    for i in range(number_of_cards*number_of_games):
        # This index tells us in which face of the page we need to write (depending if its game 1 or 2)
        game_index = int((i/k)%number_of_games)

        # Add code to the card
        card_i = cards_of_games[game_index+1].pop(0)

        code_of_card = write_card_code(title, game_index, card_i, songs_per_card, songs_of_games,
                                           add_game_index=(number_of_games!=1), add_colour=add_colour)

        whole_code_bingo += code_of_card

        # Add code for end of page depending on index k
        whole_code_bingo += add_page(i, number_of_games, game_index, k)

    whole_code_bingo += '\\end{document}'

    # Write to file
    with open(output_filename, "w") as of:
        of.write(whole_code_bingo)


##############################
### These functions are used to create histograms to gather information about how long
### each Bingo game will be, given number of people (cards), size of cards, total number of
### songs...
##############################

# This function won't directly give us how long the game will take (because we don't know
# how long the song will last), but at which round the bingo will end (i.e, song number 17).
# Then you just need to adjust the length of the song to fit the length of the Bingo game.
def create_bingo_histogram(number_of_cards, total_number_of_songs, songs_per_card, normalise = False, _plot=False, n_trials=3e2):
    """
    This functions creates a histogram, doing the average over the number of trials (n_trials), where each trial simulates a game, to show
    how long (how many songs) it will take to end the game = for someone to earn Bingo. It also prints the average number of songs needed.
    You have the option to normalise the histogram (set normalise=True). You also have the option to plot the histogram (set _plot=True).
    If you want to save the plot, you need to use an additional function.

    Arguments:
        number_of_cards (int): total number of players (cards).
        total_number_of_songs (int): total number of songs used.
        songs_per_card (int): number of songs that will appear in a card.
        normalise (bool, False): the histogram will be normalised if set to True.
        _plot (bool, False): the histogram will be plotted if set to True.
        n_trials (int, 300): number of games we want to use for the average.

    Result:
        histogram (np.array): histogram with the averaged results. 
    """

    # n_trial repetitions, to obtain the average
    average = []
    bingo = set(np.random.choice(range(1, total_number_of_songs+1), size=songs_per_card, replace=False))
    for i in range(int(n_trials)):
        # In each repetition, we take into account the cards of all players
        number_of_songs = []
        for j in range(number_of_cards):
            # Calculate how long it will take for each player to do Bingo
            player_j_card = []
            while not (bingo <= set(player_j_card)):
                player_j_card.append(np.random.randint(1,total_number_of_songs+1))

            # Save value to number of songs
            number_of_songs.append(len(set(player_j_card)))
        
        # Use the smaller number (the winner's card) for the game average
        average.append(min(number_of_songs))
    
    histogram = np.zeros(total_number_of_songs)
    needed_songs_for_bingo = round(np.sum(average)/n_trials)

    for i in range(len(average)):
        histogram[int(average[i])-1] += 1
    
    print(f"On average, you will need to play {needed_songs_for_bingo} songs for a game to end.")
    if normalise:
        histogram = histogram/np.sum(histogram)
    
    if _plot:
        show_histogram(histogram, total_number_of_songs, number_of_cards)

    return histogram


def show_histogram(histogram, total_number_of_songs, number_of_cards, save_image=None):
    """
    Plots the histogram created in `create_bingo_histogram`, along the average value.
    You have the option to save the image to a file by providing the filename in `save_image`.

    Arguments:
        histogram (np.array): histogram (array) storing the number of appearances (y) for each song (x).
        total_number_of_songs (int): total number of songs used.
        number_of_cards (int): total number of cards (players).
        save_image (str, None): if provided `name.extension`, the image will be stored. 
    """
    import matplotlib.pyplot as plt

    # Calculate average:
    x = np.linspace(1, total_number_of_songs, total_number_of_songs)
    number_of_songs_for_bingo = np.average(x, weights=histogram)

    # Fig and axes
    fig, ax = plt.subplots(figsize=(8, 5))

    # Grid
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    step = 4 if total_number_of_songs <= 50 else 10
    ax.set_xticks(np.arange(0, total_number_of_songs + 1, step))

    # Plot the data
    ax.bar(x, histogram / np.sum(histogram), width=0.8)

    # Show the average
    ax.axvline(
        number_of_songs_for_bingo,
        linestyle='--',
        linewidth=2,
        color="orange",
        label=f'Average = {number_of_songs_for_bingo:.2f}'
    )

    # Titles, labels and legends
    fig.suptitle(
        f'Number of songs needed to end Bingo game',
        fontsize=15
    )
    ax.set_title(
        f'with {number_of_cards} cards and {total_number_of_songs} songs             ',
        fontsize=13)

    ax.set_xlabel("Number of songs")
    ax.set_ylabel("Number of appearances")

    ax.legend(loc='best', fontsize=12)

    # Save image
    plt.tight_layout()
    if save_image:
        plt.savefig(save_image, dpi=300, bbox_inches="tight")

    plt.show()