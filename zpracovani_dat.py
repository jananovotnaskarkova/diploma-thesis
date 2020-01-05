import csv
import sys
import pandas as pd 

# fce odstraneni prazdnych bunek
def remove_blanks(row):
    new_list = []
    for item in row:
        if item != "":
            new_list.append(item.strip())
    return new_list

withoutBlanks = []

# odstraneni prazdnych bunek 
with open(sys.argv[1]) as openedFile:
	csvContent = csv.reader(openedFile, delimiter=';')
	for row in csvContent:
		rowWithoutBlanks = remove_blanks(row)
		if rowWithoutBlanks != []:
			withoutBlanks.append(rowWithoutBlanks)

naklady = [] # finalni seznam

# prochazeni radku souboru
for x in range (0, len(withoutBlanks)):

	# hledany blok textu zacina vzdy textem "varianta..."
	if withoutBlanks[x][0] == 'Varianta - ošetření':
		poradi = int(withoutBlanks[x+1][0]) # cislo varianty

		# prochazeni bunek v radku
		for i in range (x+2, len(withoutBlanks)):

			#print(withoutBlanks[i]) # kontrolni tisk
			posledni = len(withoutBlanks[i]) - 1 # pocet bunek v radku

			# hledany blok textu konci vzdy textem "soucet"
			if withoutBlanks[i][0] == 'Součet':	
				break

			# "+" znamena, ze bylo aplikovano vice pripravku v tankmixu	
			elif '+' in withoutBlanks[i][0]:

				# deleni tankmixu podle "+" a zjisteni poctu pripravku
				aplikovanePripravky = withoutBlanks[i][0].split('+')
				pocetPripravkuVAplikaci = len(aplikovanePripravky)

				# odstraneni mezer na zacatku a na konci				
				aplikovanePripravkyBezMezer = []
				for item in aplikovanePripravky:
					item = item.strip()
					aplikovanePripravkyBezMezer.append(item)

				# prochazeni pripravku v tankmixu
				for j in range (0, pocetPripravkuVAplikaci):

					# deleni udaju podle mezer
					jednaAplikaceTemp = aplikovanePripravkyBezMezer[j].split(' ')
					l = len(jednaAplikaceTemp)

					# slouceni viceslovnych nazvu
					jednaAplikaceNazev = []
					for a in range (0, l-2):
						jednaAplikaceNazev.append(jednaAplikaceTemp[a])
					b = " ".join(jednaAplikaceNazev)

					# vytvareni seznamu udaju k jedne aplikaci
					jednaAplikace = []
					jednaAplikace.insert(0, b) # vlozeni nazvu pripravku
					if jednaAplikaceTemp[l-1][0] == 'g': # prevod gramu na kilogramy
						prevodNaKg = str(float(jednaAplikaceTemp[l-2].replace(",", "."))/1000).replace(".", ",") #chci desetinnou carku
						jednaAplikace.insert(1, prevodNaKg) # vlozeni mnozstvi
						jednaAplikace.insert(2, 'kg/ha') # vlozeni jednotek
					else:	
						jednaAplikace.insert(1, str(float(jednaAplikaceTemp[l-2].replace(",", "."))).replace(".", ",")) # vlozeni mnozstvi, chci desetinnou carku
						jednaAplikace.insert(2, jednaAplikaceTemp[l-1]) # vlozeni jednotek
					jednaAplikace.append(withoutBlanks[i][j+1]) # vlozeni ceny
					jednaAplikace.append(pocetPripravkuVAplikaci) # vlozeni poctu pripravku
					if withoutBlanks[i][pocetPripravkuVAplikaci+2] == '300':
						typAplikace = 'kapalna'
					else:
						typAplikace = 'pevna'
					jednaAplikace.append(typAplikace) # vlozeni typu aplikace
					datum = withoutBlanks[i][posledni].split(' ')
					jednaAplikace.append(datum[0]) # vlozeni data
					if '-' in datum[2]:
						pomlcka = datum[2].find('-')
						jednaAplikace.append(datum[2][pomlcka-2:pomlcka]) # vlozeni bbch od
						jednaAplikace.append(datum[2][pomlcka+1:pomlcka+3]) # vlozeni bbch do
					else:
						jednaAplikace.append(datum[2][0:2]) # vlozeni bbch od
						jednaAplikace.append(datum[2][0:2]) # vlozeni bbch do
					jednaAplikace.insert(0, poradi) # vlozeni vylosovaneho poradi na zacatek

					# vlozeni do finalniho seznamu
					naklady.append(jednaAplikace)
			
			# tady neni plus, tj. byl aplikovan pouze jeden pripravek, nebo je zde nazev odrudy
			else:

				# pokud je delka withoutBlanks[i] 1, jedna se o nazev odrudy
				if len(withoutBlanks[i]) == 1:
					continue

				# taky byl aplikovan pouze jeden pripravek
				else:	
					pocetPripravkuVAplikaci = 1

					# deleni udaju podle mezer
					jednaAplikaceTemp = withoutBlanks[i][0].split(' ')
					l = len(jednaAplikaceTemp)

					# slouceni viceslovnych nazvu
					jednaAplikaceNazev = []
					for a in range (0, l-2):
						jednaAplikaceNazev.append(jednaAplikaceTemp[a])
					b = " ".join(jednaAplikaceNazev)
					
					# vytvareni seznamu udaju k jedne aplikaci
					jednaAplikace = []
					jednaAplikace.insert(0, b) # vlozeni nazvu pripravku
					if jednaAplikaceTemp[l-1][0] == 'g': # prevod gramu na kilogramy
						prevodNaKg = str(float(jednaAplikaceTemp[l-2].replace(",", "."))/1000).replace(".", ",") #chci desetinnou carku
						jednaAplikace.insert(1, prevodNaKg) # vlozeni mnozstvi
						jednaAplikace.insert(2, 'kg/ha') # vlozeni jednotek
					else:	
						jednaAplikace.insert(1, str(float(jednaAplikaceTemp[l-2].replace(",", "."))).replace(".", ",")) # vlozeni mnozstvi, chci desetinnou carku
						jednaAplikace.insert(2, jednaAplikaceTemp[l-1]) # vlozeni jednotek
					jednaAplikace.append(withoutBlanks[i][1]) # vlozeni ceny
					jednaAplikace.append(pocetPripravkuVAplikaci) # vlozeni poctu pripravku
					if withoutBlanks[i][3] == '300':
						typAplikace = 'kapalna'
					else:
						typAplikace = 'pevna'
					jednaAplikace.append(typAplikace) # vlozeni typu aplikace
					datum = withoutBlanks[i][posledni].split(' ')
					jednaAplikace.append(datum[0]) # vlozeni data
					if '-' in datum[2]:
						pomlcka = datum[2].find('-')
						jednaAplikace.append(datum[2][pomlcka-2:pomlcka]) # vlozeni bbch od
						jednaAplikace.append(datum[2][pomlcka+1:pomlcka+3]) # vlozeni bbch do
					else:
						jednaAplikace.append(datum[2][0:2]) # vlozeni bbch od
						jednaAplikace.append(datum[2][0:2]) # vlozeni bbch do
					jednaAplikace.insert(0, poradi) # vlozeni vylosovaneho poradi na zacatek

					# vlozeni do finalniho seznamu
					naklady.append(jednaAplikace)

	# radky, ktere nezacinaji "varianta..." preskakuji 				
	else:
		continue

df = pd.DataFrame(naklady)

print(df)	

#print(df.to_string())

#df.to_csv('zpracovano.csv', header=True, mode='a')
#df.to_csv('zpracovano.csv', header=False, mode='a')
