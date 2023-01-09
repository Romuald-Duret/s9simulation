import numpy as np
import random
import csv

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

echeancierDepartFileR = []
echeancierArriveeFileR = []

echeancierDepartFileC = []
echeancierArriveeFileC = []
#représente l'état de disponibilité de la file de controle peut prendre les valeurs
ControleDispo = 0
ReparationDispo = 0

tempsAttMoyCon =0
tempsAttMoyRep = 0
tauxUtilRep = 0

tailleMoyenneFileC = 0
tailleMoyenneFileR = 0

# Variable question 3
blocageReparation = 0
aireQrBlocage = 0
blocageControle = 0
aireQcBlocage = 0

# Variable question 5
nbBusControle = 0
nbStop = 200
tempsAttenteControle = []
tempsAttenteControleGlobal = []


def Get_Max_Time():
    global echeancierDepartFileC
    global echeancierArriveeFileC
    delais_attente_frep =  []
    delais_attente_fcont = []
    max_attente_c = 0
    max_attente_r = 0
    indice_max_r = 0
    indice_max_c = 0
    global  echeancierDepartFileR
    global echeancierArriveeFileR

    for index_arrivee_c, arrivee_file_c in enumerate(echeancierArriveeFileC):
        nb_depart = arrivee_file_c[1]
        for depart_file_c in echeancierDepartFileC:
            if depart_file_c[0] >= arrivee_file_c[0]:
                nb_depart -= 1
            if nb_depart == 0 and depart_file_c[0] >= arrivee_file_c[0]:
                indice_max_c = index_arrivee_c if depart_file_c[0] - arrivee_file_c[0] > max_attente_c else indice_max_c
                max_attente_c = depart_file_c[0] - arrivee_file_c[0] if depart_file_c[0] - arrivee_file_c[0] > max_attente_c else max_attente_c
                break
    for index_arrivee_r, arrive_file_r in enumerate(echeancierArriveeFileR):
        nb_depart = arrive_file_r[1]
        for dep_r in echeancierDepartFileR:
            if dep_r[0] >= arrive_file_r[0]:
                nb_depart -= 1
            if nb_depart == 0 and dep_r[0] >= arrive_file_r[0]:
                indice_max_r = index_arrivee_r if dep_r[0] - arrive_file_r[0] > max_attente_r else indice_max_r
                max_attente_r = dep_r[0] - arrive_file_r[0] if dep_r[0] - arrive_file_r[0] > max_attente_r else max_attente_r
                break
    return {indice_max_c: max_attente_c, indice_max_r: max_attente_r}

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
    global echeancierArriveeFileC
    global tempsAttenteControle

    tempsAttenteControle.append(HS)
    fileQc +=1
    echeancierArriveeFileC.append((HS, fileQc))
    # si la file est dispo
    if ControleDispo == 0:
        InsertionEvenement((HS,AccesControle))

def AccesControle():
    global fileQc
    global ControleDispo
    global blocageControle
    global echeancierDepartFileC
    global nbBusControle
    global tempsAttenteControle

    tempsAttenteControle[nbBusControle] = HS - tempsAttenteControle[nbBusControle]
    nbBusControle += 1

    if (nbBusControle == nbStop):
        InsertionEvenement((HS, FinSimulation))

    fileQc -= 1
    echeancierDepartFileC.append((HS, fileQc))
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
    global echeancierArriveeFileR
    fileQr += 1
    nbBusRep += 1
    echeancierArriveeFileR.append((HS, fileQr))
    if ReparationDispo < 2 :
        InsertionEvenement((HS,AccesReparation))

def AccesReparation():
    global fileQr
    global ReparationDispo
    global blocageReparation
    global  echeancierDepartFileR
    fileQr -= 1
    echeancierDepartFileR.append((HS, fileQr))
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
    InsertionEvenement((HS, ArriveeBus))

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

    tempsAttenteControleGlobal.append(tempsAttenteControle)




if __name__ == "__main__":

    nbSimu = 1000

    for i in range(nbSimu):
        HS = 0
        nbBus = 0
        nbBusRep = 0
        aireQc = 0
        aireQr = 0
        echeancier = []
        aireBr = 0
        fileQc = 0
        fileQr = 0
        echeancierDepartFileR = []
        echeancierArriveeFileR = []
        echeancierDepartFileC = []
        echeancierArriveeFileC = []
        ControleDispo = 0
        ReparationDispo = 0
        tempsAttMoyCon = 0
        tempsAttMoyRep = 0
        tauxUtilRep = 0
        tailleMoyenneFileC = 0
        tailleMoyenneFileR = 0
        blocageReparation = 0
        aireQrBlocage = 0
        blocageControle = 0
        aireQcBlocage = 0
        nbBusControle = 0
        tempsAttenteControle = []

        InsertionEvenement((HS, DebutSimulation))
        while len(echeancier) > 0:
            (date, evenement) = echeancier.pop(0)
            MajAires(HS, date)
            HS = date
            evenement()
        tmax = Get_Max_Time()
        print(f"les temps d'attentes maximums sont respectivement pour les files de contrôle et de réparation : {tmax.values()}")

    csvFile = open("question6.csv", "w")
    writer = csv.writer(csvFile)
    writer.writerows(tempsAttenteControleGlobal)
    csvFile.close()