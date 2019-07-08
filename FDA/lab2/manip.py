import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

namesList=['symboling', 'normalized-losses', 'make', 'fuel-type','aspiration', 'num-of-doors','body-style','drive-wheels',
 'enigne-location', 'wheel-base', 'length', 'width', 'height', 'curb-weight', 'enginer-type','num-of-cylinders', 'engine-size',
  'fuel-system','bore', 'stroke','compression-ration', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg','price']
with open('../imports-85-data.txt','r') as DF:
    DA=pd.read_csv(DF,header=None, names=namesList)



def M():
    c=0
    for car in DA['make']:
        if car[0]=='m':
            c=c+1
    return c

def main():
    print(M())



if __name__ == '__main__':
    main()
