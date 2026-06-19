# BingoMusikatua - Bingo musikatuetarako kartoiak automatikoki sortzeko kodea!

<p align="center">
  <img src="fitxategiak/.irudiak/logoa.png" width="400">
</p>

Kode honek bingoko kartoiak sortzen ditu, baina, zenbakien ordez, abestien izenak erabilita.

Abesti-zerrenda baten fitxategia emanda, bingoko kartoiak sortzen ditu, LaTeX kodean idatzita. Kode hori LaTeX konpilatzaile batean itsastea besterik ez da behar amaierako PDFa sortzeko (beherago ikus daiteke nola geratzen den).


## Nola erabili?

Lehenik eta behin, `python` erabilgarri izan behar da, Python scriptak erabiliko ditugu eta bingoko kartoien kodea sortzeko.

### Idatzi abesti zerrenda

Fitxategi honek nolakoa izan behar duen jakiteko, jo `fitxategiak/` karpetara. Bi zerrenda ikusiko dituzu bertan: partida bakarrerako abestiak dituena (`zerrenda_adibidea_partida1.txt`), eta bi bingo-partida egiteko abestiak dituena (`zerrenda_adibidea_2partida.txt`). Egitura bera dute; alde bakarra, bigarrenak `1` eta `2` zenbakiak dituela abestien izenaren aurretik, abesti bakoitza zein partidari dagokion zehaztu ahal izateko.

### Sortu kodea

Bi modutan egin daiteke:

#### Interaktiboki, Notebook bidez

Modu hau erabiltzeko, ireki `BingoMusikatuaNotebook.ipynb` fitxategia. Notebook hau pausoz pauso joango da urratsak azaltzen. Azalpenean zehar ageri diren balioak nahi beste alda ditzakezu, zuk nahi duzun partida osatzeko: abesti kopurua, bingoko kartoi kopurua, kartoien koloreak, izenburuak...

Bingo-saiorako zenbat abesti aukeratu ez badakizu, notebook-aren lehen zatia lagungarri izango zaizu: zure datuak sartuta, batez bestean partida zenbagarren abestian amaituko den estimatzen du. Abesti bakoitzari eman nahi diozun luzeraren arabera (abesti osoa, 30s, minutu bat...), zure partidaren gutxi gorabeherako iraupena kalkulatu ahal izango duzu!

Bigarren zatian, aldiz, zure datuak sartuta, zuzenean sortu ahal izango duzu LaTeX kodearen fitxategia. Kode hori konpilatuta, bingorako partida jokatzeko kartoi guztiak izango dituzu, denak ezberdinak. PDFa inprimatzea eta moztea baino ez zaizu faltako.

#### Zuzenean, terminaletik

Zuzenean terminaletik ere egin daiteke prozesua, Python scripta exekutatuta. Horretarako, honako hau idatzi beharko duzu terminalean:

```bash
python KartoiakSortu.py -N <kartoi kopurua> -n <kartoiko abesti kopurua> -a <abesti-zerrendaren fitxategiaren izena>
```

Hutsune bakoitzean zure balioak ordezkatu beharko dituzu; honela:

```bash
python KartoiakSortu.py -N 20 -n 12 -a fitxategiak/zerrenda_adibidea_2partida.txt
```

Hor ageri diren balioak nahitaez sartu beharrekoak dira, baina badira beste batzuk aukerakoak direnak:
- `-o <latexeko fitxategiaren izena>` -> Irteerako fitxategiaren izena aukeratzeko. Bestela, balio lehenetsia: `latex_kodea.txt`
- `-i <kartoien izenburua>` -> Kartoien gainean ageriko den testua. Bestela, balio lehenetsia: "BINGO MUSIKATUA"
- `-k` -> Hau gehituz gero, kartoiak koloretan inprimatuko dira.

Adibidez: 
```bash
python KartoiakSortu.py -N 20 -n 12 -a fitxategiak/zerrenda_adibidea_2partida.txt -o "kode_osoa.tex" -i "Bazkaloste musikatua!" -k
```

### Konpilatu kodea

Egin behar den gauza bakarra sortutako fitxategiko kode osoa kopiatu eta LaTeX konpilatzaile batean itsastea da. Era horretan bingoko kartoi guztiak biltzen dituen PDFa lortuko duzu.

Modurik errazena [Overleaf](https://www.overleaf.com/) plataforma erabiltzea da. Sortu kontua, hasi proiektu bat eta itsatsi kodea `.tex` fitxategi batean (sortu duzun fitxategia `.tex` erakoa bada, zuzenean igo dezakezu plataformara). Ondoren, konpilatu irudikatzeko, eta inprimatu.

Bi partidako bingoen kasuan, lehen partidako kartoiak orrien aurreko aldean inprimatuko dira, eta bigarrenekoak atzekoan. Kartoiek tamaina bera izango dute, eta zehazki bata bestearen atzean inprimatzeko moduan eginda daude; beraz, bi aldetatik inprimatu ahal izango duzu PDFa, eta ez da arazorik egongo mozterako orduan. Partida bakarrerako bada, aldiz, kontuz: orrialde bakarretik inprimatu beharko duzu PDFa!



## Adibideak, irudietan

Irudi hauetan ikus daiteke nolako itxura izango duten kartoiek, tamainaren eta koloreen arabera:

1. Koloretan, 12 abestiko kartoiak:
<img src="fitxategiak/.irudiak/adibidea_koloretan.jpeg" width="450">
Kasu honetan 5 kartoi inprimatuko dira orrialdeko.

2. Zuri-beltzean, 15 abestiko kartoiak:
<img src="fitxategiak/.irudiak/adibidea_zuribeltzean.jpeg" width="450">
Kasu honetan 4 kartoi inprimatuko dira orrialdeko.


Abesti kopuruaren arabera, orrialdeko 4 edo 5 kartoi ageriko dira, automatikoki.