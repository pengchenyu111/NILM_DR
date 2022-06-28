import numpy as np
import pandas as  pd

s1 = pd.Series([3, 5])
s2 = pd.Series([2, 6])
tt = [s1,s2]
res = np.min([s1, s2],axis=0)
print(res)
