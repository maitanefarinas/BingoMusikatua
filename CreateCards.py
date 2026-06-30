###########################################
# Code to generate cards for musical bingo.
###########################################
import source.musical_bingo_lib as bm
import argparse
from pathlib import Path


def get_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--file-list", required=True, type=Path,
                        help="Txt file of the list of songs. Find an example in `files/` directory.")
    parser.add_argument("-o", "--latex-code", required=False, default="whole_latex_code.txt",
                        help="File that will be generated with the LaTeX code.")
    parser.add_argument("-N", "--number-of-cards", required=True, type=int,
                        help="Number of bingo cards for the game. If more than a game, the same number will be used in both.")
    parser.add_argument("-n", "--number-of-songs", required=True, type=int,
                        help="Number of songs per card. Multiple of 3!!!!!!")
    parser.add_argument("-k", "--colour", action="store_true",
                        help="Add this flag to generate cards in colour.")
    parser.add_argument("-i", "--title", type=str, required=False, default=None,
                        help="Title that will be added on top of the cards. Adib: 'MUSICAL BINGO'")

    return parser


def get_command_line_arguments():
    parser = get_parser()
    return parser.parse_args()



def main():
    args = get_command_line_arguments()

    song_file = args.file_list.as_posix()
    number_cards = args.numer_of_cards
    output_file = args.latex_code
    number_songs = args.number_of_songs
    in_colour = args.colour
    title = args.title

    if title:
        bm.write_cards(songs_per_card=number_songs,
                number_of_cards=number_cards,
                song_filename=song_file,  # Gure abestien zerrenda (hau adibide moduan dagoena da, partida bakarrarekin)
                output_filename=output_file,  # Latex-eko kodearekin sortuko den fitxategia
                add_colour=in_colour,   # Koloreak nahi baditugu, bestela ezabatu zati hau
                title=title
                )
    else:
        bm.write_cards(songs_per_card=number_songs,
                        number_of_cards=number_cards,
                        song_filename=song_file,  # Gure abestien zerrenda (hau adibide moduan dagoena da, partida bakarrarekin)
                        output_filename=output_file,  # Latex-eko kodearekin sortuko den fitxategia
                        add_colour=in_colour   # Koloreak nahi baditugu, bestela ezabatu zati hau
                        )

    output_file = Path(output_file)
    if output_file.is_file():
        print(f"File {output_file.as_posix()} generated correctly!")
    else:
        print(f"There was an issue. File {output_file.as_posix()} was not properly generated.")

if __name__ == "__main__":
    main()
