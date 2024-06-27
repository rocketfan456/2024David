import numpy as np
import Classes as cf
import matplotlib.pyplot as plt


# Run through sequence
mSeparated  = np.linspace(3870, 8000, 6)
thrSweep    = np.linspace(3000, 15000,6)
mStart      = np.zeros((mSeparated.size, thrSweep.size))
mFinal      = np.zeros((mSeparated.size, thrSweep.size))
twPDIStart  = np.zeros((mSeparated.size, thrSweep.size))
dv          = np.zeros((mSeparated.size, thrSweep.size))
twPhase     = np.zeros((mSeparated.size, thrSweep.size))
payload     = np.zeros((mSeparated.size, thrSweep.size))
mdotRCS     = 3 / 86400     # divide by seconds per day to get rate per second



# Loop over thrust:
for jj, thrust in enumerate(thrSweep): 
    # Loop over launch mass
    for ii,mLaunch in enumerate(mSeparated):

        # Calculate the DV to raise the orbit. The equation is representative 
        # of launch performance
        apogeeOrbit= 7.7999e-10*mLaunch**4-2.1506e-5*mLaunch**3+2.2196e-1*mLaunch**2-1.0181e3*mLaunch+1.7624e6
        dvReq   = cf.ApogeeRaise(apogeeOrbit)
        
        # Define the engine. Assume an Isp of 450 s
        engMain = cf.Engine(450, thrSweep[jj], 5.5, 'Biprop', 'Cryo')
        
        engRCS  = cf.Engine(220, 448, 1, 'Monoprop', 'NotCryo')

    
        if engMain.strCryo == 'Cryo':
            # Include chill-in and boiloff only for cryogenic sequence
            mdotOxBoiloff = 5/86400    # divide by seconds per day to get rate per second
            mdotFuelBoiloff = 10/86400  # divide by seconds per day to get rate per second 
            
            PreTLISett  = cf.Phase('Pre-TCM1 Settling',        mLaunch,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreTLIChill = cf.Phase('Pre-TCM1 Chill',   PreTLISett.mEnd,       0, engMain, 'Chill',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TLI         = cf.Phase('TLI',             PreTLIChill.mEnd,   dvReq, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            CoastToTCM1 = cf.Phase('Coast to TCM1',           TLI.mEnd,       0, engMain, 'Coast', 1*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            # Replace the PHASE_TYPE below with the appropriate string
            PreTCM1Sett = cf.Phase('Pre-TCM1 Settling',CoastToTCM1.mEnd,      0, engMain, 'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            PreTCM1Chill= cf.Phase('Pre-TCM1 Chill',  PreTCM1Sett.mEnd,       0, engMain, 'Chill',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            TCM1        = cf.Phase('TCM1',           PreTCM1Chill.mEnd,      20, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
            # Replace the TIME_HERE below with 2 days (i.e. 2*86400)
            CoastToTCM2 = cf.Phase('Coast to TCM2',          TCM1.mEnd,       0, engMain, 'Coast', 2*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
            TCM2        = cf.Phase('TCM2',            CoastToTCM2.mEnd,       5,  engRCS,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 
            # Replace the TIME_HERE below wit 1 day (i.e. 1*86400)
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
        OxTanks = cf.TankSet("Oxygen", "Al2219", 2, 1, 300000, Mission.mPropTotalOx)
        FuelTanks = cf.TankSet("Hydrogen", "Al2219", 2, 2, 300000, Mission.mPropTotalFuel)    
        MonoTanks = cf.TankSet("MMH", "Al2219", 1, 2, 300000, Mission.mPropTotalMono)    
        subs = cf.Subsystems(mLaunch, engMain, OxTanks, FuelTanks, MonoTanks, 100, 'Deployable', 'Large', 8)
        twPDIStart[ii,jj]=thrust/(DOI.mEnd*9.81) # we're saving this use it to plot later

        payload[ii,jj] = mLaunch - Mission.mPropTotalTotal - subs.mTotalAllowable
   



# Start the plotting stuff 
fig1 = plt.figure()
strLegend=list()
for ii in range(thrSweep.size):                   
    plt.plot(mSeparated, payload[:,ii], linewidth=3.0)
    strLegend.append('Thrust={0:6.0f} N'.format(thrSweep[ii]))
   
plt.grid()
plt.xlabel('Start Mass (kg)')
plt.ylabel('Payload (kg)')
plt.legend(strLegend)
plt.savefig('HW2_Payload_vs_Mass.png', dpi=300)


fig1 = plt.figure()
# Build up the legend string
strLegend=list()
for ii in range(mSeparated.size):                   
    plt.plot(twPDIStart[ii,:], payload[ii,:], linewidth=3.0)
    strLegend.append('Start Mass={0:5.0f} kg'.format(mSeparated[ii]))
plt.grid()
plt.xlabel('Thrust/Weight Ratio at PDI Start')
plt.ylabel('Payload (kg)')
plt.legend(strLegend)
plt.savefig('HW2_Payload_vs_TW.png', dpi=300)
