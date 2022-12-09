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

tailleMoyenneFileC = 0
tailleMoyenneFileR = 0

# Variable quesition 3
blocageReparation = 0
aireQrBlocage = 0
blocageControle = 0
aireQcBlocage = 0

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
    global blocageControle

    fileQc -= 1
    ControleDispo += 1

    low = 15  # 00h15 = 15min
    high = 65  # 01h05 = 65min
    res = np.random.uniform(low, high, 1)
    InsertionEvenement((HS + res[0],DepartControle))

    if (HS+res[0])>=HF:
        blocageControle+=1

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
    global blocageReparation

    fileQr -= 1
    ReparationDispo += 1

    low = 168 # 02h48 = 168min
    high = 330 # 05h30 = 330min
    res = np.random.uniform(low,high,1)

    InsertionEvenement((HS + res[0], DepartReparation))

    # Modification Question 3
    if HS + res[0] > HF:
        blocageReparation+=1

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
    global aireQrBlocage
    global aireQcBlocage

    if blocageReparation == 2 and aireQrBlocage == 0:
        aireQrBlocage = aireQr
    if blocageControle == 1 and aireQcBlocage == 0:
        aireQcBlocage = aireQc
    aireQr += (D2 - D1) * fileQr
    aireQc += (D2 - D1) * fileQc
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
    global tailleMoyenneFileR
    global tailleMoyenneFileC
    global aireQrBlocage
    global aireQcBlocage

    echeancier.clear()
    tempsAttMoyCon = aireQc / nbBus
    tempsAttMoyRep = aireQr / nbBusRep
    tailleMoyenneFileR = aireQr / HF
    tailleMoyenneFileC = aireQc / HF
    tauxUtilRep = aireBr / (2*HF)
    print("temps_attente_moyen_avant_controle : ", tempsAttMoyCon,
            "temps_attente_moyen_avant_reparation : ", tempsAttMoyRep,
            "taux_utilisation_centre_reparation : ", tauxUtilRep,
            "taille_moyenne_file_reparation : ", tailleMoyenneFileR,
            "taille_moyenne_file_controle : ", tailleMoyenneFileC
    )

    if aireQrBlocage == 0:
        aireQrBlocage = aireQr
    if aireQcBlocage == 0:
        aireQcBlocage = aireQc
    tempsAttMoyCon = aireQcBlocage / nbBus
    tempsAttMoyRep = aireQrBlocage / nbBusRep
    tailleMoyenneFileR = aireQrBlocage / HF
    tailleMoyenneFileC = aireQcBlocage / HF
    tauxUtilRep = aireBr / (2 * HF)
    print("temps_attente_moyen_avant_controle : ", tempsAttMoyCon,
          "temps_attente_moyen_avant_reparation : ", tempsAttMoyRep,
          "taux_utilisation_centre_reparation : ", tauxUtilRep,
          "taille_moyenne_file_reparation : ", tailleMoyenneFileR,
          "taille_moyenne_file_controle : ", tailleMoyenneFileC
          )


if __name__ == "__main__":
    HS = 0

    InsertionEvenement((HS,DebutSimulation))
    while len(echeancier) > 0 :
        (date, evenement) = echeancier.pop(0)
        MajAires(HS,date)
        HS = date
        evenement()

"""
echeancierFile qui contient les tuples (HS, fileQr)
lastKey = 0 Variable qui indique l'indice dans dicBus du prochain bus à sortir
dicBus = {} Dictionnaire qui contient BUSi = (Hdébut, Hfin)
étatFile = 0
nbBus = 0
        #   Pour tous les éléments dans échancierFile:
        #   Si elem[1] > étatFile:
        #       Alors étatFile = elem[1]
        #       nbBus++
        #       dicBus[nbBus] = (elem[0],0)
        #       lastKey=nbBus
        #   Si elem[1] < etatFile:
        #       Alors étatFile = elem[1]
        #       dicBus[nbBus] = (dicBus[nbBus][0],elem[0])
        #       lastKey++
"""




