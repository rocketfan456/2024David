# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:26:02 2020

@author: jlamp
"""

import unittest
import FunctionFile as ff # need this for teh apogee function
import Classes_HW4 as cf   # edit this line to point to your Classes file
import numpy as np

class TestApogee(unittest.TestCase):
    def test_apogee_410000(self):
        dv = ff.ApogeeRaise(410000)
        np.testing.assert_approx_equal(dv, 0.0, 5)
    def test_apogee_185(self):
        dv = ff.ApogeeRaise(185)
        np.testing.assert_approx_equal(dv, 3142.2152618, 5)
        
class TestPhase(unittest.TestCase):
    def test_phase_1000(self):
        engMain = cf.Engine(450, 100, 4)
        tester = cf.Phase("TestPhase", 1000, 500, engMain)
        np.testing.assert_approx_equal(tester.mEnd, 892.915693, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 85.66744, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 21.41686, 5)
    def test_phase_tw(self):
        engMain = cf.Engine(450, 1500, 5)
        tester = cf.Phase("TestPhase", 1000, -1, engMain)
        np.testing.assert_approx_equal(tester.mEnd, 624.8336, 5)
        np.testing.assert_approx_equal(tester.dvPhase, 2076.00626, 5)
        np.testing.assert_approx_equal(tester.mPropImpulse, 375.16636, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseOx, 312.638639, 5)
        np.testing.assert_approx_equal(tester.mPropImpulseFuel, 62.527727, 5)

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
        np.testing.assert_approx_equal(tanks.mTotalPerTank, 134.105432, 5)      # total mass per tank with fudge factor
        np.testing.assert_approx_equal(tanks.mTotal, 147.515976, 5)             # total mass for the tank set
        
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
        np.testing.assert_approx_equal(tanks.mTotal, 204.132, 5)             # total mass for the tank set
        
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
        np.testing.assert_approx_equal(tanks.mTotal, 1089.563385, 5)             # total mass for the tank set
        
        
if __name__ =='__main__':
    unittest.main()