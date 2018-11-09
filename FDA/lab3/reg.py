import numpy as np
import scipy as sp
import pandas as pd
from sklearn import linear_model, datasets
from matplotlib import pyplot as plt


namesList=['Sex','Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Visecera weight', 'Shell weight', 'Rings']

with open('../abalone.data','r') as DF:
    DA=pd.read_csv(DF, header=None, names=namesList)





def main():
    l=DA['Length'].reshape((4177,1))
    d=DA['Diameter'].reshape((4177,1))
    lnreg=linear_model.LinearRegression()
    lnreg.fit(l,d)
    print(lnreg.coef_, lnreg.intercept_)

    predDiameter=lnreg.predict(l)
    plt.scatter(l,d, color='blue', linewidth='1')
    plt.plot(l,predDiameter,color='black', linewidth='2')
    plt.show()

    ww=DA['Whole weight'].reshape((4177,1))
    shuckedw=DA['Shucked weight']
    shellw=DA['Shell weight']
    viseceraw=DA['Visecera weight']
    wm=np.array([shuckedw,viseceraw,viseceraw]).transpose()


    mlreg=linear_model.LinearRegression()
    mlreg.fit(wm, ww)
    print(lnreg.coef_, lnreg.intercept_)

    predWW=mlreg.predict(wm)

    plt.scatter(np.add(wm[:,0],wm[:,1],wm[:,2]), predWW)
    plt.show()


if __name__ == '__main__':
    main()
