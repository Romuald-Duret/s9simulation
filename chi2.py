import numpy as np
import  scipy.stats as scp
import matplotlib.pyplot as plt
import  pandas as pd

df = pd.read_table(
    'DonneesControle.txt',header=None,sep=" ")

#on récupere la moyenne pour estimer le parametre lamda de la loi exponentielle

valMax = df[0].max()
valMin = df[0].min()

listIA = df[0].values
listC = df[1].values
nbElem = 0

for i in range(len(listIA)):
    listIA[i] *= listIA[i]
    listC[i] *= listC[i]
    nbElem += 1


#mean, var, skew, kurt = chi2.stats(df[1], moments='mvsk')

### Histogramme des données

plt.figure(figsize=(12,8))
plt.hist(df[0], bins=100, density=True)
plt.plot(df[0],label="cas reel")
plt.title("cas reel")
#plt.show()

"""""
lam = 77
res = np.random.exponential(lam, 228)
plt.figure(figsize=(12,8))
plt.hist(res, bins=100, density=True)
plt.title("Estimation de la loi de repartition")
plt.show()
"""""

low = valMin # 02h48 = 168min
high = valMax # 05h30 = 330min
res = np.random.uniform(low,high,228)
plt.figure(figsize=(12,8))
plt.hist(res, bins=100, density=True)

plt.title("Estimation de la loi de repartition")
#plt.show()

chi2Test = scp.chisquare(listIA, res.sort(), 1)

print(chi2Test)
