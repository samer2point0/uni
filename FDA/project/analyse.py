import math
import pickle
import numpy as np
import scipy
from yellowbrick import regressor, target, classifier, features
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing, pipeline,decomposition, naive_bayes, metrics,tree, cluster, linear_model,ensemble

with open('../EMI_Music/users.csv','r') as DF:
    usersM=pd.read_csv(DF)

with open('../EMI_Music/words.csv','r') as DF:
    artistsM=pd.read_csv(DF)
    artistsM=artistsM[artistsM['HEARD_OF']!='Never heard of']
    artistsM=artistsM.dropna(subset=['LIKE_ARTIST'])

with open('../EMI_Music/train.csv','r') as DF:
    ratingsM=pd.read_csv(DF)

feat=[]

def prep(artistsM):
    tempu=usersM.drop(columns=['LIST_OWN','LIST_BACK','REGION'])
    #tempu=tempu.fillna(usersM.mean())
    tempu=tempu.dropna(subset=['AGE','GENDER','WORKING'],axis=0)
    tempu=tempu.fillna(tempu.mean())

    Qs=tempu.columns.values.tolist()[5:]
    rel=pd.merge(tempu,artistsM,on='USERID', how='inner')

    groupedRatings=ratingsM[['Artist','USERID','Rating']].groupby(['Artist','USERID']).mean()
    artistAVG=groupedRatings['Rating'].groupby('Artist').mean().to_frame(name='rateAAVG')
    userAVG=groupedRatings['Rating'].groupby('USERID').mean().to_frame(name='rateUAVG')
    tempM=pd.merge(rel,groupedRatings,on=['Artist','USERID'], how='inner',right_index=True)
    tempM=pd.merge(tempM,artistAVG,on='Artist', how='inner')
    tempM=pd.merge(tempM,userAVG,on='USERID', how='inner')
    tempM.index=list(range(tempM['Rating'].size))

    Qs.extend(['Rating', 'LIKE_ARTIST'])
    tempM[Qs]=tempM[Qs].applymap(lambda x: round(x/10))

    words=artistsM.columns.values.tolist()[5:]
    wordsM=tempM[words]

    wordsM=wordsM.dropna(axis=1, thresh=1000)
    tempM=tempM.drop(columns=words)

    wordsM=wordsM.fillna(wordsM.mean())
    PCA=decomposition.PCA(n_components=5)
    wordsPC=pd.DataFrame(PCA.fit_transform(wordsM), dtype=np.float16, columns=['axis0','axis1','axis2','axis3','axis4'])

    u=tempM['USERID'].values.tolist()
    aua=list(zip(tempM['Artist'].values,u))
    r1,r2,r3=np.zeros((len(aua),1),dtype=np.int8),np.zeros((len(aua),1),dtype=np.int8),np.zeros((len(aua),1),dtype=np.int8)
    i1,i2=[],[]
    for i in range(len(aua)):
        au=aua[i]
        r=round((tempM['Rating'].iloc[i]+tempM['LIKE_ARTIST'].iloc[i])/2)
        r1[i]=round(r-userAVG['rateUAVG'].ix[au[1]])
        r2[i]=round(r-artistAVG['rateAAVG'].ix[au[0]])
        r3[i]=r


        w=tempM['WORKING'].iloc[i]
        if ('student' in w):
            tempM['WORKING'].set_value(i,'student')
        elif ('Retired' in w):
            tempM['WORKING'].set_value(i,'Retired')
        elif ('state' in w or 'voluntary' in w ):
            tempM['WORKING'].set_value(i,'Other')
        elif ('less than 8' in w):
            tempM['WORKING'].set_value(i,'Unemployed')


        m=tempM['MUSIC'].iloc[i]
        if m=='Music has no particular interest for me':
            tempM['MUSIC'].set_value(i,0)
        elif m in ['I like music but it does not feature heavily in my life', 'Music is no longer as important as it used to be to me']:
            tempM['MUSIC'].set_value(i,1)
        elif 'necessarily' in m:
            tempM['MUSIC'].set_value(i,2)
        elif m=='Music means a lot to me and is a passion of mine':
            tempM['MUSIC'].set_value(i,3)
    tempM['MUSIC']=tempM['MUSIC'].astype(int)


    R1=pd.DataFrame(r1,columns=['R1'])
    R2=pd.DataFrame(r2,columns=['R2'])
    Ravg=pd.DataFrame(r3,columns=['Ravg'])

    R=userprof(r1,u,aua)
    #R=userProf(ratingsM,u,userAVG,r2)
    M=pd.concat([Ravg,R1,R2,tempM],axis=1)

    return R,wordsPC,M

def userProf(rM,u,uavg,aavg):
    us=list(set(u))
    aua=list(zip(rM['Track'].values,rM['USERID'].values,list(rM.index)))
    #aua=list(filter(lambda x:x[1] in us, aua))#[x for x in aua if x[1] in us]
    f=open('aua.txt','rb')
    aua=pickle.load(f)
    f.close()

    ta=set(rM['Track'].values.tolist())
    R = pd.DataFrame(index=us, columns=ta)
    for i in range(len(aua)):
        au=aua[i]
        ui=u.index(au[1])
        r=round(rM['Rating'].iloc[au[2]]/10-uavg['rateUAVG'].ix[ui])
        R[au[0]].set_value(au[1],r)

    R=pd.concat([pd.DataFrame(us,index=us,columns=['USERID']),R], axis=1)

    f=open('R.txt','wb')
    pickle.dump(R,f)
    f.close()
    R=R.dropna(axis=1, thresh=100)
    R=R.dropna(axis=0,thresh=5)
    R=R.fillna(0)
    return R

def userprof(r,u, aua):
    u=list(set(u))
    R = pd.DataFrame(index=u, columns=list(range(50)))
    for i in range(len(aua)):
        R[aua[i][0]].set_value(aua[i][1],int(r[i]))

    R=pd.concat([pd.DataFrame(u,index=u,columns=['USERID']),R], axis=1)
    R=R.dropna(axis=1, thresh=100)
    R=R.dropna(axis=0,thresh=2)
    R=R.fillna(0)

    return R

def clusterA(wordsPC):
    R=neighbors.radius_neighbors_graph(wordsPC,0.5)
    DB=cluster.DBSCAN(eps=0.344, min_samples=50, metric='precomputed')
    y=DB.fit_predict(R).reshape(wordsPC[0].size,1)
    return pd.DataFrame(y, columns=['Cluster'])

def visualise(M):
    M_x=M[feat]
    M_y=M['WORKING']

    visualizer = features.Rank2D(algorithm='pearson')
    visualizer.fit(M_x, M_y)                # Fit the data to the visualizer
    visualizer.transform(M_x)             # Transform the data
    visualizer.poof()
"""
    visualizer=target.FeatureCorrelation(method='mutual_info-classification',labels=feat)
    visualizer.fit(M_x,M_y)
    visualizer.poof()


    visualizer=target.FeatureCorrelation(method='mutual_info-classification',labels=feat)
    M_y=M['GENDER']
    visualizer.fit(M_x,M_y)
    visualizer.poof()

    M_y=M['AGE']
    visualizer=target.FeatureCorrelation(labels=feat)
    visualizer.fit(M_x,M_y)
    visualizer.poof()
"""

def classify(att,M,b):
    train=M.iloc[:b]
    test=M.iloc[b:]
    train_x=train[feat]
    train_y=train[att]
    test_x=test[feat]
    test_y=test[att]

    NB=naive_bayes.GaussianNB()
    #DT=tree.DecisionTreeClassifier(min_samples_leaf=300)#min_samples_leaf=100)
    NB.fit(train_x,train_y)

    pred_y=NB.predict(test_x)

    fig = plt.figure()
    ax = fig.add_subplot()
    viz = features.importances.FeatureImportances(ensemble.GradientBoostingClassifier(), ax=ax)
    viz.fit(train_x,train_y)
    viz.poof()

    visualizer = classifier.ClassBalance()
    visualizer.fit(M[att])
    visualizer.poof()

    visualizer = classifier.ClassificationReport(NB, support=True)
    visualizer.score(test_x, test_y)
    visualizer.poof()

    visualizer = classifier.ClassPredictionError(NB)
    visualizer.score(test_x, test_y)
    visualizer.poof()

    print(metrics.accuracy_score(test_y,pred_y),metrics.cohen_kappa_score(test_y,pred_y))

def regres(att,M,b):
    train=M.iloc[:b]
    test=M.iloc[b:]
    train_x=train[feat]
    train_y=train[att]

    test_x=test[feat]
    test_y=test[att]

    reg=linear_model.LinearRegression()
    reg.fit(train_x, train_y)
    pred_y=reg.predict(test_x)


    fig = plt.figure()
    ax = fig.add_subplot()
    viz = features.importances.FeatureImportances(reg, ax=ax, labels=feat,relative=False)
    viz.fit(M[feat],M[att])
    viz.poof()

    visualizer1=regressor.PredictionError(reg)
    visualizer1.score(test_x,test_y)
    visualizer1.poof()

    visualizer2=regressor.ResidualsPlot(reg)
    visualizer2.fit(train_x,train_y)
    visualizer2.score(test_x,test_y)
    visualizer2.poof()

    print(metrics.r2_score(test_y,pred_y), metrics.mean_squared_error(test_y,pred_y))

def dif(uM,aM):
    pass

R,wordsPC,M=prep(artistsM)
#DB=clusterA(wordsPC)
M=pd.concat([wordsPC,M],axis=1)

R=pd.merge(M[['USERID','AGE','GENDER','WORKING']],R,on='USERID',how='right')
R=R.drop_duplicates()
feat=usersM.columns.values.tolist()[8:]
feat.extend(['MUSIC'])


#visualise(M)
#classify('GENDER',M,14000)
#classify('WORKING',M,14000)
#regres('AGE',M,14000)
feat=R.columns.values.tolist()[4:]
#visualise(R)
#classify('GENDER',R,10000)
#classify('WORKING',R,10000)
#regres('AGE',R,10000)
