import numpy as np
import  scipy.stats as scp
import matplotlib.pyplot as plt
import  pandas as pd

df = pd.read_table('DonneesControle.txt',header=None,sep=" ")
print(df)
#on récupere la moyenne pour estimer le parametre lamda de la loi exponentielle

valMax = df[1].max()
valMin = df[1].min()
print("Max : ", valMax)
print("Min : ", valMin)
listIA = df[0].values
listC = df[1].values
nbElem = 0

"""""
for i in range(len(listIA)):
    listIA[i] *= listIA[i]
    listC[i] *= listC[i]
    nbElem += 1
"""""
#mean, var, skew, kurt = chi2.stats(df[1], moments='mvsk')
interarrive = []
for i in range(0, 228):
    if i == 0 :
        interarrive.append(df[0][i])
    else :
        inter = df[0][i]-df[0][i-1]
        interarrive.append(inter)
        print(inter)
#plt.figure(figsize=(12,8))
#plt.hist(df[], bins=100, density=True)
#plt.plot(df[0],label="cas reel")
#plt.title("cas reel inter")
#plt.show()


### Histogramme des données
sorted = df[1].sort_values()
plt.figure(figsize=(12,8))
plt.hist(df[1], bins=100, density=True)
#plt.plot(df[0],label="cas reel")
plt.title("Durée de contrôle")
plt.show()


lam = 0.5
res = np.random.exponential(lam,228)

plt.figure(figsize=(12,8))
plt.hist(res, bins=100, density=True)
plt.title("Estimation de la loi de repartition exp de param 0.5")
plt.show()


low = valMin # 02h48 = 168min
high = valMax # 05h30 = 330min
res = np.random.uniform(low,high,228)
plt.figure(figsize=(12,8))
plt.hist(res, bins=100, density=True)

plt.title("Estimation d'une loi de repartition Uniforme")
plt.show()




