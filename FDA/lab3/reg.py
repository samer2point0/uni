import numpy as np
import scipy as sp
import pandas as pd
from sklearn import linear_model, datasets


namesList=['Sex','Length', 'Diameter', 'Height', 'whole weight', 'shucked wieght', 'Visecera wieght', 'shell weight', 'Rings']

with open('../abalone.data','r') as DF:
    DA=pd.read_csv(DF, header=None, names=namesList)





def main():
    lnreg=linear_model.LinearRegression()
    lnreg.fit(DA['Length'],DA['Diameter'])
    print(lnreg.coef)

if __name__ == '__main__':
    main()
