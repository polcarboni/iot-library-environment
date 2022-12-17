import random
import time

tm = time.localtime()

class Library():

    def __init__(self, name, max_places = 100, opening = 9, closing = 20):
        #temp, hum, entrance, s0, s1, s2, s3, progr
        self.name = name
        self.output = [0,0,0,0,0,0,0,0]
        self.max_places = max_places
        self.places = max_places
        self.opening = opening
        self.closing = closing

    def __str__(self):
        print(self.name + " (Max places: " + str(self.places),", Open: "  + str(self.opening) + ":00, ", "Closes : " + str(self.closing)+ ":00)")

    def entrance(self):
        h = tm.tm_hour
        m = tm.tm_min

        if  h> 9 and h < 11:
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
        elif -r > 0.3:
                entrance = -1
                    
        return entrance 

    def noise():
        n0 = 0
        n1 = 0
        n2 = 0
        n3 = 0


        return n0, n1, n2, n3

    def humtemp():
        hum = 0
        temp = 0

        return hum, temp
        
    def generate_value(self):
        self.output[7] = self.output[7] + 1
        self.output[2] = self.entrance()
    

l = Library("DIEF")
print(l.__str__())