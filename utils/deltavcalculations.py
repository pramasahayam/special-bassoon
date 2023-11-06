from math import sqrt
from math import pi

def Hohmann(r1, r2, mu):
    r1 = r1 # initial circular orbit radius, km
    r2 = r2 # target circular orbit radius, km
    mu = mu # gravitational parameter, km^3/s^2
    
    totalDeltav = sqrt(mu/r1) * (sqrt((2*r2)/(r1 + r2)) - 1) + sqrt(mu/r2) * (1 - sqrt((2*r1)/(r1 + r2))) # km/s
    transferTime = pi * sqrt((r1 + r2)**3/(8*mu)) # s
    
    return totalDeltav, transferTime

def BiEllipticHohmann(r1, r2, rb, mu):
    r1 = r1 # initial circular orbit radius, km
    r2 = r2 # target circular orbit radius, km
    rb = rb # transfer ellipses common apoapsis radius, km --> larger means greater delta-v savings relative to Hohmann
    mu = mu # gravitational parameter, km^3/s^2

    a1 = (r1 + rb)/2 # semi-major axis of transfer ellipse 1
    a2 = (r2 + rb)/2 # semi-major axis of transfer ellipse 2
    
    totalDeltav = sqrt((2*mu/r1) - (mu/a1)) - sqrt(mu/r1) + sqrt((2*mu/rb) - (mu/a2)) - sqrt((2*mu/rb) - (mu/a1)) + sqrt((2*mu/r2) - (mu/a2)) - sqrt(mu/r2) # km/s
    transferTime = pi * sqrt(a1**3/mu) + pi * sqrt(a2**3/mu) # s
    
    return totalDeltav, transferTime