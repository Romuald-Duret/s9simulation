import numpy as np

# Heure simulateur
HS = 0

# NbBus
nbBus = 0

# NbBusRep
nbBusRep = 0

# Echeancier
echeancier = []

# Aire queue centre de controle
aireQc = 0

# Aire queue centre de réparation
aireQb = 0

# Taux d'utilisation du centre de réparation
aireBr = 0

def ArriveeBus():
    lam = 80 # lambda = 3/4 | 1/lambda -> 4/3h donc 80 min
    res = np.random.exponential(lam, 1)
    print(res)

def AccesReparation():
    low = 168 # 2.8h = 168min
    high = 330 # 5.5h = 330min
    res = np.random.uniform(low,high,1)
    print(res)

AccesReparation()