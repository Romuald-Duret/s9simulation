import numpy as np
import random

# Heure simulateur
HS = 0
# Heure de fin
HF = 240*60
duree = HF - HS

# NbBus
nbBus = 0

# NbBusRep
nbBusRep = 0

# Aire queue centre de controle
aireQc = 0

# Aire queue centre de réparation
aireQr = 0

echeancier = []
# Taux d'utilisation du centre de réparation
aireBr = 0

fileQc = 0
fileQr = 0

#représente l'état de disponibilité de la file de controle peut prendre les valeurs
ControleDispo = 0
ReparationDispo = 0

tempsAttMoyCon =0
tempsAttMoyRep = 0
tauxUtilRep = 0

def ArriveeBus():
    global nbBus

    nbBus +=  1
    lam = 45
    res = np.random.exponential(lam, 1)


    #Ajout de l'evenement Arrivee bus dans l'echeancier
    InsertionEvenement((HS + res[0] , ArriveeBus))
    #Ajout de l'evenement ArriveeFileFC dans l'echeancier
    InsertionEvenement((HS,ArriveeFileC))

def ArriveeFileC():
    global fileQc

    fileQc +=1
    # si la file est dispo
    if ControleDispo == 0:
        InsertionEvenement((HS,AccesControle))

def AccesControle():
    global fileQc
    global ControleDispo

    fileQc -= 1
    ControleDispo += 1

    low = 15  # 00h15 = 15min
    high = 65  # 01h05 = 65min
    res = np.random.uniform(low, high, 1)
    InsertionEvenement((HS + res[0],DepartControle))

def DepartControle():
    global ControleDispo

    ControleDispo -= 1
    if fileQc > 0 :
        InsertionEvenement((HS, AccesControle))

    rand = random.random()
    if rand < 0.30 :
        InsertionEvenement((HS, ArriveeFileR))

def ArriveeFileR():
    global nbBusRep
    global fileQr

    fileQr += 1
    nbBusRep += 1
    if ReparationDispo < 2 :
        InsertionEvenement((HS,AccesReparation))

def AccesReparation():
    global fileQr
    global ReparationDispo

    fileQr -= 1
    ReparationDispo += 1

    low = 168 # 02h48 = 168min
    high = 330 # 05h30 = 330min
    res = np.random.uniform(low,high,1)

    InsertionEvenement((HS + res[0], DepartReparation))

def DepartReparation():
    global ReparationDispo

    ReparationDispo -= 1

    if fileQr > 0:
        InsertionEvenement((HS,AccesReparation))

def DebutSimulation():
    InsertionEvenement((HF, FinSimulation))
    InsertionEvenement((HS + np.random.exponential(80, 1)[0],ArriveeBus))

    print("insertion de fin ok")

def MajAires(D1, D2):
    global aireQc
    global aireQr
    global aireBr

    aireQc += (D2 - D1)* fileQc
    aireQr += (D2 - D1)* fileQr
    aireBr += (D2 - D1)* ReparationDispo

def getKey(element):
    return element[0]

def InsertionEvenement(evenement : tuple):
    global echeancier

    echeancier.insert(0, evenement)
    echeancier.sort(key=getKey)

def FinSimulation():
    global echeancier
    global tempsAttMoyRep
    global tempsAttMoyCon
    global tauxUtilRep

    echeancier.clear()
    tempsAttMoyCon = aireQc / nbBus
    tempsAttMoyRep = aireQr / nbBusRep
    tauxUtilRep = aireBr / (2*HF)
    print("temps_attente_moyen_avant_controle : ", tempsAttMoyCon,
            "temps_attente_moyen_avant_reparation : ", tempsAttMoyRep,
            "taux_utilisation_centre_reparation : ", tauxUtilRep
    )


if __name__ == "__main__":
    HS = 0

    InsertionEvenement((HS,DebutSimulation))
    while len(echeancier) > 0 :
        (date, evenement) = echeancier.pop(0)
        print((date,evenement))
        MajAires(HS,date)
        HS = date
        evenement()







