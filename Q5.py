import numpy as np
import  scipy.stats as scp
import matplotlib.pyplot as plt
import  pandas as pd
from scipy import signal


df = pd.read_csv('question6.csv',header=None,sep=";")
print (df)
moyenne=[]
calcmoy=0
for i in range(0,199):
    print(i)
    calcmoy= df[i].mean()
    moyenne.append(calcmoy)
print(moyenne)

plt.figure(figsize=(12,8))
plt.title("Moyenne sur 1000 simulations des Di avec une lim de 200 bus")
plt.plot(moyenne)
plt.show()

#Méthode Welch
df2 = pd.DataFrame(moyenne)
print(df2.rolling(4).mean())
welch = df2.rolling(4).mean()
plt.plot(welch)
plt.show()