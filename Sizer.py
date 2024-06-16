import numpy as np
import matplotlib.pyplot as plt
import Classes as cf
import FunctionFile as ff
import matplotlib.pyplot as plt


# Run through sequence
mSeparated  = np.linspace(3870, 8000, 4)# generate a linspace from 3870 to 8000 with four points
thrSweep    = np.linspace(3000, 15000, 13)
mStart      = np.zeros((mSeparated.size, thrSweep.size))
mFinal      = np.zeros((mSeparated.size, thrSweep.size))
twPDIStart  = np.zeros((mSeparated.size, thrSweep.size))
dv          = np.zeros((mSeparated.size, thrSweep.size))
twPhase     = np.zeros((mSeparated.size, thrSweep.size))
# Loop over thrust:
for jj, thrust in enumerate(thrSweep): 
    # Loop over launch mass
    for ii,mLaunch in enumerate(mSeparated):

        # Calculate the DV to raise the orbit. The equation is representative 
        # of launch performance
        apogeeOrbit= 7.7999e-10*mLaunch**4-2.1506e-5*mLaunch**3+2.2196e-1*mLaunch**2-1.0181e3*mLaunch+1.7624e6
        dvReq   = ff.ApogeeRaise(apogeeOrbit) # you may need to rename this to match your function
        
        # Define the engine. Assume an Isp of 450 s
        engMain = cf.Engine(450, thrSweep[jj], 5.5)

    
        TLI          = cf.Phase('TLI',    mLaunch,      dvReq, engMain)
        TCM1         = cf.Phase('TCM1',  TLI.mEnd,         20, engMain)
        TCM2         = cf.Phase('TCM2', TCM1.mEnd,          5, engMain) # 5 m/s 
        TCM3         = cf.Phase('TCM3', TCM2.mEnd,          5, engMain) # 5 m/s 
        LOI          = cf.Phase('LOI',   TCM3.mEnd,        850, engMain) # 850 m/s 
        TCM4         = cf.Phase('TCM4', LOI.mEnd,          5, engMain) # 5 m/s 
        DOI          = cf.Phase('DOI',   TCM4.mEnd,         25, engMain) # 25 m/s 
        PDI          = cf.Phase('PDI',   DOI.mEnd,         -1, engMain)
        
        twPDIStart[ii,jj]=thrust/(DOI.mEnd*9.81) # we're saving this use it to plot later
        mFinal[ii,jj] = PDI.mEnd
        
#?: Does TlI, TCM1, TCM2, ... PDI get replaced after each for-loop iteration?? #
phaseList = [TLI, TCM1, TCM2, TCM3, LOI, TCM4, DOI, PDI]
cf.PrintData(phaseList)


Mission = cf.MissionSummary(phaseList)
 



# Start the plotting stuff 
fig1 = plt.figure()
strLegend=list()
for ii in range(thrSweep.size):                   
    plt.plot(mSeparated, mFinal[:,ii], linewidth=3.0)
    strLegend.append('Thrust={0:6.0f} N'.format(thrSweep[ii]))
   
plt.grid()
plt.xlabel('Start Mass (kg)')
plt.ylabel('Payload (kg)')
plt.legend(strLegend)


fig1 = plt.figure()
# Build up the legend string
strLegend=list()
for ii in range(mSeparated.size):                   
    plt.plot(twPDIStart[ii,:], mFinal[ii,:], linewidth=3.0)
    strLegend.append('Start Mass={0:5.0f} kg'.format(mSeparated[ii]))
plt.grid()
plt.xlabel('Thrust/Weight Ratio at PDI Start')
plt.ylabel('Payload (kg)')
plt.legend(strLegend)




    
