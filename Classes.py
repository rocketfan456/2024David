
import numpy as np #make sure you pull in numpy

def ApogeeRaise(ap0):
    """Calculates the dV required to raise orbit to 410,000 km apostasis"""
    # Vis-viva eq: v = sqrt(mu*(2/r - 1/a))

    # Gravitational parameter (km^3/s^2)
    mu = 398600

    # Radius of earth (km)
    eRadius = 6378
    
    # periapsis altitude (km)
    r = eRadius + 185

    # semi-major axis (km)
    # a0: initial; af: final semi-major axis
    a0 = (r + ap0 + eRadius) / 2
    af = (r + 410000 + eRadius) / 2

    # velocities at periapsis (km/s)
    v0 = np.sqrt(mu * (2/r - 1/a0))
    vf = np.sqrt(mu * (2/r - 1/af))

    # Change in velocity at periapsis needed to reach moon (km/s)
    dV = vf - v0

    # Change units to m/s
    dV = 1000 * dV

    # Round change in velocity to 3 decimal places
    # dV = round(dV, 3)

    return dV


# This function will output a summary of each phase
def PrintData(phaseList):
    print('{0:25s}'.format("------------------------------------------------------------------------" ))
    print('{0:20s}{1:>11s}{2:>11s}{3:>11s}{4:>13s}{5:>13s}{6:>14s}'.format("Phase Name", "DV (m/s)", "Mass0 (kg)", "MassF (kg)", "TotProp (kg)", "OxProp (kg)", "FuelProp (kg)"   ))
    print('{0:25s}'.format("------------------------------------------------------------------------" ))
    for curPhase in phaseList:
        print('{0:20s}{1:11.1f}{2:11.1f}{3:11.1f}{4:13.1f}{5:13.1f}{6:14.1f}'.format(curPhase.strName, curPhase.dvPhase, curPhase.mStart, curPhase.mEnd, curPhase.mPropImpulse, curPhase.mPropImpulseOx, curPhase.mPropImpulseFuel ))

# This class will create a generic "phase" which will do propellant 
# calculations
class Phase:

    def __init__(self,strName, mStart, dvPhase, clsEng, strPhaseType, dtPhase, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff):

        # Check if this is a T/W phase. If so, 
        # update the dV calculate the thrust-to-weight
        twPhase = clsEng.thrust/(mStart*9.81)
        if dvPhase<0:
            dvPhase = 4335*np.exp(-(twPhase) * 20.25) + 1880 #use the thrust-to-weight equation from the slides


        # Calculate Impulse Propellant Using Rocket Equation   
        # We specify Impulse because we'll have other types later
        mPropImpulse = mStart - mStart / (np.exp(dvPhase / (clsEng.isp * 9.81)))
        mPropImpulseReserve = 0.02*mPropImpulse
   
        
        # Modify phase duration if this is a burn 
        if dvPhase>0:
            dtPhase = mPropImpulse/clsEng.mdot
    
                # Move the Impulse propellant into the correct category
        if clsEng.strPropType == "Biprop":
            mPropImpulseOx = mPropImpulse*clsEng.mr/(1+clsEng.mr)
            mPropImpulseFuel = mPropImpulse/(1+clsEng.mr)
            
            mPropImpulseReserveOx = mPropImpulseReserve*clsEng.mr/(1+clsEng.mr)
            mPropImpulseReserveFuel = mPropImpulseReserve/(1+clsEng.mr)
            
            mPropImpulseMono = 0
            mPropImpulseReserveMono = 0
        elif clsEng.strPropType == "Monoprop":
            mPropImpulseOx = 0
            mPropImpulseFuel = 0
            
            mPropImpulseReserveOx = 0
            mPropImpulseReserveFuel = 0          
            
            mPropImpulseMono = mPropImpulse
            mPropImpulseReserveMono = mPropImpulseReserve
        
        # Determine boiloff losses
        mPropBoiloffOx = mdotOxBoiloff*dtPhase
        mPropBoiloffFuel = mdotFuelBoiloff*dtPhase
        mPropBoiloff   = mPropBoiloffOx + mPropBoiloffFuel
        
        # Determine RCS losses
        mPropRCS = mdotRCS*dtPhase
        
        # Check if this is a chill-in phase
        if strPhaseType =="Chill":
            mChill = 10
            mChillOx = 5
            mChillFuel = 5
        else:
            mChill=0
            mChillOx =0
            mChillFuel = 0
            
        if strPhaseType =="Settling":
            mSettling = 5
        else:
            mSettling=0

        
        # Determine final mass      
        mEnd = mStart - mPropImpulse - mPropBoiloff - mPropRCS - mChill - mSettling
        
        
        # Move data to class structure to save information
        self.mStart         = mStart
        self.mEnd           = mEnd
        self.dtPhase        = dtPhase
        self.dvPhase        = dvPhase
        self.clsEng         = clsEng
        self.mdotRCS        = mdotRCS
        self.mdotOxBoiloff   = mdotOxBoiloff
        self.mdotFuelBoiloff = mdotFuelBoiloff
        self.mPropImpulse   = mPropImpulse
        self.mPropImpulseOx = mPropImpulseOx
        self.mPropImpulseFuel = mPropImpulseFuel
        self.mPropImpulseMono = mPropImpulseMono
        self.mPropImpulseReserve = mPropImpulseReserve
        self.mPropImpulseReserveOx = mPropImpulseReserveOx
        self.mPropImpulseReserveFuel = mPropImpulseReserveFuel
        self.mPropImpulseReserveMono = mPropImpulseReserveMono
        self.mPropBoiloff       = mPropBoiloff
        self.mPropBoiloffOx     = mPropBoiloffOx
        self.mPropBoiloffFuel   = mPropBoiloffFuel
        self.mPropRCS           = mPropRCS
        self.twPhase            = twPhase
        self.mChill             = mChill
        self.mChillOx           = mChillOx
        self.mChillFuel         = mChillFuel
        self.mSettling          = mSettling
        
 
# This class creates a summary of the entire mission - summing things up across
# phases         
class MissionSummary:
    def __init__(self, tupPhases):
        """
        Inputs:
            tupPhases: list of phase classes
        
        """
        # Initialize variables 
        
        pctResdiual = 0.01
        
        mPropImpulse     = 0
        mPropImpulseOx   = 0
        mPropImpulseFuel = 0
        mPropImpulseMono = 0
        mPropImpulseReserve = 0
        mPropImpulseReserveOx = 0
        mPropImpulseReserveFuel = 0
        mPropImpulseReserveMono = 0
        mPropBoiloff     = 0
        mPropBoiloffOx   = 0
        mPropBoiloffFuel = 0
        mPropRCS         = 0 

        mPropChill     = 0
        mPropChillOx   = 0
        mPropChillFuel = 0

        mPropSettling = 0

        # sum up the usages by phase
        for curPhase in tupPhases:
            mPropImpulse     += curPhase.mPropImpulse 
            mPropImpulseOx   += curPhase.mPropImpulseOx
            mPropImpulseFuel += curPhase.mPropImpulseFuel
            mPropImpulseMono += curPhase.mPropImpulseMono
            
            mPropImpulseReserve +=  curPhase.mPropImpulseReserve
            mPropImpulseReserveOx +=  curPhase.mPropImpulseReserveOx
            mPropImpulseReserveFuel += curPhase.mPropImpulseReserveFuel
            mPropImpulseReserveMono +=  curPhase.mPropImpulseReserveMono
            
            mPropBoiloff     +=  curPhase.mPropBoiloff
            mPropBoiloffOx   +=  curPhase.mPropBoiloffOx
            mPropBoiloffFuel +=  curPhase.mPropBoiloffFuel
            mPropRCS         +=  curPhase.mPropRCS 
            
            mPropChill       += curPhase.mChill
            mPropChillOx     += curPhase.mChillOx
            mPropChillFuel   += curPhase.mChillFuel
            
            mPropSettling    += curPhase.mSettling


        # Stuff everything into self    
        mPropConsumedOx   = mPropImpulseOx   + mPropBoiloffOx + mPropChillOx
        mPropConsumedFuel = mPropImpulseFuel + mPropBoiloffFuel + mPropChillFuel
        mPropConsumedMono = mPropImpulseMono + mPropRCS + mPropSettling
        mPropConsumedTotal = mPropConsumedOx + mPropConsumedFuel + mPropConsumedMono

        mPropResidualOx    = pctResdiual*(mPropConsumedOx+mPropImpulseReserveOx)
        mPropResidualFuel  = pctResdiual*(mPropConsumedFuel+mPropImpulseReserveFuel)
        mPropResidualMono  = pctResdiual*(mPropConsumedMono+mPropImpulseReserveMono)
        mPropResidualTotal = mPropResidualOx + mPropResidualFuel + mPropResidualMono

        mPropAtLandingOx    = mPropResidualOx   +mPropImpulseReserveOx
        mPropAtLandingFuel  = mPropResidualFuel +mPropImpulseReserveFuel
        mPropAtLandingMono  = mPropResidualMono + mPropImpulseReserveMono
        mPropAtLandingTotal = mPropAtLandingOx + mPropAtLandingFuel + mPropAtLandingMono

        mPropTotalOx = mPropConsumedOx + mPropAtLandingOx
        mPropTotalFuel = mPropConsumedFuel + mPropAtLandingFuel
        mPropTotalMono = mPropConsumedMono + mPropAtLandingMono
        mPropTotalTotal = mPropTotalOx + mPropTotalFuel + mPropTotalMono

        dvPhase = np.zeros(len(tupPhases))
        for ii,curPhase in enumerate(tupPhases):
            dvPhase[ii] = curPhase.dvPhase 


        self.mPropImpulse      = mPropImpulse
        self.mPropImpulseOx    = mPropImpulseOx
        self.mPropImpulseFuel  = mPropImpulseFuel
        self.mPropImpulseMono  = mPropImpulseMono
        self.mPropImpulseReserve = mPropImpulseReserve
        self.mPropImpulseReserveOx = mPropImpulseReserveOx
        self.mPropImpulseReserveFuel = mPropImpulseReserveFuel
        self.mPropImpulseReserveMono = mPropImpulseReserveMono
        self.mPropBoiloff       = mPropBoiloff
        self.mPropBoiloffOx     = mPropBoiloffOx
        self.mPropBoiloffFuel   = mPropBoiloffFuel
        self.mPropRCS           = mPropRCS    
        self.mPropChill         = mPropChill
        self.mPropChillOx       = mPropChillOx
        self.mPropChillFuel     = mPropChillFuel
        self.mPropSettling      = mPropSettling
        self.mPropConsumedOx    = mPropConsumedOx
        self.mPropConsumedFuel  = mPropConsumedFuel
        self.mPropConsumedMono  = mPropConsumedMono
        self.mPropConsumedTotal = mPropConsumedTotal
        self.mPropResidualOx    = mPropResidualOx
        self.mPropResidualFuel  = mPropResidualFuel
        self.mPropResidualMono  = mPropResidualMono
        self.mPropResidualTotal = mPropResidualTotal
        self.mPropAtLandingOx   = mPropAtLandingOx
        self.mPropAtLandingFuel = mPropAtLandingFuel
        self.mPropAtLandingMono = mPropAtLandingMono
        self.mPropAtLandingTotal= mPropAtLandingTotal
        self.mPropTotalOx       = mPropTotalOx
        self.mPropTotalFuel     = mPropTotalFuel
        self.mPropTotalMono     = mPropTotalMono
        self.mPropTotalTotal    = mPropTotalTotal
        self.dvPhase            = dvPhase




# This builds up an engine, with an assumed thrust, specific impulse, and 
# mixture ratio
class Engine:
    def __init__(self,isp, thrust, mr, strPropType, strCryo):
        self.mr = mr
        self.isp = isp
        self.thrust = thrust
        self.mdot = thrust/isp/9.81
        self.strPropType = strPropType
        self.strCryo = strCryo

        
class TankSet:
    def __init__(self, strPropType,strMatType, nTanks, lMaxRadTank, presTank, mPropTotal):
        # General Parameters for Tanks
        pctUllage = 0.1         # Extra ullage room as a percentage of tank volume
        aMax      =  50         # Maximum acceleration (m/s2)
        pctFudge  =  1.2       # Fudge factor for welds, etc
        fosMat    =  1.5        # factor of safety for material (nd)
        
        # Tank material switch case
        if strMatType=="Al2219":
            rhoMat = 2840     # Density of material (kg/m3)
            sigMat = 2.9e8    # Yield Stress of material (Pa)
            thkMin = 0.004   # Minimum thickness of material (m)
        elif strMatType=="Stainless":
            rhoMat = 8000
            sigMat = 2.15e8
            thkMin = 0.0004
        elif strMatType == "Al-Li":
            rhoMat = 2700
            sigMat = 7e8
            thkMin = 0.004
    
        
        # Propellant Density switch case
        if strPropType=="Oxygen":
            rhoProp = 1140     # Density of propellant (kg/m3)
        elif strPropType=="Hydrogen":
            rhoProp = 70
        elif strPropType == "Methane":
            rhoProp = 420
        elif strPropType == "MMH":
            rhoProp = 866
        elif strPropType == "NTO":
            rhoProp = 1450
        elif strPropType == "RP-1":
            rhoProp = 820
        
        
        # Calculate propellant volume and volume per tank (include ullage)
        volPropTotal    = mPropTotal / rhoProp
        volPropPerTank  = volPropTotal / nTanks
        volPerTank      = volPropPerTank*(1+pctUllage)
        
        # Compare volume of tank to maximum allowable for given radius
        #    This will help us determine if the tank is a sphere or a pill.
        volMaxRadius    = 4/3*np.pi*(lMaxRadTank**3)
        
        if volMaxRadius>volPerTank:
            # A sphere with the max radius is too big, so calculate
            # the needed radius and set cylinder length to zero
            lRadiusTank = (volPerTank*3/4/np.pi)**(1/3)
            lCylTank   = 0
            
        else:
            # A sphere with the max radius is too small, so calculate
            # what the cylinder length will be
            lRadiusTank = lMaxRadTank
            lCylTank    = (volPerTank-4/3*np.pi*(lRadiusTank**3))/(np.pi*lRadiusTank**2)
       
        # Calculate the total length of the tank 
        lTankLength = lCylTank + 2*lRadiusTank
        
        # Calculate the surface area of each portion of the tank
        saDomesPerTank   = 4*np.pi*lRadiusTank**2
        saCylinderPerTank = 2*np.pi*lRadiusTank*lCylTank
        saTotalPerTank   = saCylinderPerTank + saDomesPerTank
       
        # Calculate the thickness.  Start with pressure
        presTotal = fosMat*(presTank + rhoProp*aMax*lTankLength)
        thkDomesCalc  = presTotal * lRadiusTank / (2 * sigMat)
        thkCylCalc    = 2*thkDomesCalc
        
        # Compare the pressure thickness to the minimum thickness
        thkDomes  = max(thkDomesCalc,thkMin)
        thkCyl    = max(thkCylCalc,thkMin )

        # Calculate the volume of the material
        volMatDomesPerTank = thkDomes*saDomesPerTank
        volMatCylPerTank   = thkCyl*saCylinderPerTank
        
        # Calculate the mass of each tank
        mDomesPerTank = volMatDomesPerTank*rhoMat
        mCylPerTank   = volMatCylPerTank*rhoMat
        
        # Add in the fudge factor 
        mTotalPerTank = (mDomesPerTank + mCylPerTank) * (pctFudge)
        mTotal        = (mTotalPerTank*nTanks)*(1.1**nTanks)
        
       
       
       
        # Stuff everything back into "self" for output
        self.strPropType = strPropType
        self.strMatType  = strMatType
        self.nTanks      = nTanks
        self.lMaxRadTank = lMaxRadTank
        self.presTank    = presTank
        self.mPropTotal  = mPropTotal
       
        self.pctUllage       = pctUllage
        self.rhoProp         = rhoProp
        self.volPropTotal    = volPropTotal
        self.volPropPerTank  = volPropPerTank
        self.volPerTank      = volPerTank
        self.volMaxRadius    = volMaxRadius
        self.lRadiusTank     = lRadiusTank
        self.lCylTank        = lCylTank
        self.lTankLength     = lTankLength
        self.saDomesPerTank     = saDomesPerTank
        self.saCylinderPerTank  = saCylinderPerTank
        self.saTotalPerTank  = saTotalPerTank
        self.presTotal       = presTotal
        self.thkDomesCalc    = thkDomesCalc
        self.thkCylCalc      = thkCylCalc
        self.thkDomes        = thkDomes
        self.thkCyl          = thkCyl
        self.volMatDomesPerTank = volMatDomesPerTank
        self.volMatCylPerTank = volMatCylPerTank
        self.mDomesPerTank   = mDomesPerTank
        self.mCylPerTank     = mCylPerTank
        self.mTotalPerTank   = mTotalPerTank
        self.mTotal          = mTotal


class Subsystems:
    def __init__(self, mVehicleStart, clsEng, clsOxTankSet,clsFuelTankSet, clsMonoTankSet, pwrDrawPayload, strArrayType, strLanderSize, tBattery):
        pctMarginArray      = 0.30
        pctDepthOfDischarge = 0.70
        nrgdenBattery       =  100 # w-hr/kg
        rhoSOFI             =  50 # Foam insulation density (kg/m3)
        thkSOFI             =  0.005 # Foam insulation thickness (m)
        rhoMLI              =  80 # multi-layer insulation density (kg/m3)
        thkMLI              =  0.001 # multi-layer insulation thickness (m)
        pctLandingGear      = 0.08
        pctStructure        = 0.20
        pctMGA              =  0.15 # mass growth allowance
        pctMargin           =  0.15 # mass margin percentage
        
        # Avionics
        mAvionics = 8*(mVehicleStart)**0.361
        
        # Electrical Subsystem      
        if strLanderSize =='Small':
            mPowerConversion = 30
            pwrDrawLander    =  300 # W
        else:
            mPowerConversion = 50
            pwrDrawLander    = 1200
        
        if strArrayType == 'Body':
            pwrdenArray =  30 # w/kg
        else: 
            pwrdenArray =  75 # w/kg
        
        lTank = max(clsOxTankSet.lTankLength, clsFuelTankSet.lTankLength) # pick the maximum length of your clsOxTankSet.lTankLength and clsFuelTankSet.lTanklength
        mWiring   = 1.058 * (mVehicleStart)**0.5 * (lTank)**0.25
        
        pwrTotalMargined = (1+pctMarginArray)*(pwrDrawLander + pwrDrawPayload) #the parenthesis is the sum of lander power and payload power
        mSolarArray      = pwrTotalMargined/pwrdenArray #divide the total margined power by the density 
        
        nrgTotal       = tBattery * pwrTotalMargined
        nrgTotalMargin = nrgTotal / pctDepthOfDischarge
        mBattery       = nrgTotalMargin / nrgdenBattery
        
        mElectrical = mPowerConversion+mWiring + mSolarArray + mBattery
        
        # Propulsion
        if strLanderSize =='Small':
            mRCS = 20
            mPressurization = 50
            mFeedlines = 20
        else:
            mRCS = 50
            mPressurization = 100
            mFeedlines = 50
            
        if clsOxTankSet.strPropType == 'Oxygen':
            mSOFIOx = thkSOFI*clsOxTankSet.saTotalPerTank*clsOxTankSet.nTanks*rhoSOFI
            mMLIOx  = thkMLI*clsOxTankSet.saTotalPerTank*clsOxTankSet.nTanks*rhoMLI
        else:
            mSOFIOx = 0
            mMLIOx  = thkMLI*clsOxTankSet.saTotalPerTank*clsOxTankSet.nTanks*rhoMLI

        if clsFuelTankSet.strPropType == 'Hydrogen':
            mSOFIFuel = thkSOFI*clsFuelTankSet.saTotalPerTank*clsFuelTankSet.nTanks*rhoSOFI
            mMLIFuel  = thkMLI*clsFuelTankSet.saTotalPerTank*clsFuelTankSet.nTanks*rhoMLI
            twEngine  = 40
        elif clsFuelTankSet.strPropType == 'Methane':
            mSOFIFuel = thkSOFI*clsFuelTankSet.saTotalPerTank*clsFuelTankSet.nTanks*rhoSOFI
            mMLIFuel  = thkMLI*clsFuelTankSet.saTotalPerTank*clsFuelTankSet.nTanks*rhoMLI
            twEngine = 50
        elif clsFuelTankSet.strPropType == 'MMH':
            mSOFIFuel = thkSOFI*clsFuelTankSet.saTotalPerTank*clsFuelTankSet.nTanks*rhoSOFI
            mMLIFuel  = thkMLI*clsFuelTankSet.saTotalPerTank*clsFuelTankSet.nTanks*rhoMLI
            twEngine = 50
        elif clsFuelTankSet.strPropType == 'RP-1':
            mSOFIFuel = 0
            mMLIFuel  = thkMLI*clsFuelTankSet.saTotalPerTank*clsFuelTankSet.nTanks*rhoMLI
            twEngine  = 60
        
        mEngine = 1/(twEngine/clsEng.thrust)/9.81

        #?
        mPropulsion = mRCS + mPressurization + mFeedlines + mSOFIOx + mMLIOx + mSOFIFuel + mMLIFuel + mEngine \
            + clsOxTankSet.mTotal + clsFuelTankSet.mTotal + clsMonoTankSet.mTotal

        # Thermal
        mThermal = 0.03*mVehicleStart
        
        # Structure
        mDryWithoutStructure = mAvionics + mElectrical + mPropulsion + mThermal 
        mStructureAndGear    = mDryWithoutStructure/(1-(pctStructure+pctLandingGear) )*(pctStructure+pctLandingGear)
        
        mTotalBasic     = mDryWithoutStructure + mStructureAndGear
        mMGA            = pctMGA * mTotalBasic
        mTotalPredicted = mTotalBasic + mMGA
        mMargin         = pctMargin * mTotalBasic
        mTotalAllowable = mTotalBasic + mMGA + mMargin
        
            
        self.mAvionics         = mAvionics
        self.mWiring           = mWiring
        self.pwrTotalMargined  = pwrTotalMargined
        self.mSolarArray       = mSolarArray
        self.nrgTotal          = nrgTotal
        self.nrgTotalMargin    = nrgTotalMargin
        self.mBattery          = mBattery
        self.mElectrical       = mElectrical
        self.mSOFIOx           = mSOFIOx
        self.mSOFIFuel         = mSOFIFuel
        self.mMLIOx            = mMLIOx
        self.mMLIFuel          = mMLIFuel
        self.twEngine          = twEngine
        self.mEngine           = mEngine
        self.mPropulsion       = mPropulsion
        self.mThermal          = mThermal
        self.mDryWithoutStructure = mDryWithoutStructure
        self.mStructureAndGear = mStructureAndGear
        self.mTotalBasic       = mTotalBasic
        self.mMGA              = mMGA
        self.mMargin           = mMargin
        self.mTotalPredicted   = mTotalPredicted
        self.mTotalAllowable   = mTotalAllowable
        
    
class Cost:
    def __init__(self,mDryMass, thrEngine, cstRocket):
        costRELander = 30000000*(mDryMass/2000)**0.4
        costNRELander = 12*costRELander
        costNREEngine  = 2500*thrEngine
        costNRETotal  = costNRELander+costNREEngine+cstRocket
        
        self.costRELander  = costRELander
        self.costNRELander = costNRELander
        self.costNREEngine = costNREEngine
        self.costNRETotal  = costNRETotal