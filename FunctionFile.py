import numpy as np

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
    dV = round(dV, 3)

    return dV

