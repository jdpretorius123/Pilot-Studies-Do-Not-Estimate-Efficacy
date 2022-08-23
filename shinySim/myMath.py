def pooledSD(n, varC, varT): # caclulates pooled SD using the variance from a control distribution sample and the varience from a treatment distribution sample
    sampleSize = n - 1
    
    num = (sampleSize)*varC + (sampleSize)*varT
    den = sampleSize*2
    
    pooled_SD = (num / den)**(0.5)
    return pooled_SD

def calculateES(meanT, meanC, pSD): # caclulates treatment ES using the mean from a control distribution sample and the mean from a treatment distribution sample
    diff = meanT - meanC
    ES = diff / pSD
    return ES

def calculateAvgES(sampleSize, alist): # calculates average treatment ES using all ES values determined across all samples for a given ES (-0.2,-0.35,-0.5)
    n = sampleSize
    obs = alist

    num = sum(obs)
    den = n

    EShat = num / den
    EShat = round(EShat, 2)
    return EShat

def calculateB(ES): # determines bin from treatment ES value
    if (ES <= -0.5):
        return 3

    else:
        if (-0.5 < ES <= -0.35):
            return 2

        else:
            if (-0.35 < ES < 0):
                return 1

            else:
                return 0

def calculateSD(sampleSize, vals): # calculates SD for average ES determined across all samples for a given ES
    n = sampleSize
    obs = vals
    total = sum(vals)
    mean = total / n

    ss = 0
    for idx in range(n):
        ss += (mean - obs[idx])**2

    var = ss / (n - 1)
    sd = var**(0.5)
    return sd

def calculateCI(sampleSize, sd): # calculates CI for average ES determined across all samples for a given ES
    n = sampleSize
    n_sqrt = n**(0.5)
    
    ci = 1.96 * (sd / n_sqrt)
    ci = round(ci, 2)
    return ci

def calculateLB(ES, CI): # calculates lower CI bound
    lb = ES - CI
    lb = round(lb, 2)
    return lb

def calculateUB(ES, CI): # calculates upper CI bound
    ub = ES + CI
    ub = round(ub, 2)
    return ub
