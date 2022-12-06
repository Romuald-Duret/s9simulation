import numpy as np
import random
global echeancier
global HS
global HF
global nbBus
global nbBusRep
global ReparationDispo
global aireQr
global aireBr
global fileQc
global fileQr
global ControleDispo
global aireQc
global duree

# Heure simulateur
HS = 0
# Heure de fin
HF = 2400
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

    nbBus +=  1
    lam = 80 # lambda = 3/4 | 1/lambda -> 4/3h donc 80 min
    res = np.random.exponential(lam, 1)


    #Ajout de l'evenement Arrivee bus dans l'echeancier
    InsertionEvenement((HS + res[0] , ArriveeBus))
    #Ajout de l'evenement ArriveeFileFC dans l'echeancier
    InsertionEvenement((HS,ArriveeFileC))

def AccesReparation(echeancier):
    fileQr -= 1
    ReparationDispo += 1

    low = 168 # 2.8h = 168min
    high = 330 # 5.5h = 330min
    res = np.random.uniform(low,high,1)

    InsertionEvenement((HS + res[0], DepartReparation))

def ArriveeFileC():
    fileQc +=1
    # si la file est dispo
    if ControleDispo == 0:
        InsertionEvenement((HS,AccesControle))


def AccesControle():
    fileQc -= 1
    ReparationDispo += 1

    low = 168  # 2.8h = 168min
    high = 330  # 5.5h = 330min
    res = np.random.uniform(low, high, 1)
    InsertionEvenement(())

def DepartControle():
    ControleDispo = 0
    if fileQc > 0 :
        InsertionEvenement((HS, AccesControle))

    rand = random.random()
    print(rand)
    if rand < 0.30 :
        InsertionEvenement((HS,ArriveeFileR))

def ArriveeFileR():
    global nbBusRep
    fileQr += 1
    nbBusRep += 1
    if ReparationDispo < 2 :
        InsertionEvenement((HS,AccesReparation))

def AccesReparation():
    fileQr -= 1
    ReparationDispo += 1
    low = 126  # 2.1h = 126min
    high = 270  # 4.5h = 270min
    res = np.random.uniform(low, high, 1)

    InsertionEvenement((HS + res[0], DepartReparation))


def DepartReparation():
    ReparationDispo -= 1
    if fileQr > 0:
        InsertionEvenement((HS,AccesReparation))

def DebutSimulation():
    nbBus = 0
    nbBusRep=0
    aireQc = 0
    aireQr = 0
    aireBr = 0
    fileQc = 0
    fileQr = 0
    ReparationDispo = 0
    ControleDispo = 0

    InsertionEvenement((HF, FinSimulation))
    InsertionEvenement((HS + np.random.exponential(80, 1)[0],ArriveeBus))

    print("insertion de fin ok")
def FinSimulation():
    echeancier = []

    tempsAttMoyCon = aireQc/nbBus
    tempsAttMoyRep = aireQr/nbBusRep
    tauxUtilRep = aireBr/(2*duree)



def MajAires(D1, D2):
    aireQc += (D2 - D1)*fileQc
    aireQr += (D2 - D1)* fileQr
    aireBr += (D2 - D1)* ReparationDispo


def InsertionEvenement(evenement : tuple):
    # fonction pour insérer l'évenement dans l'échéancier, implique de décaler les évènements après
    indice = -1

    if len(echeancier) == 0 :
        echeancier.insert(0, evenement)
        print("insertion début ok ")

    elif len(echeancier) == 1 :
        echeancier.insert(1, evenement)
        print("insertion début ok ")

    else :
        for i in range(len(echeancier)):
            if echeancier[i][0] > evenement[0]:
                indice = i
        if indice == -1:
            print("Erreur, insertion failed")
        else:
            echeancier.insert(i, evenement)

def FinSimulation():
    echeancier.clear()
    temps_attente_moyen_avant_controle = aireQc / nbBus
    temps_attente_moyen_avant_reparation = aireQr / nbBusRep
    taux_utilisation_centre_reparation = aireBr / (2*160)
    print("temps_attente_moyen_avant_controle : ", tempsAttMoyCon,
            "temps_attente_moyen_avant_reparation : ", tempsAttMoyRep,
            "taux_utilisation_centre_reparation : ", tauxUtilRep
    )


if __name__ == "__main__":
    HS = 0
    InsertionEvenement((HS,DebutSimulation))
    loop_counter = 0
    while loop_counter < len(echeancier) :
        echeancier[loop_counter][1]()

        loop_counter+=1







