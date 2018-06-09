import re
import scipy.stats as stats
import numpy as np
import pandas as pd
from pandas import DataFrame
from openpyxl.workbook import Workbook

## Openen  en inlezen Waardenbestand
WaardenFile = open("QTLwaarden(1).qua", "r").readlines()


## Filteren van Waardendata tot een lijst met alleen waarden.
WaardenLijst = []
pLijst = []
fLijst = []
naamLijst =[]
for line in WaardenFile[8:]:
    RawWaarden = line.replace("\n", "").replace("-","0")
    SplitWaarden = RawWaarden.split("\t")
    WaardenLijst.append(SplitWaarden[1])

IntWaardenLijst = []
IntWaardenLijst = [round(float(x),10) for x in WaardenLijst]                                                            #Maakt van stringlijst een intlijst


## Openen en inlezen van Markerbestand.
with open("QTLgroepen.loc", "r") as MarkerFile:

    file = MarkerFile.readline()
    while file != "":
        file = MarkerFile.readline()
        if "(a,b)" in file:
            naam = file.split("(a,b)")
            naamLijst.append(naam[0])

    MarkerFile.seek(0)
## Markerdata op 1 regel, waarna gesplit in een lijst.
    RawMarkerData = MarkerFile.read().replace("\n", "").replace(" ", "").replace("\t", "")
    print(RawMarkerData)


    SplitMarkerData = RawMarkerData.split("(a,b)")
    RawMarkerLijst = SplitMarkerData[1:]


ANOVALijst = []
## Wegfilteren van ongewenste karakters.
for item in RawMarkerLijst:
    NoCapitals = re.sub(r'[A-Z].*', '', item)
    NoAB = re.sub(r'[c-z].*', '', NoCapitals)
    NoNumber = re.sub(r'[0-9]', '', NoAB)
    NoExtra = NoNumber.replace(";","")

## Doorloop abseq en voegt waarde toe.
    LijstA = []
    LijstB = []


    WaardenLijstindex = 0
    for ABitem in NoExtra:
        if ABitem == "a":
            LijstA.append(IntWaardenLijst[WaardenLijstindex])
            WaardenLijstindex = WaardenLijstindex + 1
            #print(LijstA)
        elif ABitem == "b":
            LijstB.append(IntWaardenLijst[WaardenLijstindex])
            WaardenLijstindex = WaardenLijstindex + 1
            #print(LijstB)
        else:
            WaardenLijstindex = WaardenLijstindex + 1
            continue

    statistic, pvalue = stats.f_oneway(LijstA, LijstB)
    pLijst.append(pvalue)
    fLijst.append(statistic)

l1 = pLijst
l2 =  fLijst
l3 = naamLijst
d = {'Marker Naam': l3, 'P-value': l1,'F-value':l2}
df = pd.DataFrame(data=d)
writer = pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()


