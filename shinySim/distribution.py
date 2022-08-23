from numpy.random import normal, seed # imports necessary functions from numpy random module

class Distribution:
    def __init__(self, numTrials, mu, sd, seed):
        self.numTrials = numTrials
        self.mu = mu
        self.sd = sd
        self.seed = seed

        self.sampleSize = None
        self.sampleMean = None
        self.sampleVar = None
        self.samplePool = None
        self.currentSample = None

    def __repr__(self):
        return self.__class__.__name__ + "mu: " + str(self.getMu) + " sd: " + str(self.getSD)

    def __str__(self):
        return "A random normal distribution with mu: " + str(self.getMu) + " and sd: " + str(self.getSD)

    def getNumTrials(self):
        return self.numTrials

    def getMu(self):
        return self.mu

    def getSD(self):
        return self.sd

    def getSeed(self):
        return self.seed

    def getSampleSize(self):
        return self.sampleSize

    def getSampleMean(self):
        return self.sampleMean

    def getSampleVar(self):
        return self.sampleVar

    def getSamplePool(self):
        return self.samplePool

    def getCurrentSample(self):
        return self.currentSample

    def setSeed(self, aSeed):
        self.seed = aSeed

    def setSampleSize(self, n):
        self.sampleSize = n
        self.createSamples()

    def setSampleMean(self, mean):
        self.sampleMean = mean

    def setSampleVar(self, var):
        self.sampleVar = var

    def setSamplePool(self, samplePool):
        self.samplePool = samplePool

    def setCurrentSample(self, sample):
        self.currentSample = sample

    def createSamples(self): # creates a reproducible random normal distribution and draws as many samples as trials asked for by user
        mean = self.getMu()
        stanDev = self.getSD()

        numSamples = self.getNumTrials()
        sampleSize = self.getSampleSize()
        dimensions = (numSamples, sampleSize)
        aSeed = self.getSeed()

        seed(aSeed)
        
        samplePool = normal(loc = mean, scale = stanDev, size = dimensions)
        samplePool = samplePool.tolist()
        self.setSamplePool(samplePool)

    def drawSample(self): # draws sample from sample pool
        sample_Float = self.getSamplePool().pop()
        sample_Int = self.roundVals(sample_Float)

        self.setCurrentSample(sample_Int)
        
        self.calculateSampleMean()
        self.calculateSampleVar()

    def calculateSampleMean(self): # calculates sample mean from most recently drawn sample
        sample = self.getCurrentSample()
        total = sum(sample)
        length = self.getSampleSize()
        
        mean = total / length
        self.setSampleMean(mean)

    def calculateSampleVar(self): # calculates sample variance from most recently drawn sample
        sample = self.getCurrentSample()
        mean = self.getSampleMean()
        length = self.getSampleSize()

        SS = 0
        for score in sample:
            SS += (score - mean)**2

        var = SS / (length - 1)
        self.setSampleVar(var)

    def roundVals(self, alist): # rounds all floating point values in a list to nearest integer   
        length = len(alist)

        for i in range(length):
            alist[i] = int(alist[i])
            
        return alist
