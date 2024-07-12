# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import matplotlib.pyplot as plt
import Classes as cf
import pandas as pd

##############################################
# The actual running portion of the code
#
#
##############################################     


# Run through sequence
rocketData  = np.genfromtxt("/Users/Dfmei/OneDrive/Documents/GitHub/2024David/RocketData.csv", delimiter=',', dtype='f8') # load in the data file
nDataPointsMass = 100

rockSweep   = np.arange(1, 5)
mStart      = np.zeros((nDataPointsMass, rockSweep.size))
mPayload    = np.zeros((nDataPointsMass, rockSweep.size))
mDry        = np.zeros((nDataPointsMass, rockSweep.size))
dv          = np.zeros((nDataPointsMass, rockSweep.size))
twPhase     = np.zeros((nDataPointsMass, rockSweep.size))

mdotRCS     = 3 / 86400     # divide by seconds per day to get rate per second




for jj,indRocket in enumerate(rockSweep):   
    mSeparated  = np.linspace(rocketData[-1,indRocket], rocketData[0,indRocket], nDataPointsMass)

    for ii,mLaunch in enumerate(mSeparated):
        
        apogeeOrbit = np.interp(mLaunch,rocketData[::-1,indRocket],rocketData[::-1,0]) # the weird -1 reverses the order of the data since interp expects increasing values
        
        
        
        # engMain = cf.Engine(450, 25000, 5.5, 'Biprop', 'Cryo') # Fill in values from hydrogen
        engMain = cf.Engine(370, 25000, 2.8, 'Biprop', 'Cryo') # Fill in values from Methane
        # engMain = cf.Engine(305, 25000, 1.8, 'Biprop', 'NotCryo') # fill in vlues with NTO/MMH
        # engMain = cf.Engine(330, 22240, 2.3, 'Biprop', 'NotCryo') # Fill in values with RP-1
        engRCS  = cf.Engine(220, 448, 1, 'Monoprop', 'NotCryo')
        
        dvReq = cf.ApogeeRaise(apogeeOrbit);
        
        
        if engMain.strCryo == 'Cryo':
            # Include chill-in and boiloff only for cryogenic sequence
            mdotOxBoiloff = 5/86400    # divide by seconds per day to get rate per second
            mdotFuelBoiloff = 10/86400  # divide by seconds per day to get rate per second 
            
            PreTLISett  = cf.Phase('Pre-TCM1 Settling',        mLaunch,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreTLIChill = cf.Phase('Pre-TCM1 Chill',   PreTLISett.mEnd,       0, engMain, 'Chill',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TLI         = cf.Phase('TLI',             PreTLIChill.mEnd,   dvReq, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToTCM1 = cf.Phase('Coast to TCM1',           TLI.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreTCM1Sett = cf.Phase('Pre-TCM1 Settling',CoastToTCM1.mEnd,      0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreTCM1Chill= cf.Phase('Pre-TCM1 Chill',  PreTCM1Sett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM1        = cf.Phase('TCM1',           PreTCM1Chill.mEnd,      20, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToTCM2 = cf.Phase('Coast to TCM2',          TCM1.mEnd,       0, engMain, 'Coast', 2*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM2        = cf.Phase('TCM2',            CoastToTCM2.mEnd,       5,  engRCS,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
            CoastToTCM3 = cf.Phase('Coast to TCM3',          TCM2.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM3        = cf.Phase('TCM3',            CoastToTCM3.mEnd,       5,  engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToLOI  = cf.Phase('Coast to LOI',           TCM3.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreLOISett  = cf.Phase('Pre-LOI Settling', CoastToLOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreLOIChill = cf.Phase('Pre-LOI Chill',    PreLOISett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
            LOI         = cf.Phase('LOI',             PreLOIChill.mEnd,     850, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToTCM4 = cf.Phase('Coast to TCM4',           LOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM4        = cf.Phase('TCM4',            CoastToTCM4.mEnd,       5, engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToDOI  = cf.Phase('Coast to DOI',           TCM4.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreDOISett  = cf.Phase('Pre-DOI Settling', CoastToDOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreDOIChill = cf.Phase('Pre-DOI Chill',    PreDOISett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
            DOI         = cf.Phase('DOI',             PreDOIChill.mEnd,      25, engMain, 'Burn',     0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToPDI  = cf.Phase('Coast to PDI',            DOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PrePDISett  = cf.Phase('Pre-PDI Settling', CoastToPDI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PrePDIChill = cf.Phase('Pre-PDI Chill',    PrePDISett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
            PDI         = cf.Phase('PDI',             PrePDIChill.mEnd,      -1, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        
            Sequence = [PreTLISett, PreTLIChill, TLI, CoastToTCM1, PreTCM1Sett, PreTCM1Chill, TCM1,CoastToTCM2, TCM2, CoastToTCM3, \
            TCM3,CoastToLOI,PreLOISett, PreLOIChill, LOI, CoastToTCM4, TCM4,CoastToDOI, PreDOISett, PreDOIChill, DOI, CoastToPDI, \
                PrePDISett, PrePDIChill, PDI]
        
        else:
            # This is not a cryogenic engine, so we don't need chill-in or boiloff
            mdotOxBoiloff   = 0    # divide by seconds per day to get rate per second
            mdotFuelBoiloff = 0  # divide by seconds per day to get rate per second 
            
            PreTLISett  = cf.Phase('Pre-TCM1 Settling',        mLaunch,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TLI         = cf.Phase('TLI',              PreTLISett.mEnd,   dvReq, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToTCM1 = cf.Phase('Coast to TCM1',           TLI.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreTCM1Sett = cf.Phase('Pre-TCM1 Settling',CoastToTCM1.mEnd,      0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM1        = cf.Phase('TCM1',           PreTCM1Sett.mEnd,      20, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToTCM2 = cf.Phase('Coast to TCM2',          TCM1.mEnd,       0, engMain, 'Coast', 2*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM2        = cf.Phase('TCM2',            CoastToTCM2.mEnd,       5,  engRCS,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
            CoastToTCM3 = cf.Phase('Coast to TCM3',          TCM2.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM3        = cf.Phase('TCM3',            CoastToTCM3.mEnd,       5,  engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToLOI  = cf.Phase('Coast to LOI',           TCM3.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreLOISett  = cf.Phase('Pre-LOI Settling', CoastToLOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            LOI         = cf.Phase('LOI',              PreLOISett.mEnd,     850, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToTCM4 = cf.Phase('Coast to TCM4',           LOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM4        = cf.Phase('TCM4',            CoastToTCM4.mEnd,       5, engRCS,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToDOI  = cf.Phase('Coast to DOI',           TCM4.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreDOISett  = cf.Phase('Pre-DOI Settling', CoastToDOI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            DOI         = cf.Phase('DOI',             PreDOISett.mEnd,      25, engMain, 'Burn',     0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToPDI  = cf.Phase('Coast to PDI',            DOI.mEnd,       0, engMain, 'Coast', 0.5*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PrePDISett  = cf.Phase('Pre-PDI Settling', CoastToPDI.mEnd,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PDI         = cf.Phase('PDI',              PrePDISett.mEnd,      -1, engMain,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            
            Sequence = [PreTLISett, TLI, CoastToTCM1, PreTCM1Sett, TCM1,CoastToTCM2, TCM2, CoastToTCM3, \
            TCM3,CoastToLOI,PreLOISett,LOI,CoastToTCM4, TCM4,CoastToDOI, PreDOISett, DOI, CoastToPDI, \
                PrePDISett, PDI]
        
        # Create the Misison Summary and calculate subsystem masses with payload    
        Mission = cf.MissionSummary(Sequence)
        OxTanks = cf.TankSet("Oxygen", "Stainless", 1, 2, 300000, Mission.mPropTotalOx) #Ox for now

        # FuelTanks = cf.TankSet("RP-1", "Stainless", 1, 2.05, 300000, Mission.mPropTotalFuel)    # Fill in RP-1 here
        FuelTanks = cf.TankSet("Methane", "Stainless", 1, 2.0, 300000, Mission.mPropTotalFuel)     # Fill in Methane here
        MonoTanks = cf.TankSet("MMH", "Al2219", 1,1.08, 300000, Mission.mPropTotalMono)    
        subs = cf.Subsystems(mLaunch, engMain, OxTanks, FuelTanks, MonoTanks, 2000, 'Deployable', 'Large', 8)
        payload = mLaunch - Mission.mPropTotalTotal - subs.mTotalAllowable
        
        print([OxTanks.lRadiusTank, mLaunch, dvReq])
        
        mStart[ii, jj] = mLaunch
        mPayload[ii, jj] = payload
        mDry[ii,jj] = subs.mTotalAllowable

legString=('Goal', 'Scout', 'Juno', 'Vanguard', 'Nike') # initialize the list for the legend, add in the rocket names
fig1 = plt.figure()
plt.plot([2000, 20000], [50, 50], color='k')
for ii in range(rockSweep.size):                   
    plt.plot(mStart[:,ii], mPayload[:,ii], linewidth=3.0)
   
plt.grid()
plt.xlabel('Start Mass (kg)')
plt.ylabel('Payload (kg)')
plt.legend((legString))


"""      

for jj, thrust in enumerate(rockSweep):
    print('{:9.1f} {:9.1f}{:9.1f}{:9.3f}'.format(rockSweep[jj], mFinal[0,jj], dv[0,jj], twPhase[0,jj]))
# Start the plotting stuff 


plt.grid()

fig2 = plt.figure()
plt.plot(mSeparated, mFinal[:,0])
plt.xlabel('Launch Mass (kg)')
plt.ylabel('Final Mass (kg)')
plt.grid()
"""
