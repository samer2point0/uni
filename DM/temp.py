import numpy as np
import pandas as pd
import math
from datetime import datetime
import matplotlib.pyplot as plt # visualizing data
import seaborn as sns
from collections import Counter

import pandas_profiling as pP

# write your code here
with open('./pollution.csv','r') as DF:
    AD=pd.read_csv(DF)

print(AD.columns)
print(AD.describe())
pP.ProfileReport(AD)
