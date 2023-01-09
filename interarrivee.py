import numpy as np
import  scipy.stats as scp
import matplotlib.pyplot as plt
import  pandas as pd

df = pd.read_table('interarrivee.txt',header=None,sep=" ")
print(df)
plt.figure(figsize=(12,8))
plt.hist(df[0], bins=100, density=True)
plt.title("cas reel inter")
plt.show()

