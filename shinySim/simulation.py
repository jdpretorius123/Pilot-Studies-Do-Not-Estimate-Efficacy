"""Make accessory functions to improve readability."""

from distribution import Distribution

from table import Table

from myMath import *

from myFunctions import *

def simulation(numTrials = 1000):
    if not isinstance(numTrials, int):
        raise TypeError("ONLY INT TYPES SUPPORTED")

    if numTrials < 2:
        raise ValueError("NUMTRIALS MUST BE GREATER THAN OR EQUAL TO 2")
    
    c = Distribution(numTrials, mu = 50, sd = 10, seed = 1)    #creates instance of Distribution class for control distribution
    t1 = Distribution(numTrials, mu = 48, sd = 10, seed = 2)   #creates instance of Distribution class for treatment 1 distribution
    t2 = Distribution(numTrials, mu = 46.5, sd = 10, seed = 3) #creates instance of Distribution class for treatment 2 distribution
    t3 = Distribution(numTrials, mu = 45, sd = 10, seed = 4)   #creates instance of Distribution class for treatment 3 distribution

    distributions = [c, t1, t2, t3]

    table = Table() #creates instance of Table class

    sampleSizes = [10, 20, 30]

    simResults = {} #key:value -- row:[EShat,lb,ub,[bin0,bin1,bin2,bin3]] 

    row = 1 #key for final results

    for i in range(3): #initiates simulation for each sample size
        n = sampleSizes[i]

        esObs = [[],[],[]] #stores EShat and bins from each trial for each sample size
        bObs = [[],[],[]]  # for each treatment to calculate final test statistics

        for adist in range(4):
            distributions[adist].setSampleSize(n)

        for trial in range(numTrials): #calculates mean and variance for Control, T1, T2, T3
            distStats = [[],[],[],[]]

            for adist in range(4):
                dist = distributions[adist]
                dist.drawSample()
                mean = dist.getSampleMean()
                var = dist.getSampleVar()

                distStats[adist].append(mean)
                distStats[adist].append(var)

            meanC = distStats[0][0]
            varC = distStats[0][1]

            for stat in range(1,4): #calculates and stores EShat and bins from each trial
                varT = distStats[stat][1]
                pSD = pooledSD(n, varT, varC)

                meanT = distStats[stat][0]
                es = calculateES(meanT, meanC, pSD)
                esObs[stat - 1].append(es)

                b = calculateB(es)
                bObs[stat - 1].append(b)
        
        for k in range(3): #calculates final test statstics for each sample size for each treatment
            esvals = esObs[k]
            EShat = calculateAvgES(numTrials, esvals)

            sd = calculateSD(numTrials, esvals)
            ci = calculateCI(numTrials, sd)

            lb = calculateLB(EShat, ci)
            ub = calculateUB(EShat, ci)

            bvals = bObs[k]
            bins = [0,0,0,0]
            for obs in bvals:
                bins[obs] += 1

            for abin in range(4):
                bins[abin] = (bins[abin] / numTrials) * 100

            value = [EShat,lb,ub,bins]
            simResults[row] = value

            row += 3
                
        row -= 8

    items = list(simResults.items())
    items.sort(key = getRow)

    tableData = []
    length = len(items)
    for i in range(length): #extracts and prepares final results for Table class
        row = items[i][1]
        tableData.append(row)
        
    table.storeData(tableData)
