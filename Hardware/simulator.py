import random
import time

def entrance_generator(self):
    a = round(random.gauss(0, 0.3),2)
    return a

class Simulator():

    def __init__(self, places, max_places = 100):
        #temp, hum, entrance, s0, s1, s2, s3, progr
        self.output = [0,0,0,0,0,0,0,0]
        self.max_places = max_places
        self.places = 0

    def __str__(self):
        print(self.output, self.places)

    
    def entrances(self):
        # Simulation of library entrances and exits
        a = entrance_generator()

        if a > 0.3:
            entrance = 1
        if -a > 0.3:
            entrance = -1
                 
        
        
        return entrance
        
    def generate_value(self):
        self.output[7] = self.output[7] + 1
        self.output[2] = self.entrances()
    
    

    
