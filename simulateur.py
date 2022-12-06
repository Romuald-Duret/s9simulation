import numpy as np

# Heure simulateur
HS = 0

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

ControleDispo = 0
ReparationDispo = 0

def ArriveeBus():
    global nbBus
    global HS
    nbBus +=  1
    lam = 80 # lambda = 3/4 | 1/lambda -> 4/3h donc 80 min
    res = np.random.exponential(lam, 1)


    #Ajout de l'evenement Arrivee bus dans l'echeancier
    InsertionEvenement((HS + res[0] , ArriveeBus))
    #Ajout de l'evenement ArriveeFileFC dans l'echeancier
    InsertionEvenement((HS,ArriveeFileC))

def AccesReparation(echeancier):
    global fileQr
    global ReparationDispo
    fileQr -= 1
    ReparationDispo += 1

    low = 168 # 2.8h = 168min
    high = 330 # 5.5h = 330min
    res = np.random.uniform(low,high,1)

    InsertionEvenement((HS + res[0], DepartReparation))

def ArriveeFileC():
    global  fileQc
    fileQc +=1
    # si la file est dispo
    if ControleDispo == 0:
        InsertionEvenement((HS,AccesControle))


def AccesControle():
    global fileQc
    global ReparationDispo
    fileQc -= 1
    ReparationDispo += 1

    low = 168  # 2.8h = 168min
    high = 330  # 5.5h = 330min
    res = np.random.uniform(low, high, 1)
    InsertionEvenement(())

def DepartControle():
    pass

def ArriveeFileR():
    pass

def AccesReparation():
    global fileQr
    global ReparationDispo
    fileQr -= 1
    ReparationDispo = 0

def DepartReparation():
    pass

def DebutSimulation():
    global echeancier
    global HS
    global HF
    echeancier.append((HS + np.random.exponential(80, 1)[0],ArriveeBus))
    echeancier.append((HF, FinSimulation))

def FinSimulation():
    pass

def MajAires():
    pass

def DepartReparation():
    pass

def InsertionEvenement(evenement : tuple):
    # fonction pour insérer l'évenement dans l'échéancier, implique de décaler les évènements après
    indice = -1
    global echeancier
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
    return {"temps_attente_moyen_avant_controle" : temps_attente_moyen_avant_controle,
            "temps_attente_moyen_avant_reparation" : temps_attente_moyen_avant_reparation,
            "taux_utilisation_centre_reparation" : taux_utilisation_centre_reparation
            }
if __name__ == "__main":




