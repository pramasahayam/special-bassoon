from math import sqrt
from math import pi

class DeltaVCalculator:
    def hohmannTransfer(body, r1, r2):
        # r1 = initial circular orbit radius, km
        # r2 = target circular orbit radius, km
        
        mu = body.mu # gravitational parameter, km^3/s^2
        
        a_transfer = (r1 + r2) / 2 # semi-major axis of transfer ellipse, km
        deltaVDeparture = sqrt(mu * (2/r1 - 1/a_transfer)) - sqrt((mu/r1)) # km/s
        deltaVArrival = (sqrt(mu/r2) - sqrt(mu * (2/r2 - 1/a_transfer))) # km/s
        
        totalDeltaV = deltaVDeparture + deltaVArrival # km/s
        transferTime = pi * sqrt(a_transfer**3 / mu) # s
        transferTimeConversions = [
            transferTime, # s
            transferTime/60, # min
            transferTime/3600, # hrs
            transferTime/86400, # days
        ]
        
        return totalDeltaV, transferTimeConversions

    def interplanetaryHohmannTransfer(body1, body2):
        if body1.orbital_center_mu == body2.orbital_center_mu: # body1/body2 must orbit same body
            r1 = body1.semimajoraxis
            r2 = body2.semimajoraxis

            mu = body1.orbital_center_mu
            
            a_transfer = (r1 + r2) / 2 # semi-major axis of transfer ellipse, km
            deltaVDeparture = sqrt(mu * (2/r1 - 1/a_transfer)) - sqrt((mu/r1)) # km/s
            deltaVArrival = (sqrt(mu/r2) - sqrt(mu * (2/r2 - 1/a_transfer))) # km/s
            
            totalDeltaV = deltaVDeparture + deltaVArrival # km/s
            transferTime = pi * sqrt(a_transfer**3 / mu) # s
            transferTimeConversions = [
                transferTime, # s
                transferTime/60, # min
                transferTime/3600, # hrs
                transferTime/86400, # days
            ]
            
            return totalDeltaV, transferTimeConversions

    def biEllipticHohmannTransfer(body, r1, r2, rb):
        # r1 initial circular orbit radius, km
        # r2 target circular orbit radius, km
        # rb transfer ellipses common apoapsis radius, km --> larger means greater delta-v savings relative to Hohmann

        mu = body.mu # gravitational parameter, km^3/s^2
        
        a1 = (r1 + rb)/2 # semi-major axis of transfer ellipse 1
        a2 = (r2 + rb)/2 # semi-major axis of transfer ellipse 2
        
        totalDeltaV = sqrt((2*mu/r1) - (mu/a1)) - sqrt(mu/r1) + sqrt((2*mu/rb) - (mu/a2)) - sqrt((2*mu/rb) - (mu/a1)) + sqrt((2*mu/r2) - (mu/a2)) - sqrt(mu/r2) # km/s
        transferTime = pi * sqrt(a1**3/mu) + pi * sqrt(a2**3/mu) # s
        transferTimeConversions = [
            transferTime, # s
            transferTime/60, # min
            transferTime/3600, # hrs
            transferTime/86400, # days
        ]
        
        return totalDeltaV, transferTimeConversions