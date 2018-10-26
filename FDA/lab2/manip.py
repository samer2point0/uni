

namesList=['symboling', 'normalized-losses', 'make', 'fuel-type','aspiration', 'num-of-doors','body-style', 'drive-wheels', 'enigne-location', 'wheel-base', 'length', 'width', 'height', 'curb-weight', 'enginer-type', 'num-of-cylinders', 'engine-size', 'fuel-system','bore', 'stroke','compression-ration', 'horsepower', 'peak-rpm', 'city-mpg', 'highway-mpg','price']

with open('./imports-85-data.txt') as DF:
    DA=[namesList]
    for line in DF:
        DA.append(DF.read().replace('\n','').split(','))
print(DA)
