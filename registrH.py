import xml.etree.ElementTree as et
import pandas as pd

# soubor stazeny z http://eagri.cz/public/app/eagricis/Forms/Lists/Agricultural/HnojivaListPage.aspx
fileH = 'CiselnikHnojiv.xml'

listH = [] # finalni seznam

tree = et.parse(fileH)
root = tree.getroot()
path = root[0]

# vkladam nazvy sloupcu
listH.append(list(path[1].attrib))

# vkladam data
for child in path:
    a = dict(child.attrib)
    listH.append(list(a.values()))

# dataframe + upravy
df = pd.DataFrame(listH)
df.columns = df.iloc[0]
df = df.iloc[2:,:41]

# tisk do csv (desetinna tecka)
df.to_csv('registrHDot.csv', encoding='windows-1250', header=True, sep=';', mode='w')

columnsNumberValues = ['CH_N', 'CH_P', 'CH_K', 'CH_CA', 'CH_MG', 'CH_NA', 'CH_S', 'CH_CL', 'CH_SL', 'CH_ZN', 'CH_CU', 'CH_FE', 'CH_B', 'CH_MN', 'CH_MO', 'CH_SE', 'CH_PH_OD', 'CH_PH_DO', 'CH_EL_V', 'KOEFPREP']

# uprava desetinne tecky na carku
for item in columnsNumberValues:
    df[item] = df[item].astype(str)
    df[item] = [x.replace('.', ',') for x in df[item]]

print(df)

# tisk do csv (desetinna carka)
df.to_csv('registrHCom.csv', encoding='windows-1250', header=True, sep=';', mode='w')

