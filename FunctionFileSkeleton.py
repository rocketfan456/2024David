import numpy as np

def ApogeeRaise(apogeeStart):
    mu = 398600
    apogeeEnd = 410000
    rEarth = 6378
    rStart = rEarth+185
    aStart = (rStart+rEarth+apogeeStart)/2
    aEnd   = (rStart+rEarth+apogeeEnd)/2
        
    vStart = np.sqrt(mu*(2/rStart-1/aStart))
    vEnd   = np.sqrt(mu*(2/rStart-1/aEnd))
    dv     = vEnd-vStart
       
    return dv*1000 # multiply by 1000 to put in m/s
