import math
import numpy as np
import scipy as sp
import pandas as pd
from sklearn import linear_model, datasets,preprocessing, pipeline, metrics
from matplotlib import pyplot as plt


namesList=['Sex','Length', 'Diameter', 'Height', 'Whole weight', 'Shucked weight', 'Visecera weight', 'Shell weight', 'Rings']
with open('../abalone.data','r') as DF:
    DA=pd.read_csv(DF, header=None, names=namesList)

namesList=['age','workclass', 'fnlwgt','education', 'education num', 'status','occupation',
 'relation','race',  'sex', 'capital gain', 'capital loss','HPW', 'country','50k']
with open('../adult.data','r') as DF:
    AD=pd.read_csv(DF,header=None, names=namesList)


def task1(l,d):
    lnreg=linear_model.LinearRegression()
    lnreg.fit(l,d)

    predDiameter=lnreg.predict(l)
    print(lnreg.coef_, lnreg.intercept_, metrics.r2_score(d,predDiameter))
    plt.scatter(l,d, color='blue', linewidth='1')
    plt.plot(l,predDiameter,color='black', linewidth='2')
    plt.title('Length Vs Diameter')
    plt.xlabel('Length(mm)')
    plt.ylabel('Diameter(mm)')
    plt.show()

def task2(wm,ww):
    mlreg=linear_model.LinearRegression()
    mlreg.fit(wm, ww)
    predWW=mlreg.predict(wm)

    print(mlreg.coef_, mlreg.intercept_,metrics.r2_score(ww,predWW))
    plt.scatter(np.add(wm[:,0],wm[:,1],wm[:,2]), predWW, color='black')
    plt.title('Added weight Vs Whole weight')
    plt.xlabel('added weight(g)')
    plt.ylabel('whole wight(g)')
    plt.show()

def task3(d,ww):
    corr={'linear':0,'quad':0,'cubic':0,'exp':0}

    lnreg=linear_model.LinearRegression()
    lnreg.fit(d,ww)
    linpred=lnreg.predict(d)
    corr['linear']=metrics.r2_score(ww,linpred)

    quad=pipeline.Pipeline([('quad',preprocessing.PolynomialFeatures(2)),('linear',linear_model.LinearRegression())])
    quad.fit(d,ww)
    quadpred=quad.predict(np.linspace(0.05, 0.7, 4177).reshape((4177,1)))
    corr['quad']=metrics.r2_score(ww,quad.predict(d))

    cub=pipeline.Pipeline([('cub',preprocessing.PolynomialFeatures(3)),('linear',linear_model.LinearRegression())])
    cub.fit(d,ww)
    cubpred=cub.predict(np.linspace(0.05, 0.7, 4177).reshape((4177,1)))
    corr['cubic']=metrics.r2_score(ww,cub.predict(d))

    expreg=linear_model.LinearRegression()
    expreg.fit(d,np.log(ww))
    exppred=np.exp(expreg.predict(np.linspace(0.05, 0.7, 4177).reshape((4177,1))))
    corr['exp']=metrics.r2_score(ww,np.exp(expreg.predict(d)))

    print(corr)
    plt.scatter(d,ww,color='blue')
    plt.plot(d,linpred, color='yellow',linewidth=3,label='Linear')
    plt.plot(np.linspace(0.05, 0.7, 4177),exppred, color='green',linewidth=3, label='Exponential')
    plt.plot(np.linspace(0.05, 0.7, 4177),quadpred, color='black',linewidth=3, label='Quadratic')
    plt.plot(np.linspace(0.05, 0.7, 4177),cubpred, color='red',linewidth=3, label='Cubic')
    plt.title('Diameter Vs Whole weight')
    plt.xlabel('Diameter(mm)')
    plt.ylabel('Whole weight(g)')
    plt.legend()
    plt.show()


def task4(l,ww,rings,gender):
    AorI=np.array(gender).reshape((4177,1))
    acc={'length':0,'wholeWeight':0,'rings':0,'all':0}
    allF=np.zeros((4177,3))
    allF[:,0]=list(l)
    allF[:,1]=list(ww)
    allF[:,2]=list(rings)

    lOnly=linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial')
    lOnly.fit(l,AorI)
    predG=lOnly.predict(l)
    acc['length']=metrics.accuracy_score(AorI,predG)

    wOnly=linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial')
    wOnly.fit(ww,AorI)
    predG=wOnly.predict(ww)
    acc['wholeWeight']=metrics.accuracy_score(AorI,predG)

    rOnly=linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial')
    rOnly.fit(rings,AorI)
    predG=rOnly.predict(rings)
    acc['rings']=metrics.accuracy_score(AorI,predG)

    allreg=linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial')
    allreg.fit(allF,AorI)
    predG=allreg.predict(allF)
    acc['all']=metrics.accuracy_score(AorI,predG)
    print(acc)

def task5(am,sex):
    allreg=linear_model.LogisticRegression(solver='lbfgs', multi_class='multinomial', max_iter=1000)
    allreg.fit(am,sex)
    predSex=allreg.predict(am)
    acc=metrics.accuracy_score(sex,predSex)
    print(acc)

def main():

    l=DA['Length'].values.reshape((4177,1))
    d=DA['Diameter'].values.reshape((4177,1))
    ww=DA['Whole weight'].values.reshape((4177,1))
    shuckedw=DA['Shucked weight']
    shellw=DA['Shell weight']
    viseceraw=DA['Visecera weight']
    gender=','.join(list(DA['Sex'])).replace('M','F').split(',')
    rings=DA['Rings'].values.reshape((4177,1))
    wm=np.array([shuckedw,viseceraw,shellw]).transpose()

    #task one linear regressiion between length and diameter
    #task1(l,d)
    #task 2 multi variable linear regression
    #task2(wm,ww)
    #task 3 fitting to different fucntions linear and nonlinear regression
    #task3(d,ww)
    #task 4 logistic regression
    #task4(l,ww,rings,gender)

    #task5 logistic regression gender from adult dataset
    sex=AD['sex'].values.reshape((32561,1))
    #indefrent to removing workclass, country, race, age,capital gain, capital loss,education num,,50k,status
    catAdult=AD[['occupation','relation']]
    catAdult=pd.get_dummies(catAdult)
    numAdult=AD[ 'HPW']
    am=pd.concat([numAdult,catAdult],axis=1)
    #task5(am, sex)


if __name__ == '__main__':
    main()
