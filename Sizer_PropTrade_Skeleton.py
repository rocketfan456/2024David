# -*- coding: utf-8 -*-
"""

"""
import numpy as np
import matplotlib.pyplot as plt
import Classes as cf

##############################################
# The actual running portion of the code
#
#
##############################################     


# Run through sequence
rocketData  = np.genfromtxt('/Users/Dfmei/OneDrive/Documents/Github/2024David/RocketData.csv', delimiter=',', dtype='f8')
nDataPointsMass = 100

ispSweep    =  np.array([305, 330, 370, 450])# The order of propellant is NTO/MMH (305), RP1 (330), Methane (370), Hydrogen (450)
mrSweep     = np.array([1.8, 2.3, 2.8, 5.5])# The order of propellant is NTO/MMH, RP1, Methane, Hydrogen 
cryoFlag    = ['Not Cryo', 'Not Cryo', 'Cryo', 'Cryo']
mStart      = np.zeros((nDataPointsMass, ispSweep.size))
mPayload    = np.zeros((nDataPointsMass, ispSweep.size))
mDry        = np.zeros((nDataPointsMass, ispSweep.size))
dv          = np.zeros((nDataPointsMass, ispSweep.size))
twPhase     = np.zeros((nDataPointsMass, ispSweep.size))
cost        = np.zeros((nDataPointsMass, ispSweep.size))


mdotRCS     = 3 / 86400     # divide by seconds per day to get rate per second


# Rocket Information. Index to use and the cost of the rocket
rocketIndex = 3 # Pick a number that corresponds to the rocket
cstRocket   =  100_000_000 # Put in the cost of the rocket
fairingDiameter = 5 # Put in the fairing diameter


# Number of Prop Tanks and Radius
nTanks = 2;
print("Num Tanks: " + str(nTanks))
rMax = (fairingDiameter-0.2-0.024-0.15-0.3)/nTanks/2
print("\nMax Radius: " + str(rMax))

for jj,ispEngine in enumerate(ispSweep):   
    # The fifth column of rocketData (index 3) contains the rocket of interest
    mSeparated  = np.linspace(rocketData[-1,rocketIndex], rocketData[0,rocketIndex], nDataPointsMass)
    for ii,mLaunch in enumerate(mSeparated):
        
        # Interpolate the data from the datafile
        apogeeOrbit = np.interp(mLaunch,rocketData[::-1,rocketIndex],rocketData[::-1,0]) # the weird -1 reverses the order of the data since interp expects increasing values
        #print(rocketData[::-1,rocketIndex])
               
        
        dvReq   = cf.ApogeeRaise(apogeeOrbit)
        engMain = cf.Engine(ispEngine, 2224, mrSweep[jj], 'Biprop', cryoFlag[jj])
        engRCS  = cf.Engine(220, 448, 1, 'Monoprop', 'NotCryo')
        
        
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
        
        # Check tanks based on Isp (since each value is a different propellant)
        matFuelTank = "Al-Li" # fuel tank material all the same
        if ispEngine==305:
            OxTanks = cf.TankSet("NTO", matFuelTank, nTanks, rMax, 1000000, Mission.mPropTotalOx)
            FuelTanks = cf.TankSet("MMH", matFuelTank, nTanks, rMax, 1000000, Mission.mPropTotalFuel)
        elif ispEngine==330:
            OxTanks = cf.TankSet("Oxygen", matFuelTank, nTanks, rMax, 300000, Mission.mPropTotalOx)
            FuelTanks = cf.TankSet("RP-1", matFuelTank, nTanks, rMax, 300000, Mission.mPropTotalFuel)   
        elif ispEngine==370:
            OxTanks = cf.TankSet("Oxygen", matFuelTank, nTanks, rMax, 300000, Mission.mPropTotalOx)
            FuelTanks = cf.TankSet("Methane", matFuelTank, nTanks, rMax, 300000, Mission.mPropTotalFuel)  
        elif ispEngine==450:
            OxTanks = cf.TankSet("Oxygen", matFuelTank, nTanks, rMax, 300000, Mission.mPropTotalOx)
            FuelTanks = cf.TankSet("Hydrogen", matFuelTank, nTanks, rMax, 300000, Mission.mPropTotalFuel)  
        
        # Calculate monopropellant tank size
        MonoTanks = cf.TankSet("MMH", "Al2219", 1, 2, 300000, Mission.mPropTotalMono) # Forgetting monoprop tanks?   
        subs = cf.Subsystems(mLaunch, engMain, OxTanks, FuelTanks, MonoTanks, 100, 'Deployable', 'Large', 8)
        
        # print("\nTank MAss: " + str(OxTanks.mTotal + FuelTanks.mTotal)) 
        # Determine payload
        payload = mLaunch - Mission.mPropTotalTotal - subs.mTotalAllowable
        
        # Determine Cost
        costObject = cf.Cost(subs.mTotalAllowable,  25000, cstRocket)
        cost[ii,jj] = costObject.costNRETotal/1000000
        
        # Save values for plotting        
        mStart[ii, jj] = mLaunch
        mPayload[ii, jj] = payload
        mDry[ii,jj] = subs.mTotalAllowable
        
        
        

legString=('Goal', 'NTO/MMH', 'LOX/RP-1', 'LOX/Methane', 'LOX/LH2') # initialize the list for the legend
fig1, ax1 = plt.subplots()
ax1.plot([7500, 20000], [50, 50], color='k')
for ii in range(ispSweep.size):                   
    ax1.plot(mStart[:,ii], mPayload[:,ii], linewidth=3.0)
   
plt.grid()
plt.xlabel('Start Mass (kg)')
plt.ylabel('Payload (kg)')
plt.legend((legString))

legString=('NTO/MMH','LOX/RP-1','LOX/Methane','LOX/LH2') # initialize the list for the legend
fig2, ax2 = plt.subplots()
for ii in range(ispSweep.size):                   
    ax2.plot(mStart[:,ii], cost[:,ii], linewidth=3.0)
   
plt.grid()
plt.xlabel('Start Mass (kg)')
plt.ylabel('Cost (Millions of Monopoly Dollars)')
plt.legend((legString))



