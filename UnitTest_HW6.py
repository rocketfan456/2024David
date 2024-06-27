# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:26:02 2020

@author: jlamp
"""

import unittest
import Classes as cf
import numpy as np

class TestApogee(unittest.TestCase):
    def test_apogee_410000(self):
        dv = cf.ApogeeRaise(410000)
        np.testing.assert_approx_equal(dv, 0)
    def test_apogee_185(self):
        dv = cf.ApogeeRaise(185)
        np.testing.assert_approx_equal(dv, 3142.2152618, 5)
        
class TestPhase(unittest.TestCase):
    def test_phase_1000(self):
        engMain = cf.Engine(450, 100, 4, 'Biprop', 'Cryo')
        mdotRCS = 10/86400
        mdotOxBoiloff = 10/86400
        mdotFuelBoiloff = 10/86400
        tester = cf.Phase('TLI', 1000,   500, engMain,  'Burn',   0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        np.testing.assert_approx_equal(tester.mStart, 1000, 5)
        np.testing.assert_approx_equal(tester.mEnd, 891.274292346793, 5)
        np.testing.assert_approx_equal(tester.dtPhase, 4727.236689470039, 5)
        np.testing.assert_approx_equal(tester.dvPhase, 500, 5)
        np.testing.assert_approx_equal(tester.mdotRCS, 0.000115740, 5)
        np.testing.assert_approx_equal(tester.mdotOxBoiloff, 0.0001157407, 5)
        np.testing.assert_approx_equal(tester.mdotFuelBoiloff, 0.000115740, 5)
        np.testing.assert_approx_equal(tester.mPropImpulse, 107.08430602, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 85.66744481, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 21.416861, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserve,2.14168612, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveOx, 1.7133488, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveFuel, 0.42833722, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloff, 1.094267752, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffOx, 0.54713387, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffFuel, 0.547133876, 5)
        np.testing.assert_approx_equal(tester.mPropRCS, 0.54713387, 5)
        np.testing.assert_approx_equal(tester.twPhase, 0.0101936799, 5)
        np.testing.assert_approx_equal(tester.mChill, 0, 5)
        np.testing.assert_approx_equal(tester.mChillOx, 0, 5)
        np.testing.assert_approx_equal(tester.mChillFuel, 0, 5)
    def test_phase_tw(self):
        engMain = cf.Engine(450, 1500, 5, 'Biprop', 'Cryo')
        mdotRCS = 15.2/86400
        mdotOxBoiloff = 40/86400
        mdotFuelBoiloff = 40/86400
        tester = cf.Phase('TLI', 1000,   -1, engMain,  'Burn',   0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        np.testing.assert_approx_equal(tester.mStart, 1000, 5)
        np.testing.assert_approx_equal(tester.mEnd, 623.61706196, 5)
        np.testing.assert_approx_equal(tester.dtPhase, 1104.11461890039, 5)
        np.testing.assert_approx_equal(tester.dvPhase, 2076.00626323, 5)
        np.testing.assert_approx_equal(tester.mdotRCS, 0.000175925, 6)
        np.testing.assert_approx_equal(tester.mdotOxBoiloff, 0.0004629629, 5)
        np.testing.assert_approx_equal(tester.mdotFuelBoiloff, 0.00046296, 5)
        np.testing.assert_approx_equal(tester.mPropImpulse, 375.16636729, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 312.6386394, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 62.52772788, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserve,7.50332734, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveOx, 6.25277278, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveFuel, 1.250554557, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloff, 1.02232835, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffOx, 0.511164175, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffFuel, 0.51116417544, 5)
        np.testing.assert_approx_equal(tester.mPropRCS, 0.1942423866, 5)
        np.testing.assert_approx_equal(tester.twPhase, 0.1529051987, 5)
        np.testing.assert_approx_equal(tester.mChill, 0, 5)
        np.testing.assert_approx_equal(tester.mChillOx, 0, 5)
        np.testing.assert_approx_equal(tester.mChillFuel, 0, 5)
        
    def test_phase_coast(self):
        engMain = cf.Engine(350, 12500, 5, 'Biprop', 'Cryo')
        mdotRCS = 3/86400
        mdotOxBoiloff = 40/86400
        mdotFuelBoiloff = 10/86400
        tester = cf.Phase('Coast to PDI', 1000,   0, engMain,  'Coast',  4*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        np.testing.assert_approx_equal(tester.mStart, 1000, 5)
        np.testing.assert_approx_equal(tester.mEnd, 788.0, 5)
        np.testing.assert_approx_equal(tester.dtPhase, 345600, 5)
        np.testing.assert_approx_equal(tester.dvPhase, 0, 5)
        np.testing.assert_approx_equal(tester.mdotRCS, 3.472222222222222e-05, 6)
        np.testing.assert_approx_equal(tester.mdotOxBoiloff, 0.00046296296, 5)
        np.testing.assert_approx_equal(tester.mdotFuelBoiloff,  0.000115740740, 5)
        np.testing.assert_approx_equal(tester.mPropImpulse, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserve,0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloff, 200, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffOx, 160, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffFuel, 40, 5)
        np.testing.assert_approx_equal(tester.mPropRCS, 12, 5)
        np.testing.assert_approx_equal(tester.twPhase, 1.2742099, 5)
        np.testing.assert_approx_equal(tester.mChill, 0, 5)
        np.testing.assert_approx_equal(tester.mChillOx, 0, 5)
        np.testing.assert_approx_equal(tester.mChillFuel, 0, 5)
    def test_phase_chill(self):
        engMain = cf.Engine(350, 12500, 5, 'Biprop', 'Cryo')
        mdotRCS = 3/86400
        mdotOxBoiloff = 10/86400
        mdotFuelBoiloff = 30/86400
        tester = cf.Phase('PrePDI Chill', 1000,   0, engMain,  'Chill',  0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        np.testing.assert_approx_equal(tester.mStart, 1000, 5)
        np.testing.assert_approx_equal(tester.mEnd, 990, 5)
        np.testing.assert_approx_equal(tester.dtPhase, 0, 5)
        np.testing.assert_approx_equal(tester.dvPhase, 0, 5)
        np.testing.assert_approx_equal(tester.mdotRCS, 3.472222222222222e-05, 6)
        np.testing.assert_approx_equal(tester.mdotOxBoiloff, 0.00011574074074074075, 5)
        np.testing.assert_approx_equal(tester.mdotFuelBoiloff,  0.00034722222222222224, 5)
        np.testing.assert_approx_equal(tester.mPropImpulse, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserve,0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloff, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropRCS, 0, 5)
        np.testing.assert_approx_equal(tester.twPhase, 1.2742099, 5)
        np.testing.assert_approx_equal(tester.mChill, 10, 5)
        np.testing.assert_approx_equal(tester.mChillOx, 5, 5)
        np.testing.assert_approx_equal(tester.mChillFuel, 5, 5) 
        
    def test_phase_rcs(self):
        engRCS = cf.Engine(220, 400, 5, 'Monoprop', 'NotCryo')
        mdotRCS = 3/86400
        mdotOxBoiloff = 10/86400
        mdotFuelBoiloff = 30/86400
        tester = cf.Phase('TCM3', 1500,   5, engRCS,  'Burn',  0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        np.testing.assert_approx_equal(tester.mStart, 1500, 5)
        np.testing.assert_approx_equal(tester.mEnd, 1496.5195834, 5)
        np.testing.assert_approx_equal(tester.dtPhase, 18.72829727, 5)
        np.testing.assert_approx_equal(tester.dvPhase, 5, 5)
        np.testing.assert_approx_equal(tester.mdotRCS, 3.472222222222222e-05, 6)
        np.testing.assert_approx_equal(tester.mdotOxBoiloff, 0.00011574074074074075, 5)
        np.testing.assert_approx_equal(tester.mdotFuelBoiloff,  0.00034722222222222224, 5)
        np.testing.assert_approx_equal(tester.mPropImpulse, 3.47109577, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseMono, 3.47109577, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserve,0.0694219155, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveMono, 0.0694219155, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloff, 0.0086705079, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffOx, 0.00216762699, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffFuel, 0.006502880, 5)
        np.testing.assert_approx_equal(tester.mPropRCS, 0.000650288, 5)
        np.testing.assert_approx_equal(tester.twPhase, 0.0271831, 5)
        np.testing.assert_approx_equal(tester.mChill, 0, 5)
        np.testing.assert_approx_equal(tester.mChillOx, 0, 5)
        np.testing.assert_approx_equal(tester.mChillFuel, 0, 5) 
        
    def test_phase_settling(self):
        engRCS = cf.Engine(220, 400, 5, 'Monoprop', 'NotCryo')
        mdotRCS = 3/86400
        mdotOxBoiloff = 10/86400
        mdotFuelBoiloff = 30/86400
        tester = cf.Phase('PreTLI Settling', 1500,   0, engRCS,  'Settling',  0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        np.testing.assert_approx_equal(tester.mStart, 1500, 5)
        np.testing.assert_approx_equal(tester.mEnd, 1495, 5)
        np.testing.assert_approx_equal(tester.dtPhase, 0, 5)
        np.testing.assert_approx_equal(tester.dvPhase, 0, 5)
        np.testing.assert_approx_equal(tester.mdotRCS, 3.472222222222222e-05, 6)
        np.testing.assert_approx_equal(tester.mdotOxBoiloff, 0.00011574074074074075, 5)
        np.testing.assert_approx_equal(tester.mdotFuelBoiloff,  0.00034722222222222224, 5)
        np.testing.assert_approx_equal(tester.mPropImpulse, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserve,0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseReserveMono, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloff, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffOx, 0, 5)
        np.testing.assert_approx_equal(tester.mPropBoiloffFuel, 0, 5)
        np.testing.assert_approx_equal(tester.mPropRCS, 0, 5)
        np.testing.assert_approx_equal(tester.twPhase, 0.0271831, 5)
        np.testing.assert_approx_equal(tester.mChill, 0, 5)
        np.testing.assert_approx_equal(tester.mChillOx, 0, 5)
        np.testing.assert_approx_equal(tester.mChillFuel, 0, 5) 
        np.testing.assert_approx_equal(tester.mSettling, 5, 5) 

class TestTankset(unittest.TestCase):
    def test_al2219_oxygen_single_tank(self):
        tanks = cf.TankSet("Oxygen", "Al2219", 1, 0.85, 300000, 3000)
        np.testing.assert_approx_equal(tanks.volPropTotal, 2.6315789, 5)     # Prop only total
        np.testing.assert_approx_equal(tanks.volPropPerTank, 2.6315789, 5)   # Prop only per tank
        np.testing.assert_approx_equal(tanks.volPerTank, 2.8947368, 5)       # Total including ullage
        np.testing.assert_approx_equal(tanks.volMaxRadius, 2.5724407, 5)     # Volume of a sphere with max radius
        np.testing.assert_approx_equal(tanks.lCylTank, 0.1419931, 5)         # length of cylindrical section
        np.testing.assert_approx_equal(tanks.lTankLength, 1.8419931, 5)      # overall tank length
        np.testing.assert_approx_equal(tanks.saDomesPerTank, 9.07920276, 5)  # surface area of domes
        np.testing.assert_approx_equal(tanks.saCylinderPerTank, 0.75834366, 5)     # surface area of cylinder
        np.testing.assert_approx_equal(tanks.saTotalPerTank, 9.83754643, 5)         # total surface area of tank
        np.testing.assert_approx_equal(tanks.presTotal, 607490.41083, 5)        # total pressure in the tank
        np.testing.assert_approx_equal(tanks.thkDomesCalc, 0.0008902876, 5)     # required dome thickness (before minimum comparison)
        np.testing.assert_approx_equal(tanks.thkCylCalc, 0.001780575, 5)        # required cylinder thickness (before minimum comparison)
        np.testing.assert_approx_equal(tanks.thkDomes, 0.004, 5)           # thickness of dome used (after minimum comparison)
        np.testing.assert_approx_equal(tanks.thkCyl, 0.004, 5)             # thickness of cylinder used (after minimum comparison)
        np.testing.assert_approx_equal(tanks.volMatDomesPerTank, 0.036316811, 5)      # volume of material in domes
        np.testing.assert_approx_equal(tanks.volMatCylPerTank, 0.00303337, 5)   # volume of material in cylinder
        np.testing.assert_approx_equal(tanks.mDomesPerTank, 103.139743, 5)      # mass of domes
        np.testing.assert_approx_equal(tanks.mCylPerTank, 8.61478403, 5)        # mass of cylinder
        np.testing.assert_approx_equal(tanks.mTotalPerTank,134.10543298, 5)      # total mass per tank with fudge factor
        np.testing.assert_approx_equal(tanks.mTotal, 147.515976284, 5)             # total mass for the tank set
        
    def test_al2219_oxygen_two_tanks(self):
        tanks = cf.TankSet("Oxygen", "Al2219", 2, 0.85, 300000, 3000)
        np.testing.assert_approx_equal(tanks.volPropTotal, 2.63157894, 5)     # Prop only total
        np.testing.assert_approx_equal(tanks.volPropPerTank, 1.3157894, 5)   # Prop only per tank
        np.testing.assert_approx_equal(tanks.volPerTank, 1.4473684, 5)       # Total including ullage
        np.testing.assert_approx_equal(tanks.volMaxRadius, 2.5724407, 5)     # Volume of a sphere with max radius
        np.testing.assert_approx_equal(tanks.lCylTank, 0.00000, 5)         # length of cylindrical section
        np.testing.assert_approx_equal(tanks.lTankLength, 1.40343883, 5)      # overall tank length
        np.testing.assert_approx_equal(tanks.saDomesPerTank, 6.187808334, 5)  # surface area of domes
        np.testing.assert_approx_equal(tanks.saCylinderPerTank, 0.0000, 5)     # surface area of cylinder
        np.testing.assert_approx_equal(tanks.saTotalPerTank, 6.187808334, 5)         # total surface area of tank
        np.testing.assert_approx_equal(tanks.presTotal, 569994.02048, 5)        # total pressure in the tank
        np.testing.assert_approx_equal(tanks.thkDomesCalc, 0.000689613, 5)     # required dome thickness (before minimum comparison)
        np.testing.assert_approx_equal(tanks.thkCylCalc, 0.001379227, 5)        # required cylinder thickness (before minimum comparison)
        np.testing.assert_approx_equal(tanks.thkDomes, 0.004, 5)           # thickness of dome used (after minimum comparison)
        np.testing.assert_approx_equal(tanks.thkCyl, 0.004, 5)             # thickness of cylinder used (after minimum comparison)
        np.testing.assert_approx_equal(tanks.volMatDomesPerTank, 0.02475123, 5)      # volume of material in domes
        np.testing.assert_approx_equal(tanks.volMatCylPerTank, 0.00, 5)   # volume of material in cylinder
        np.testing.assert_approx_equal(tanks.mDomesPerTank, 70.29350267623, 5)      # mass of domes
        np.testing.assert_approx_equal(tanks.mCylPerTank, 0.00, 5)        # mass of cylinder
        np.testing.assert_approx_equal(tanks.mTotalPerTank, 84.35220321, 5)      # total mass per tank with fudge factor
        np.testing.assert_approx_equal(tanks.mTotal, 204.13233177, 5)             # total mass for the tank set
        
    def test_stainless_hydrogen_one_tank(self):
        tanks = cf.TankSet("Hydrogen", "Stainless", 1, 3.85, 300000, 2000)
        np.testing.assert_approx_equal(tanks.volPropTotal, 28.571428, 5)     # Prop only total
        np.testing.assert_approx_equal(tanks.volPropPerTank, 28.571428, 5)   # Prop only per tank
        np.testing.assert_approx_equal(tanks.volPerTank, 31.4285714, 5)       # Total including ullage
        np.testing.assert_approx_equal(tanks.volMaxRadius, 239.040119, 5)     # Volume of a sphere with max radius
        np.testing.assert_approx_equal(tanks.lRadiusTank, 1.957696, 5)         # Actual radius of the tank
        np.testing.assert_approx_equal(tanks.lCylTank, 0.00000, 5)         # length of cylindrical section
        np.testing.assert_approx_equal(tanks.lTankLength, 3.9153928147, 5)      # overall tank length
        np.testing.assert_approx_equal(tanks.saDomesPerTank, 48.161560, 5)  # surface area of domes
        np.testing.assert_approx_equal(tanks.saCylinderPerTank, 0.0000, 5)     # surface area of cylinder
        np.testing.assert_approx_equal(tanks.saTotalPerTank, 48.161560, 5)         # total surface area of tank
        np.testing.assert_approx_equal(tanks.presTotal, 470555.812277, 5)        # total pressure in the tank
        np.testing.assert_approx_equal(tanks.thkDomesCalc, 0.002142338, 5)     # required dome thickness (before minimum comparison)
        np.testing.assert_approx_equal(tanks.thkCylCalc, 0.00428467, 5)        # required cylinder thickness (before minimum comparison)
        np.testing.assert_approx_equal(tanks.thkDomes, 0.00214233, 5)           # thickness of dome used (after minimum comparison)
        np.testing.assert_approx_equal(tanks.thkCyl, 0.004284676, 5)             # thickness of cylinder used (after minimum comparison)
        np.testing.assert_approx_equal(tanks.volMatDomesPerTank, 0.103178350864, 5)      # volume of material in domes
        np.testing.assert_approx_equal(tanks.volMatCylPerTank, 0.00, 5)   # volume of material in cylinder
        np.testing.assert_approx_equal(tanks.mDomesPerTank, 825.4268069, 5)      # mass of domes
        np.testing.assert_approx_equal(tanks.mCylPerTank, 0.00, 5)        # mass of cylinder
        np.testing.assert_approx_equal(tanks.mTotalPerTank, 990.512168, 5)      # total mass per tank with fudge factor
        np.testing.assert_approx_equal(tanks.mTotal, 1089.5633851, 5)             # total mass for the tank set
class TestSubsystems(unittest.TestCase):
    def test_oxygen_hydrogen_large(self):    
        eng = cf.Engine(450, 8000, 4, 'Biprop', 'Cryo')
        oxtanks = cf.TankSet("Oxygen", "Al2219", 1, 0.85, 300000, 3000)
        fueltanks = cf.TankSet("Hydrogen", "Stainless", 1, 3.85, 300000, 2000)
        monotanks = cf.TankSet("MMH", "Al2219",1,1,300000,100)
        subs = cf.Subsystems(10000, eng, oxtanks, fueltanks, monotanks, 100, 'Body', 'Large', 8)
        np.testing.assert_approx_equal(subs.mAvionics, 222.3770614, 5)          # avionics mass
        np.testing.assert_approx_equal(subs.mWiring, 148.8262375, 5)            # wiring mass 
        np.testing.assert_approx_equal(subs.pwrTotalMargined, 1690.0, 5)        # Total power draw including margin
        np.testing.assert_approx_equal(subs.mSolarArray, 56.33333, 5)           # solar array mass
        np.testing.assert_approx_equal(subs.nrgTotal, 13520.0, 5)         # total energy for battery without depth of discharge
        np.testing.assert_approx_equal(subs.nrgTotalMargin, 19314.2857142, 5)         # total energy of battery including depth of discharge
        np.testing.assert_approx_equal(subs.mBattery, 193.14285714285714, 5)      # mass of battery
        np.testing.assert_approx_equal(subs.mElectrical, 448.30242802685075, 5)  # mass of electrical subsystem
        np.testing.assert_approx_equal(subs.mSOFIOx, 2.4593866084485203, 5)     # mass of SOFI for ox tanks
        np.testing.assert_approx_equal(subs.mSOFIFuel, 12.040390166125304, 5)         # mass of SOFI for fuel tanks
        np.testing.assert_approx_equal(subs.mMLIOx, 0.7870037147035265, 5)        # mass of MLI for Ox tanks
        np.testing.assert_approx_equal(subs.mMLIFuel, 3.8529248531600975, 5)     # mass of MLI for fuel tanks
        np.testing.assert_approx_equal(subs.twEngine, 40.0, 5)        # thrust to weight of the engine
        np.testing.assert_approx_equal(subs.mEngine, 20.38735983690112, 5)           # mass of the engine    
        np.testing.assert_approx_equal(subs.mPropulsion, 1494.9303970350272, 5)      # mass of propulsion subsystem
        np.testing.assert_approx_equal(subs.mThermal, 300.0, 5)  # mass of thermal subsystem 
        np.testing.assert_approx_equal(subs.mDryWithoutStructure, 2465.609886482621, 5)     # mass of everything but structure and gear
        np.testing.assert_approx_equal(subs.mStructureAndGear, 958.84828918, 5)         # mass of structure and gear
        np.testing.assert_approx_equal(subs.mTotalBasic, 3424.458175670307, 5)        # basic mass
        np.testing.assert_approx_equal(subs.mMGA, 513.668726350546, 5)     # mass growth allowance
        np.testing.assert_approx_equal(subs.mMargin, 513.668726350546, 5)        # margin
        np.testing.assert_approx_equal(subs.mTotalPredicted, 3938.126902020853, 5)           # predicted mass
        np.testing.assert_approx_equal(subs.mTotalAllowable,  4451.795628371399, 5)           # allowable mass
    def test_oxygen_methane_small(self):    
        eng = cf.Engine(370, 10000, 4, 'Biprop', 'Cryo')
        oxtanks = cf.TankSet("Oxygen", "Al2219", 1, 0.85, 300000, 1000)
        fueltanks = cf.TankSet("Methane", "Al2219", 1, 3.85, 300000, 1000)
        monotanks = cf.TankSet("MMH", "Al2219",1,1,300000,100)
        subs = cf.Subsystems(5000, eng, oxtanks, fueltanks, monotanks, 100, 'Deployable', 'Small', 8)
        np.testing.assert_approx_equal(subs.mAvionics, 173.14827074792632, 5)          # avionics mass
        np.testing.assert_approx_equal(subs.mWiring, 85.55250577167209, 5)            # wiring mass 
        np.testing.assert_approx_equal(subs.pwrTotalMargined, 520.0, 5)        # Total power draw including margin
        np.testing.assert_approx_equal(subs.mSolarArray, 6.9333333333, 5)           # solar array mass
        np.testing.assert_approx_equal(subs.nrgTotal, 4160.0, 5)         # total energy for battery without depth of discharge
        np.testing.assert_approx_equal(subs.nrgTotalMargin, 5942.85714285, 5)         # total energy of battery including depth of discharge
        np.testing.assert_approx_equal(subs.mBattery, 59.428571, 5)      # mass of battery
        np.testing.assert_approx_equal(subs.mElectrical, 181.91441053357, 5)  # mass of electrical subsystem
        np.testing.assert_approx_equal(subs.mSOFIOx, 1.180545388386, 5)     # mass of SOFI for ox tanks
        np.testing.assert_approx_equal(subs.mSOFIFuel, 2.29713435151045, 5)         # mass of SOFI for fuel tanks
        np.testing.assert_approx_equal(subs.mMLIOx, 0.3777745242837968, 5)        # mass of MLI for Ox tanks
        np.testing.assert_approx_equal(subs.mMLIFuel, 0.7350829924833446, 5)     # mass of MLI for fuel tanks
        np.testing.assert_approx_equal(subs.twEngine, 50.0, 5)        # thrust to weight of the engine
        np.testing.assert_approx_equal(subs.mEngine, 20.38735983690112, 5)           # mass of the engine    
        np.testing.assert_approx_equal(subs.mPropulsion, 341.8958804759, 5)      # mass of propulsion subsystem
        np.testing.assert_approx_equal(subs.mThermal, 150.0, 5)  # mass of thermal subsystem 
        np.testing.assert_approx_equal(subs.mDryWithoutStructure, 846.95856175, 5)     # mass of everything but structure and gear
        np.testing.assert_approx_equal(subs.mStructureAndGear, 329.37277401678233, 5)         # mass of structure and gear
        np.testing.assert_approx_equal(subs.mTotalBasic, 1176.3313357742225, 5)        # basic mass
        np.testing.assert_approx_equal(subs.mMGA, 176.44970036613336, 5)     # mass growth allowance
        np.testing.assert_approx_equal(subs.mMargin, 176.44970036613336, 5)        # margin
        np.testing.assert_approx_equal(subs.mTotalPredicted, 1352.7810361403558, 5)           # predicted mass
        np.testing.assert_approx_equal(subs.mTotalAllowable,  1529.2307365064892, 5)           # allowable mass
class TestCost(unittest.TestCase):
    def test_no_engine(self):    
        dryMass = 4000
        thrEng = 0
        cost = cf.Cost(dryMass,thrEng, 60000000)
        np.testing.assert_approx_equal(cost.costRELander, 39585237.3231868, 5)         
        np.testing.assert_approx_equal(cost.costNRELander, 475022847.8782419, 5)            
        np.testing.assert_approx_equal(cost.costNREEngine, 0.0, 5)       
        np.testing.assert_approx_equal(cost.costNRETotal, 535022847.8782419, 5)           
    def test_with_engine(self):    
        dryMass = 4000
        thrEng = 15000
        cost = cf.Cost(dryMass,thrEng, 100000000)
        np.testing.assert_approx_equal(cost.costRELander, 39585237.3231868, 5)         
        np.testing.assert_approx_equal(cost.costNRELander, 475022847.8782419, 5)            
        np.testing.assert_approx_equal(cost.costNREEngine, 37500000, 5)       
        np.testing.assert_approx_equal(cost.costNRETotal, 612522847.87824196, 5)  
class TestMission(unittest.TestCase):
    def test_sequence(self):
        mdotRCS = 3/86400
        mdotOxBoiloff = 5/86400    # divide by seconds per day to get rate per second
        mdotFuelBoiloff = 10/86400  # divide by seconds per day to get rate per second 
            
        engMain = cf.Engine(450, 25000, 5.5, 'Biprop', 'Cryo')
        engRCS  = cf.Engine(220, 448, 1, 'Monoprop', 'NotCryo')

        
        PreTLISett  = cf.Phase('Pre-TCM1 Settling',        10000,       0, engMain,'Settling',      0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        PreTLIChill = cf.Phase('Pre-TCM1 Chill',   PreTLISett.mEnd,     0, engMain, 'Chill',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        TLI         = cf.Phase('TLI',             PreTLIChill.mEnd,   500, engMain,  'Burn',        0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        CoastToTCM2 = cf.Phase('Coast to TCM2',          TLI.mEnd,       0, engMain, 'Coast', 2*86400, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff)
        TCM2        = cf.Phase('TCM2',            CoastToTCM2.mEnd,       5,  engRCS,  'Burn',       0, mdotRCS, mdotOxBoiloff, mdotFuelBoiloff) 

        Sequence = [PreTLISett, PreTLIChill, TLI, CoastToTCM2, TCM2]
        Mission = cf.MissionSummary(Sequence)
        np.testing.assert_approx_equal(Mission.mPropImpulse, 1089.7850436865483, 5)          # avionics mass
        np.testing.assert_approx_equal(Mission.mPropImpulseOx, 904.7388270959204, 5)            # wiring mass 
        np.testing.assert_approx_equal(Mission.mPropImpulseFuel, 164.4979685628946, 5)        # Total power draw including margin
        np.testing.assert_approx_equal(Mission.mPropImpulseMono, 20.54824802773328, 5)           # solar array mass
        np.testing.assert_approx_equal(Mission.mPropImpulseReserve, 21.795700873730965, 5)         # total energy for battery without depth of discharge
        np.testing.assert_approx_equal(Mission.mPropImpulseReserveOx, 18.094776541918407, 5)         # total energy of battery including depth of discharge
        np.testing.assert_approx_equal(Mission.mPropImpulseReserveFuel, 3.2899593712578925, 5)      # mass of battery
        np.testing.assert_approx_equal(Mission.mPropImpulseReserveMono, 0.4109649605546656, 5)  # mass of electrical subsystem
        np.testing.assert_approx_equal(Mission.mPropBoiloff, 30.049964441594796, 5)     # mass of SOFI for ox tanks
        np.testing.assert_approx_equal(Mission.mPropBoiloffOx, 10.016654813864932, 5)         # mass of SOFI for fuel tanks
        np.testing.assert_approx_equal(Mission.mPropBoiloffFuel, 20.033309627729864, 5)        # mass of MLI for Ox tanks
        np.testing.assert_approx_equal(Mission.mPropRCS, 6.00999288831896, 5)     # mass of MLI for fuel tanks
        np.testing.assert_approx_equal(Mission.mPropChill, 10.0, 5)        # thrust to weight of the engine
        np.testing.assert_approx_equal(Mission.mPropChillOx, 5, 5)           # mass of the engine    
        np.testing.assert_approx_equal(Mission.mPropChillFuel, 5, 5)      # mass of propulsion subsystem
        np.testing.assert_approx_equal(Mission.mPropSettling, 5.0, 5)  # mass of thermal subsystem 
        np.testing.assert_approx_equal(Mission.mPropConsumedOx, 919.7554819097854, 5)     # mass of everything but structure and gear
        np.testing.assert_approx_equal(Mission.mPropConsumedFuel, 189.53127819062448, 5)     # mass of everything but structure and gear
        np.testing.assert_approx_equal(Mission.mPropConsumedMono, 31.55824091605224, 5)         # mass of structure and gear
        np.testing.assert_approx_equal(Mission.mPropConsumedTotal, 1140.8450010164622, 5)        # basic mass
        np.testing.assert_approx_equal(Mission.mPropResidualOx, 9.378502584517038, 5)     # mass growth allowance
        np.testing.assert_approx_equal(Mission.mPropResidualFuel, 1.9282123756188236, 5)        # margin
        np.testing.assert_approx_equal(Mission.mPropResidualMono, 0.3196920587660691, 5)           # predicted mass
        np.testing.assert_approx_equal(Mission.mPropResidualTotal,  11.626407018901931, 5)           # allowable mass
        np.testing.assert_approx_equal(Mission.mPropAtLandingOx, 27.473279126435443, 5)          # avionics mass
        np.testing.assert_approx_equal(Mission.mPropAtLandingFuel, 5.218171746876716, 5)            # wiring mass 
        np.testing.assert_approx_equal(Mission.mPropAtLandingMono, 0.7306570193207347, 5)        # Total power draw including margin
        np.testing.assert_approx_equal(Mission.mPropAtLandingTotal, 33.422107892632894, 5)           # solar array mass
        np.testing.assert_approx_equal(Mission.mPropTotalOx, 947.2287610362209, 5)         # total energy for battery without depth of discharge
        np.testing.assert_approx_equal(Mission.mPropTotalFuel, 194.7494499375012, 5)         # total energy of battery including depth of discharge
        np.testing.assert_approx_equal(Mission.mPropTotalMono, 32.28889793537298, 5)      # mass of battery
        np.testing.assert_approx_equal(Mission.mPropTotalTotal, 1174.267108909095, 5)  # mass of electrical subsystem
  
if __name__ =='__main__':
    unittest.main()