from math import sqrt

def Hohmann(r1, r2, mu):
    r1 = r1 # departure circular orbit, km
    r2 = r2 # arrival circular orbit, km
    mu = mu # gravitational parameter, km^2/s
    
    totalDeltav = sqrt(mu/r1) * (sqrt((2*r2)/(r1 + r2)) - 1) + sqrt(mu/r2) * (1 - sqrt((2*r1)/(r1 + r2)))
    
    return totalDeltav # km/s