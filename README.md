# BingoMusikatua - Bingo musikatuetarako kartoiak automatikoki sortzeko kodea!

Abesti-zerrenda baten fitxategia emanda, kartoiak latex-eko kodean idazten ditu, eta kode hori latex-eko konpilatzaile batean (Overleaf) itsastea besterik ez da behar.

## Nola erabili?

Lehenik eta behin, `python` erabilgarri izan behar da. Pythoneko scriptak erabiliko ditugu kartoien kodea sortzeko.

### Sortu kodea

Bi modutan egin daiteke:

#### Interaktiboki, Notebook bidez

Modu hau erabiltzeko, ireki `BingoMusikatuaNotebook.ipynb` fitxategia. Notebook honetan pausoz pauso joango da urratsak azaltzen. Bertan ageri diren balioak alda ditzakezu zuk nahi duzunaren arabera: abesti kopurua, kartoi kopurua...

Bingo-saiorako zenbat abesti aukeratu ez badakizu, lehen zatiak lagun diezazuke: zure datuak sartuta, batez bestean partida zenbagarren abestian amaituko den estimatzen da. Abesti bakoitzari eman nahi diozun luzeraren arabera kalkulatu ahal izango duzu zure partidaren gutxi gorabeherako iraupena!

Bigarren zatian, zure datuak sartuta, zuzenean sortu ahal izango duzu latex-eko kodearen fitxategia.

#### Zuzenean terminaletik

Zuzenean terminaletik ere egin daiteke, pythoneko scripta exekutatuta. Horretarako, honako hau idatzi beharko duzu terminalean:

```bash

python KartoiakSortu.py -N <kartoi kopurua> -n <kartoiko abesti kopurua> -a <abesti-zerrendaren fitxategiaren izena>
```

Hutsune bakoitzean zure balioak ordezkatu beharko dituzu; honela:

```bash
python KartoiakSortu.py -N 20 -n 12 -a fitxategiak/zerrenda_adibidea_2partida.txt
```

Hor ageri diren balioak nahitaez sartu beharrekoak dira, baina badira beste batzuk aukerakoak direnak:
- `-o <latexeko fitxategiaren izena>` -> Irteerako fitxategiaren izena aukeratzeko. Bestela, defektuz: `latex_kodea.txt`
- `-i <kartoien izenburua>` -> Kartoien gainean ageriko den testua. Bestela, defektuz: "BINGO MUSIKATUA"
- `-k` -> Hau gehituz gero, kartoiak koloretan inprimatuko dira.

Adibdiez: 
```bash
python KartoiakSortu.py -N 20 -n 12 -a fitxategiak/zerrenda_adibidea_2partida.txt -o "kode_osoa.tex" -i "Bazkaloste musikatua!" -k
```


### Konpilatu kodea

Egin behar den gauza bakarra sortutako fitxategiko kode osoa kopiatu eta latexeko konpilatzaile batean itsastea da. Era horretan kartoi guztiak biltzen dituen PDFa lortuko dugu.

Modurik errazena [Overleaf](https://www.overleaf.com/) plataforma erabiltzea da. Sortu kontua, hasi proiektu bat eta itsatsi kodea `.tex` fitxategi batean (sortu duzun fitxategia `.tex` erakoa bada, zuzenean igo dezakezu plataformara). Ondoren, konpilatu irudikatzeko, eta inprimatu.