import random
import time
import datetime
from temp_hum_score import temp_hum_score


class Library():

    def __init__(self, name, places, max_places = 100, opening = 9, closing = 20):
        #temp, hum, entrance, s0, s1, s2, s3, progr
        self.name = name
        self.output = [0,0,0,0,0,0,0,5]
        self.max_places = max_places
        self.places = places
        self.opening = opening
        self.closing = closing

        

    def __str__(self):
        print(self.name + " (Max places: " + str(self.places),", Open: "  + str(self.opening) + ":00, ", "Closes : " + str(self.closing)+ ":00)")

    def entrance(self, h, m):
        mu = 0
        entrance = 0
        if  h> self.opening and h < 11:
            mu = 0.6
        elif h > 11 and h < 14:
            mu = 1.4
        elif h > 14 and h < 16:
            mu = 0.8
        elif h > 18:
            mu = 1.6

        r = round(random.gauss(mu, 0.3),2)

        if r > 0.3:
                entrance = 1
                self.places = self.places - 1
        elif -r > 0.3:
                entrance = -1
                self.places = self.places + 1
                    
        return entrance 

    def noise(self, h, m):
        
        perc = self.places/self.max_places

        n0 = 0
        n1 = 0
        n2 = 0
        n3 = 0
        sigma = random.uniform(0.25, 0.35)

        for i in range(1000):
            r = random.gauss(perc - 1, sigma)

            if r < -0.4:
                n0 = n0 + 1
            elif r > -0.4 and r < 0.4:
                n1 = n1 + 1
            elif r > 0.41 and r < 0.75:
                n2 = n2 + 1
            elif r > 0.85:
                n3 = n3 + 1
            
        return n0, n1, n2, n3

    def temp_hum(self, h, m):
        hum = 42
        temp = 54

        return temp, hum
        
    def generate_value(self, h, m):

        n0, n1, n2, n3 = self.noise(h,m)
        temp, hum = self.temp_hum(h,m)

        self.output[0] = temp
        self.output[1] = hum
        self.output[2] = self.entrance(h,m)
        self.output[3] = n0
        self.output[4] = n1
        self.output[5] = n2
        self.output[6] = n3
        self.output[7] = self.output[7] + 1

        print(self.name, self.output, "Posti disponibili: ", self.max_places-self.places)
        #Agginugi data orario, mattinapome + giorno settimana
    
    
    


## TESTING FUNCTIONS
'''
l = Library("Dief", 0, 100)
ae = Library("Giuri", 50, 100)
g = Library("100%", 100, 100)


print(l.name, l.noise())
print(ae.name, ae.noise())
print(g.name, g.noise())'''