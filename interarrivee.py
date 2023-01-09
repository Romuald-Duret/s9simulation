import numpy as np
import  scipy.stats as scp
import matplotlib.pyplot as plt
import  pandas as pd

df = pd.read_table('sort.txt',header=None,sep=" ")
print(df)
plt.figure(figsize=(12,8))
plt.hist(df[0], bins=100, density=True)
plt.title("Inter arrivee des bus")
plt.show()

