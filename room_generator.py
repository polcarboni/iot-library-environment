import random

places = 1
max_places = 1
avg_temp = 1
avg_hum = 1
h = 1
m = 1

class Room():

    def __init__(self, name, places, max_places, temp, hum):

        self.name = name
        self.output= [0,0,0,0,0,0,0,0]
        self.occ_places = places
        self.max_places = max_places
        self.temp = temp
        self.hum = hum
        self.noise_variance = random.uniform(0.25, 0.35)

    def __str__(self):
        print("Nome stanza: ", self.name)

    
    def noise(self, h, m):
        
        perc = self.occ_places/self.max_places

        n0 = 0
        n1 = 0
        n2 = 0
        n3 = 0

        for i in range(1000):
            r = random.gauss(perc - 1, self.noise_variance)

            if r < -0.4:
                n0 = n0 + 1
            elif r > -0.4 and r < 0.4:
                n1 = n1 + 1
            elif r > 0.41 and r < 0.75:
                n2 = n2 + 1
            elif r > 0.85:
                n3 = n3 + 1
            
        return n0, n1, n2, n3

    def temp_hum(self, temp, hum, h, m):

        t = random.gauss(0,0.3)
        h = random.uniform(0,100)

        if t > 0.8:
            self.temp = round(self.temp + 0.1, 1)

        if t < -0.8:
            self.temp = round(self.temp - 0.1, 1)

        if h>80:
            self.hum = round(self.hum + random.uniform(-0.5, 0.5),1)

        return temp, hum