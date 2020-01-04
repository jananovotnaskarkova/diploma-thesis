import xml.etree.ElementTree as et
import pandas as pd

fileH = 'CiselnikHnojiv.xml'
listH = []

tree = et.parse(fileH)
root = tree.getroot()

path = root[0]

listH.append(list(path[1].attrib))

for child in path:
    a = dict(child.attrib)
    listH.append(list(a.values()))

df = pd.DataFrame(listH)

df.columns = df.iloc[0]
df = df.iloc[2:,:41]

df.to_csv('registrHDot.csv', encoding='windows-1250', header=True, sep=';', mode='w')

columnsNumberValues = ['CH_N', 'CH_P', 'CH_K', 'CH_CA', 'CH_MG', 'CH_NA', 'CH_S', 'CH_CL', 'CH_SL', 'CH_ZN', 'CH_CU', 'CH_FE', 'CH_B', 'CH_MN', 'CH_MO', 'CH_SE', 'CH_PH_OD', 'CH_PH_DO', 'CH_EL_V', 'KOEFPREP']

for item in columnsNumberValues:
    df[item] = df[item].astype(str)
    df[item] = [x.replace('.', ',') for x in df[item]]

df.to_csv('registrHCom.csv', encoding='windows-1250', header=True, sep=';', mode='w')

print(df)