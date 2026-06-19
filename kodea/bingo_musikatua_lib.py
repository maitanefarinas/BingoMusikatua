# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 00:45:57 2023

@author: Maitane Fariñas Argoitia
"""

import numpy as np

# Bestelako funtzioak
def kolorea_sortu(abestia: str):
    import hashlib
    import colorsys
    h = hashlib.md5(abestia.encode()).hexdigest()

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
## ABESTIEN FITXATEGIA IRAKURRI
def fitxategia_irakurri(abesti_zerrenda_filename: str):
    """
    Hiztegi bat itzultzen du
    """
    partidak = {}
    with open(abesti_zerrenda_filename, "r") as az:
        for line in az:
            line = line.strip()
            if not line:
                continue

            # Begiratu zein zenbaki duen partidak
            line_zatitua = line.split(" ", 1)
            
            # Abestien zenbakirik ez badago, bingo bakarra egingo dela suposatzen da
            if not line_zatitua[0].isdigit() or (line_zatitua[0].isdigit() and len(line_zatitua) == 1):
                indizea = 1
                abestia = line

            # Bestela, zenbakiari dagokion bingo partidan gehituko da abestia
            else:
                indizea = int(line_zatitua[0])
                abestia = line_zatitua[1].strip()
            
            if indizea in partidak.keys():
                partidak[indizea].append(abestia)
            else:
                partidak[indizea] = [abestia]
    
    return partidak


###############################################
# KARTOIETAKO ZENBAKIAK LORTU

## Kartoi bat
def kartoi_bat_sortu(abesti_kopurua_guztira, kartoiko_abesti_kopurua):
    import random

    if kartoiko_abesti_kopurua > abesti_kopurua_guztira:
        raise ValueError()
    
    return set(random.sample(range(1, abesti_kopurua_guztira + 1), kartoiko_abesti_kopurua))

## Kartoi multzoa
def partidako_kartoiak_sortu(kartoi_kopurua, abesti_kopurua_guztira, kartoiko_abesti_kopurua):
    import math
    import random

    kartoiak = set()

    if kartoi_kopurua > math.comb(abesti_kopurua_guztira, kartoiko_abesti_kopurua):
        raise ValueError("Ez dago konbinazio nahikorik kartoi ezberdinak sortzeko! Gehitu abesti gehiago zerrendan, txikitu kartoiaren tamaina edo gutxitu kartoi kopurua.")

    while len(kartoiak) < kartoi_kopurua:
        kartoia_i = frozenset(kartoi_bat_sortu(abesti_kopurua_guztira, kartoiko_abesti_kopurua))
        kartoiak.add(kartoia_i)
    
    return [random.sample(kartoi, len(kartoi)) for kartoi in kartoiak]

## Partida bakoitzerako kartoiak biltzen dituen hiztegia
def kartoien_hiztegia_sortu(partidetako_abestiak, kartoiko_abesti_kopurua, kartoi_kopurua):
    partida_kopurua = len(partidetako_abestiak)
    partidetako_kartoiak = {}
    for i in range(partida_kopurua):
        partida = i+1
        abesti_kopurua_guztira = len(partidetako_abestiak[partida])
        partidetako_kartoiak[partida] = partidako_kartoiak_sortu(kartoi_kopurua, abesti_kopurua_guztira, kartoiko_abesti_kopurua)
    
    return partidetako_kartoiak

###############################################
# TAULETAKO KODEA SORTU

## Dokumentuaren sarrera
def sarrera_idatzi():
    # Kodeko lehen zatia
    sarrerako_zatia = r"""
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
    return sarrerako_zatia

# Kartoi bakoitzaren kodea
def taula_kodea_idatzi(izenburua, jokaldia_index, kartoia_i, kartoiko_abesti_kopurua, partidetako_abestiak, gehitu_partida_indizea=False, kolorea_gehitu=False):

    # Tablako kodian lelengo zatixa (beti iguala)
    izenburu_berria = izenburua
    if gehitu_partida_indizea:
        izenburu_berria = f"{izenburua} - {jokaldia_index+1}"

    kode_berria = (
    "\\begin{center}\n"
    "{\\Large\\textbf{" + izenburu_berria.strip() + "}}\n"
    "\\end{center}\n"
    "\\vspace{-7mm}\n"
    "\\begin{table}[H]\n"
    "\\centering\n"
    "\\begin{tabular}{|C{5.75cm}|C{5.75cm}|C{5.75cm}|}\n"
    "\\hline\n"
    )

    # Abestiak gehitu
    for j in range(kartoiko_abesti_kopurua):
        #print(partidetako_abestiak[jokaldia_index][kartoia_i[j]])
        abestiaren_izena = partidetako_abestiak[jokaldia_index+1][kartoia_i[j]-1].strip()
        kolorea_kodea = ""
        if kolorea_gehitu:
            kolorea_kodea = "{\cellcolor[HTML]{" + f"{kolorea_sortu(abestiaren_izena)}" + "}"
        else:
            if j%2 == 1: kolorea_kodea = "{\cellcolor{" + "gray!40" + "}"
            
        kode_berria += kolorea_kodea +"{\\textbf{" + abestiaren_izena + "}}"
        if kolorea_gehitu or j%2==1: kode_berria += "}"

        if (j+1)%3 == 0:
            kode_berria += "\\\\ \\hline"
        else:
            kode_berria += "&"

    kode_berria += """
    \\end{tabular}
    \\end{table}
    \\vspace{5mm}
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    """

    return kode_berria

## Partida osoko kartoien kodea sortzen du
def orria_gehitu(i, partida_kopurua, jokaldia_index, k):
    orri_amaiera = ""
    if ((i+1)%k == 0) and (i!=0):
        orri_amaiera += '\\newpage\n'
    if partida_kopurua%2 != 0 and jokaldia_index == partida_kopurua:
        orri_amaiera += '\\null\\newpage\n'

    return orri_amaiera

def kartoiak_idatzi_n(kartoiko_abesti_kopurua, kartoi_kopurua,
                     abesti_zerrenda_filename,
                     output_fitxategia_filename='kode_osoa.txt',
                     koloretan = False,
                     izenburua: str = "BINGO MUSIKATUA"):

    partidetako_abestiak = fitxategia_irakurri(abesti_zerrenda_filename)
    partida_kopurua = len(partidetako_abestiak)
    partidetako_kartoiak = kartoien_hiztegia_sortu(partidetako_abestiak, kartoiko_abesti_kopurua, kartoi_kopurua)

    # Ziurtatu kartoiko abesti kopurua 3ren multiploa dela
    if kartoiko_abesti_kopurua%3 != 0:
        raise ValueError(f"Kartoiko abesti kopuruak 3ren multiploa izan behar du! {kartoiko_abesti_kopurua}-k ez du balio.")

    # Orri batean zenbat kartoi sartzen diren zehazteko
    k = 5
    if kartoiko_abesti_kopurua > 12: k = 4
    
    # Gure kode osoa hemen idazten joango gara: kode_osoa_bingo
    kode_osoa_bingo = sarrera_idatzi()

    for i in range(kartoi_kopurua*partida_kopurua):
        # Indize honek esango digu orriaren zein aldetan idazten ari garen (1. partida edo 2.a den, hain zuzen)
        jokaldia_index = int((i/k)%partida_kopurua)

        # Orain taulari dagokion kodea gehituko diogu
        kartoia_i = partidetako_kartoiak[jokaldia_index+1].pop(0)
        #print(kartoia_i)
        taulako_kodea = taula_kodea_idatzi(izenburua, jokaldia_index, kartoia_i, kartoiko_abesti_kopurua, partidetako_abestiak,
                                           gehitu_partida_indizea=(partida_kopurua!=1), kolorea_gehitu=koloretan)

        kode_osoa_bingo += taulako_kodea

        # 4-ren multiploetan, orri berrirako kodea gehitu
        kode_osoa_bingo += orria_gehitu(i, partida_kopurua, jokaldia_index, k)

    kode_osoa_bingo += '\\end{document}'
    # Fitxategian idatzi
    with open(output_fitxategia_filename, "w") as of:
        of.write(kode_osoa_bingo)



### Histograma sortu zenbat iraungo duen kalkulatzeko

# Honekin ez dugu denbora zehatza jakingo, bingo zenbagarren abestian egingo den baizik.
# Horren arabera abesti bakoitzean zenbat denbora entzungo dugun erabaki eta listo
def bingo_histograma_sortu(N_partaide, N_abesti_kopurua, N_kartoiaren_tamaina, normalizatu = False, irudikatu=False, N_errepikapen=3e2):
    """
    Histograma bat sortzen du N_errepikapen-en ostean (errepikapen bakoitza bingo partida bat izango da) batez bestan bingo zenbagarren
    abestian egingo den irudikatzeko. Batezbestekoa inprimatzen du, zenbaki osoetan. Histograma normalizatzeko eta irudikatzeko aukera
    ematen du. Irudia gorde nahi bada, ordea, aparteko funtzioa erabili beharko da.

    Aldagaiak:
        N_partaide (int): parte hartzaile / kartoi kopuru totala.
        N_abesti kopurua (int): guztira erabilitako abesti kopurua.
        N_kartoiaren_tamaina (int): kartoi bakoitzean agertuko den abesti kopurua.
        normalizatu (bool, False): histograma normalizatu nahi bada, True balioa eman.
        irudikatu (bool, False): histograma irudikatu nahi bada, True balioa eman.
        N_errepikapen (int, 300): simulatu nahi diren partiden kopurua.

    Itzultzeko:
        histograma (np.array): batezbesteko balioak emango dituen histograma. 
    """

    # N_errepikapen errepikapen, gero batez bestekoa egiteko
    batez_bestekoa = []
    bingo = set(np.random.choice(range(1, N_abesti_kopurua+1), size=N_kartoiaren_tamaina, replace=False))
    for i in range(int(N_errepikapen)):
        # Errepikapen bakoitzean partaide guztien kartoiak hartuko dira kontuan
        abesti_kopurua = []
        for j in range(N_partaide):
            # Partaide bakoitzan bingo zenbagarren abestian egiten duen kalkulatu
            j_jokalariaren_kartoia = []
            while not (bingo <= set(j_jokalariaren_kartoia)):
                j_jokalariaren_kartoia.append(np.random.randint(1,N_abesti_kopurua+1))
                
            # Balio hori abesti_kopurua-n gorde
            abesti_kopurua.append(len(set(j_jokalariaren_kartoia)))
        
        # Partida bakoitzeko balio txikiena batezbestekorako gorde
        batez_bestekoa.append(min(abesti_kopurua))
    
    histograma = np.zeros(N_abesti_kopurua)
    bingorako_abesti_kopurua = round(np.sum(batez_bestekoa)/N_errepikapen)

    for i in range(len(batez_bestekoa)):
        histograma[int(batez_bestekoa[i])-1] += 1
    
    print(f"Batez bestean {bingorako_abesti_kopurua}. abestian egingo da bingo.")
    if normalizatu:
        histograma = histograma/np.sum(histograma)
    
    if irudikatu:
        histograma_irudikatu(histograma, N_abesti_kopurua, N_partaide)

    return histograma


def histograma_irudikatu(histograma, N_abesti_kopurua, N_partaide, irudia_gorde=None):
    """
    `bingo_histograma_sortu` funtzioak sortutako histograma irudikatzen du, batezbestekoarekin batera.
    Irudia gordetzeko aukera eskaintzen du.

    Aldagaiak:
        histograma (np.array): abesti kopuru bakoitzeko (x) maiztasunak (y) gordetzen dituen bektorea.
        N_abesti kopurua (int): guztira erabilitako abesti kopurua.
        N_partaide (int): parte hartzaile / kartoi kopuru totala
        irudia_gorde (str, None): izena+estentsioa eskainiz gero (irudia.png), bertan gordeko du. 
    """
    import matplotlib.pyplot as plt

    # Batez bestekoa kalkulatu:
    x = np.linspace(1, N_abesti_kopurua, N_abesti_kopurua)
    bingorako_abesti_kopurua = np.average(x, weights=histograma)

    # Figura eta ardatza
    fig, ax = plt.subplots(figsize=(8, 5))

    # Sarea
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    step = 4 if N_abesti_kopurua <= 50 else 10
    ax.set_xticks(np.arange(0, N_abesti_kopurua + 1, step))

    # Grafikoa irudikatu
    ax.bar(x, histograma / np.sum(histograma), width=0.8)

    # Batezbestekoa markatu
    ax.axvline(
        bingorako_abesti_kopurua,
        linestyle='--',
        linewidth=2,
        color="orange",
        label=f'Batez bestekoa = {bingorako_abesti_kopurua:.2f}'
    )

    # Izenburu nagusia
    fig.suptitle(
        f'Bingo egiteko batez besteko abesti kopurua',
        fontsize=15
    )
    ax.set_title(
        f'{N_partaide} kartoi eta {N_abesti_kopurua} abesti             ',
        fontsize=13)

    # Ardatzetako etiketak
    ax.set_xlabel("Abesti kopurua")
    ax.set_ylabel("Maiztasuna")

    # Legenda
    ax.legend(loc='best', fontsize=12)

    plt.tight_layout()
    if irudia_gorde:
        plt.savefig(irudia_gorde, dpi=300, bbox_inches="tight")

    plt.show()