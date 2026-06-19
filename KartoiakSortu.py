############################################
# Bingo musikatuko kartoiak sortzeko kodea.
############################################
import bingo_musikatua_lib as bm
import argparse
from pathlib import Path


def get_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--abesti-zerrenda", required=True, type=Path,
                        help="Abestien zerrendaren txt fitxategia. Adibide bat behar izanez gero begiratu fitxategiak/ karpetan.")
    parser.add_argument("-o", "--latex-kodea", required=False, default="latex_kodea.txt",
                        help="Latexeko kodea idazteko sortuko den fitxategiaren izena.")
    parser.add_argument("-N", "--kartoi-kopurua", required=True, type=int,
                        help="Nahi dugun kartoi kopurua, partidako. Partida bat baino gehiago izanez gero, bietan kopuru bera erabiliko da.")
    parser.add_argument("-n", "--abesti-kopurua", required=True, type=int,
                        help="Kartoi bakoitzeko abesti kopurua. 3ren multiploa!!!!!!")
    parser.add_argument("-k", "--koloretan", action="store_true",
                        help="Kartoiak koloretan inprimatzeko. Abesti bakoitzari ausazko kolore bat ematen zaio.")
    parser.add_argument("-i", "--izenburua", type=str, required=False, default=None,
                        help="Kartoiaren gainean idatziko den izenburua. Adib: 'BINGO MUSIKATUA'")

    return parser


def get_command_line_arguments():
    parser = get_parser()
    return parser.parse_args()



def main():
    args = get_command_line_arguments()

    zerrenda_fitx = args.abesti_zerrenda.as_posix()
    kartoi_kopurua = args.kartoi_kopurua
    output_fitxategia = args.latex_kodea
    abesti_kopurua = args.abesti_kopurua
    koloretan = args.koloretan
    izenburua = args.izenburua

    if izenburua:
        bm.kartoiak_idatzi_n(kartoiko_abesti_kopurua=abesti_kopurua,
                kartoi_kopurua=kartoi_kopurua,
                abesti_zerrenda_filename=zerrenda_fitx,  # Gure abestien zerrenda (hau adibide moduan dagoena da, partida bakarrarekin)
                output_fitxategia_filename=output_fitxategia,  # Latex-eko kodearekin sortuko den fitxategia
                koloretan=koloretan,   # Koloreak nahi baditugu, bestela ezabatu zati hau
                izenburua=izenburua
                )
    else:
        bm.kartoiak_idatzi_n(kartoiko_abesti_kopurua=abesti_kopurua,
                        kartoi_kopurua=kartoi_kopurua,
                        abesti_zerrenda_filename=zerrenda_fitx,  # Gure abestien zerrenda (hau adibide moduan dagoena da, partida bakarrarekin)
                        output_fitxategia_filename=output_fitxategia,  # Latex-eko kodearekin sortuko den fitxategia
                        koloretan=koloretan   # Koloreak nahi baditugu, bestela ezabatu zati hau
                        )

    output_fitxategia = Path(output_fitxategia)
    if output_fitxategia.is_file():
        print(f"Ondo sortu da {output_fitxategia.as_posix()} fitxategia!")
    else:
        print(f"Arazo bat egon da. Ezin izan da {output_fitxategia.as_posix()} fitxategia sortu.")

if __name__ == "__main__":
    main()
