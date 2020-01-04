import xml.etree.ElementTree as et
import pandas as pd

# soubor stazeny z http://eagri.cz/public/app/eagricis/Forms/Lists/Agricultural/PorListsPage.aspx
fileP = 'CiselnikPor.xml'

tree = et.parse(fileP)
root = tree.getroot()
path = root[0]

# tagy, ktere potrebuji pri prochazeni souboru
polozkaTag = '{http://www.ccv.cz/EPH_GCP01E}POLOZKA'
rozhodnutiTag = '{http://www.ccv.cz/EPH_GCP01E}ROZHODNUTI'
ulTag = '{http://www.ccv.cz/EPH_GCP01E}UL'
udajeTag = '{http://www.ccv.cz/EPH_GCP01E}UDAJE'
udajTag = '{http://www.ccv.cz/EPH_GCP01E}UDAJ'
zkrTag = '{http://www.ccv.cz/EPH_GCP01E}ZKR'
skupulTag = '{http://www.ccv.cz/EPH_GCP01E}SKUP_UL'
nazevenTag = '{http://www.ccv.cz/EPH_GCP01E}NAZEV_EN'

# seznam dat, ktera chci ziskat
header = ['POLOZKA_ID',
'POLOZKA_OJP',
'POLOZKA_STAV',
'POLOZKA_D_POUZITELNY_DO',
'ROZHODNUTI_B_FCE',
'ROZHODNUTI_EKO',
'UL_ID',
'UL_NAZEV',
'UL_NAZEV_EN',
'UL_MNOZSTVI',
'UL_MJ',
'UL_SKUP_UL',
'UDAJE_Zvláštní rizika pro lidské zdraví',
'UDAJE_Bezpečnostní opatření',
'UDAJE_Další označení',
'UDAJE_Riziko pro vodní organismy',
'UDAJE_Riziko pro ptáky',
'UDAJE_Riziko pro savce',
'UDAJE_Riziko pro včely',
'UDAJE_Riziko pro ostatní necílové členovce',
'UDAJE_Riziko pro půdní makroorganismy',
'UDAJE_Riziko pro půdní mikroorganismy',
'UDAJE_Riziko pro necílové rostliny',
'UDAJE_Riziko pro životní prostředí',
'UDAJE_Ochranná pásma vod',
'UDAJE_Další označení - fyz. chem. vlastnosti',
'UDAJE_Biologická funkce',
'UDAJE_Úprava = Typ formulace',
'UDAJE_Klasifikace (CLP)',
'UDAJE_Výstražné symboly nebezpečí dle CLP',
'UDAJE_Signální slova',
'UDAJE_H věty - úplný seznam',
'UDAJE_EUH věty']

listP = [] # finalni seznam
listTemp = [] # pomocny seznam

# vkladam hlavicku sloupcu
listP.append(header)

for child in path:

    dictTemp = {} # pomocny slovnik

    # data POLOZKA
    polozka = child
    for child in polozka:

        # data ROZHODNUTI
        if child.tag == rozhodnutiTag:
            rozhodnuti = child
            for child in rozhodnuti:

                # data UL    
                if child.tag == ulTag:
                    ul = child
                    for child in ul: 
                        text = 'UL_' + child.tag[child.tag.find('}')+1:]
                        if child.tag == skupulTag:
                            skupul = child
                            for child in skupul:
                                if child.tag == nazevenTag:
                                    if text in header:
                                        if text in dictTemp:
                                            dictTemp[text].add(child.text.strip())
                                        else:
                                            dictTemp[text] = set()
                                            dictTemp[text].add(child.text.strip())
                        else:    
                            text = 'UL_' + child.tag[child.tag.find('}')+1:]
                            if text in header:
                                if text in dictTemp:
                                    dictTemp[text].add(child.text.strip())
                                else:
                                    dictTemp[text] = set()
                                    #dictTemp[text] = [child.text.strip()]
                                    dictTemp[text].add(child.text.strip())
                
                # data UDAJE 
                elif child.tag == udajeTag:
                    udaje = child
                    for child in udaje:
                        if child.tag == udajTag:
                            text = 'UDAJE_' + child.text.strip()
                        if child.tag == zkrTag:
                            textZkr = child.text.strip()
                            if (textZkr == '- -') or (textZkr == '-'):
                                break
                            if text in header:
                                if text in dictTemp:
                                    dictTemp[text].add(textZkr)
                                else:
                                    dictTemp[text] = set()
                                    dictTemp[text].add(textZkr)

                else:
                    text = 'ROZHODNUTI_' + child.tag[child.tag.find('}')+1:]
                    if text in header:
                        dictTemp[text] = child.text.strip()

        else:
            text = 'POLOZKA_' + child.tag[child.tag.find('}')+1:]
            if text in header:
                dictTemp[text] = child.text.strip()

    # serazeni do stejneho poradi jako je v 'header'            
    listTemp = []
    for item in header:
        if item in dictTemp.keys():
            listTemp.append(dictTemp[item])
        else:
            listTemp.append('')

    # pripojeni k finalnimu seznamu        
    listP.append(listTemp)

# dataframe + upravy
df = pd.DataFrame(listP)
df.columns = df.iloc[0]
df = df.iloc[3:,]

print(df)  

# tisk do csv
df.to_csv('registrP.csv', encoding='windows-1250', sep=';', mode='w')
