from math import sqrt
from math import pi
from space_bodies import *
import datetime
from skyfield.api import load

class DeltaVCalculator:
    def __init__(self):
        self.space_bodies = [
            Sun(), Earth(), Mercury(), Venus(), Mars(), Jupiter(),
            Saturn(), Uranus(), Neptune(), Pluto(), Moon()
        ]
    
    def hohmann_transfer(self, body_index, r1, r2):
        # r1 = initial circular orbit radius, km
        # r2 = target circular orbit radius, km
        
        body = self.space_bodies[body_index]
        
        mu = body.mu # gravitational parameter, km^3/s^2
        
        a_transfer = (r1 + r2) / 2 # semi-major axis of transfer ellipse, km
        deltav_departure = abs(sqrt(mu * (2/r1 - 1/a_transfer)) - sqrt((mu/r1))) # km/s
        deltav_arrival = abs((sqrt(mu/r2) - sqrt(mu * (2/r2 - 1/a_transfer)))) # km/s
        
        total_deltav = deltav_departure + deltav_arrival # km/s
        transfer_time = pi * sqrt(a_transfer**3 / mu) # s
        transfer_time_conversions = [
            transfer_time, # s
            transfer_time/60, # min
            transfer_time/3600, # hrs
            transfer_time/86400, # days
        ]
        
        return total_deltav, transfer_time_conversions

    def bi_elliptic_hohmann_transfer(self, body_index, r1, r2, rb):
        # r1 initial circular orbit radius, km
        # r2 target circular orbit radius, km
        # rb transfer ellipses common apoapsis radius, km --> larger means greater delta-v savings relative to Hohmann

        body = self.space_bodies[body_index]
        mu = body.mu # gravitational parameter, km^3/s^2
        
        a1 = (r1 + rb)/2 # semi-major axis of transfer ellipse 1
        a2 = (r2 + rb)/2 # semi-major axis of transfer ellipse 2
        
        total_deltav = sqrt((2*mu/r1) - (mu/a1)) - sqrt(mu/r1) + sqrt((2*mu/rb) - (mu/a2)) - sqrt((2*mu/rb) - (mu/a1)) + sqrt((2*mu/r2) - (mu/a2)) - sqrt(mu/r2) # km/s
        transfer_time = pi * sqrt(a1**3/mu) + pi * sqrt(a2**3/mu) # s
        transfer_time_conversions = [
            transfer_time, # s
            transfer_time/60, # min
            transfer_time/3600, # hrs
            transfer_time/86400, # days
        ]
        
        return total_deltav, transfer_time_conversions
    
    def interplanetary_hohmann_transfer(self, body1_index, orbit_r1, body2_index, orbit_r2):
        # assumptions: orbit same body, coplanar, 0 eccentricity, impulsive burns, ideal angular separation
        body1 = self.space_bodies[body1_index]
        body2 = self.space_bodies[body2_index]
        
        if body1.orbital_center_mu == body2.orbital_center_mu: # body1/body2 must orbit same body
            
            v_orbit_r1 = sqrt(body1.mu / orbit_r1) # velocity of inital orbit around body1
            v_esc_orbit_r1 = sqrt(2 * body1.mu / orbit_r1) # escape velocity at inital orbit of body1
            body1_escape_deltav = abs(v_esc_orbit_r1 - v_orbit_r1) # delta-v to escape body1
            # spacecraft velocity now equal to body1's velocity around central body
            
            v_body1 = sqrt(body1.orbital_center_mu / body1.semimajoraxis) # velocity of body1 around central body
            v_body2 = sqrt(body2.orbital_center_mu / body2.semimajoraxis) # velocity of body2 around central body
            transfer_deltav = abs(v_body2 - v_body1) # delta-v of transfer ellipse from body1 to body2 
            # spacecraft velocity now equal to body2's velocity around central body
            
            v_esc_orbit_r2 = sqrt(2 * body2.mu / orbit_r2) # escape velocity at final orbit of body2
            v_orbit_r2 = sqrt(body2.mu / orbit_r2) # velocity of final orbit around body2
            body2_capture_deltav = abs(v_orbit_r2 - v_esc_orbit_r2) # delta-v capture from transfer to final orbit
            
            total_deltav = body1_escape_deltav + transfer_deltav + body2_capture_deltav # total delta-v
            
            a_transfer = (body1.semimajoraxis + body2.semimajoraxis) / 2
            transfer_time = pi * sqrt(a_transfer**3 / body1.orbital_center_mu) # s
            transfer_time_conversions = [
                transfer_time, # s
                transfer_time/60, # min
                transfer_time/3600, # hrs
                transfer_time/86400, # days
            ]
            
            return total_deltav, transfer_time_conversions
        
    def next_transfer_window(self, body1_index, body2_index):
        body1 = self.space_bodies[body1_index]
        body2 = self.space_bodies[body2_index]
        
        # t = current date
        t = Sun().ts.now()
        eph = Sun().ephemeris
        initial_body = eph[body1.skyfield_name]
        final_body = eph[body2.skyfield_name]
        sun = eph["Sun"]
        
        # required angle
        alpha_req = pi * (1 - sqrt((body1.semimajoraxis/body2.semimajoraxis + 1)**3) / (sqrt(8))) # radians
        
        # current angle
        body1_pos = initial_body.at(t)
        sun_pos = body1_pos.observe(sun)
        body2_pos = body1_pos.observe(final_body)
        current_alpha = sun_pos.separation_from(body2_pos).radians
        
        i = 1
        
        # solver for next date
        while current_alpha/alpha_req < 0.99 or current_alpha/alpha_req > 1.01: # more than 1% error in alpha
            next_date = t + datetime.timedelta(days=i)

            body1_pos = initial_body.at(next_date)
            sun_pos = body1_pos.observe(sun)
            body2_pos = body1_pos.observe(final_body)
            current_alpha = sun_pos.separation_from(body2_pos).radians
            
            i+=1
        
        return next_date