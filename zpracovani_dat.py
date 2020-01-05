import csv
import sys
import pandas as pd 

def remove_blanks(row):
    new_list = []
    for item in row:
        if item != "":
            new_list.append(item)
    return new_list

withoutBlanks = []

with open(sys.argv[1]) as openedFile:
	csvContent = csv.reader(openedFile, delimiter=';')
	for row in csvContent:
		rowWithoutBlanks = remove_blanks(row)
		if rowWithoutBlanks != []:
			withoutBlanks.append(rowWithoutBlanks)

#for i in range (0, len(withoutBlanks)):
	#print(withoutBlanks[i])

'''poradi = int(withoutBlanks[3][0])
print(poradi)'''

naklady = []

for x in range (0, len(withoutBlanks)):
	if withoutBlanks[x][0] == 'Varianta - ošetření':
		poradi = int(withoutBlanks[x+1][0])
		for i in range (x+2, len(withoutBlanks)):
			#print(withoutBlanks[i])
			posledni = len(withoutBlanks[i]) - 1
			if withoutBlanks[i][0] == 'Součet':	
				break
			elif '+' in withoutBlanks[i][0]:
				aplikovanePripravky = withoutBlanks[i][0].split('+')
				pocetPripravkuVAplikaci = len(aplikovanePripravky)
				for j in range (0, pocetPripravkuVAplikaci):
					aplikovanePripravkyBezMezer = []
					for item in aplikovanePripravky:
						item = item.strip()
						aplikovanePripravkyBezMezer.append(item)
					jednaAplikaceTemp = aplikovanePripravkyBezMezer[j].split(' ')
					#print(jednaAplikace)
					l = len(jednaAplikaceTemp)
					jednaAplikaceNazev = []
					for a in range (0, l-2):
						jednaAplikaceNazev.append(jednaAplikaceTemp[a])
					b = " ".join(jednaAplikaceNazev)
					#print(b)
					jednaAplikace = []
					jednaAplikace.insert(0, b)
					if jednaAplikaceTemp[l-1][0] == 'g':
						prevodNaKg = str(float(jednaAplikaceTemp[l-2].replace(",", "."))/1000).replace(".", ",")
						jednaAplikace.insert(1, prevodNaKg)
						jednaAplikace.insert(2, 'kg/ha')
					else:	
						jednaAplikace.insert(1, str(float(jednaAplikaceTemp[l-2].replace(",", "."))).replace(".", ","))
						jednaAplikace.insert(2, jednaAplikaceTemp[l-1])
					jednaAplikace.append(withoutBlanks[i][j+1])
					jednaAplikace.append(pocetPripravkuVAplikaci)
					if withoutBlanks[i][pocetPripravkuVAplikaci+2] == '300':
						typAplikace = 'kapalna'
					else:
						typAplikace = 'pevna'
					jednaAplikace.append(typAplikace)
					datum = withoutBlanks[i][posledni].split(' ')
					jednaAplikace.append(datum[0])
					if '-' in datum[2]:
						pomlcka = datum[2].find('-')
						jednaAplikace.append(datum[2][pomlcka-2:pomlcka])
						jednaAplikace.append(datum[2][pomlcka+1:pomlcka+3])
					else:
						jednaAplikace.append(datum[2][0:2])
						jednaAplikace.append(datum[2][0:2])
					jednaAplikace.insert(0, poradi)
					naklady.append(jednaAplikace)
			else:
				if len(withoutBlanks[i]) == 1:
					continue
				else:	
					pocetPripravkuVAplikaci = 1
					jednaAplikaceTemp = withoutBlanks[i][0].split(' ')
					#print(jednaAplikaceTemp)
					l = len(jednaAplikaceTemp)
					jednaAplikaceNazev = []
					for a in range (0, l-2):
						jednaAplikaceNazev.append(jednaAplikaceTemp[a])
					b = " ".join(jednaAplikaceNazev)
					#print(b)
					jednaAplikace = []
					jednaAplikace.insert(0, b)
					if jednaAplikaceTemp[l-1][0] == 'g':
						prevodNaKg = str(float(jednaAplikaceTemp[l-2].replace(",", "."))/1000).replace(".", ",")
						jednaAplikace.insert(1, prevodNaKg)
						jednaAplikace.insert(2, 'kg/ha')
					else:	
						jednaAplikace.insert(1, str(float(jednaAplikaceTemp[l-2].replace(",", "."))).replace(".", ","))
						jednaAplikace.insert(2, jednaAplikaceTemp[l-1])
					jednaAplikace.append(withoutBlanks[i][1])
					jednaAplikace.append(pocetPripravkuVAplikaci)
					if withoutBlanks[i][3] == '300':
						typAplikace = 'kapalna'
					else:
						typAplikace = 'pevna'
					jednaAplikace.append(typAplikace)
					datum = withoutBlanks[i][posledni].split(' ')
					jednaAplikace.append(datum[0])
					if '-' in datum[2]:
						pomlcka = datum[2].find('-')
						jednaAplikace.append(datum[2][pomlcka-2:pomlcka])
						jednaAplikace.append(datum[2][pomlcka+1:pomlcka+3])
					else:
						jednaAplikace.append(datum[2][0:2])
						jednaAplikace.append(datum[2][0:2])
					jednaAplikace.insert(0, poradi)
					naklady.append(jednaAplikace)
	else:
		continue

#for item in naklady:
	#print(item)   

df = pd.DataFrame(naklady)

print(df)	

df.to_csv('zpracovano_kodovani.csv', encoding='windows-1250', header=True, mode='a')
#df.to_csv('zpracovano.csv', header=False, mode='a')
