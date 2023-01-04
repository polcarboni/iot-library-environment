import random
import time
import datetime
import score_functions
from Hardware.room_gen import Room


class Library():

    def __init__(self, name, floornames, avg_temp, avg_hum, max_places = 100, opening = 9, open_min = 0, closing = 20, closing_min = 0):
        #temp, hum, entrance, s0, s1, s2, s3, temphumscore, noisescore, progr
        self.name = name
        self.floornames = floornames
        self.output = [0,0,0,0,0,0,0,0,0,0]
        self.max_places = max_places
        self.occ_places = 0

        self.opening = opening
        self.closing = closing
        self.open_min = open_min
        self.closing_min = closing_min

        self.avg_temp = avg_temp
        self.avg_hum = avg_hum

        self.floors = {}

        self.mu_test = 0

        for i in range(len(self.floornames)):
            self.floors[self.floornames[i]]= Room(self.floornames[i], self.occ_places, self.max_places, self.avg_temp, self.avg_hum)
            

    def __str__(self):
        print(self.name + " (Max places: " + str(self.max_places),", Open: "  + str(self.opening) + ":00, ", "Closes : " + str(self.closing)+ ":00)")


    def entrance(self, h, m):

        entrance = 0
        mu=0
        hourbased = 0

        if  h >= 8 and m >= 0:
            mu = 0.4
        if h >= 9 and m >= 0:
            mu = 0.5
        if h >= 11 and m >= 30:
            mu = -0.75
        if h >= 13 and m >= 30:
            mu = 0.3
        if h >= 15 and m >= 0:
            mu = 0.4
        if h >= 17 and m >= 0:
            mu = -0.2
        if h >= 19 and m >=0:
            mu = -0.6

        if  h >= self.opening and m >= self.open_min:
            hourbased = 0.15
        if h >= self.opening and m >= self.open_min + 30:
            hourbased = 0.05
        if h >= self.opening + 2 and m >= self.open_min:
            hourbased = 0 
        if h >= self.closing - 2 and m >= self.closing_min:
            hourbased = -0.05
        if h >= self.closing -1 and m >= self.closing_min:
            mu = -1

        mu = mu + hourbased

        r = round(random.gauss(mu, 0.3),2)


        if self.occ_places <= self.max_places and self.occ_places >= 0:
            if r > 0.8:
                entrance = 1
            elif -r > 0.8:
                entrance = -1
        
        if self.occ_places == self.max_places and entrance == 1:
                entrance = 0
                
        elif self.occ_places == 0 and entrance == -1:
                entrance = 0
        
        self.occ_places = self.occ_places + entrance

        self.mu_test = mu
        return entrance 
    
    def generate_values(self, h, m):
        h = int(str(h))
        m = int(str(m))
        
        flooroutput = [0,0,0,0,0,0,0,0,0,0]
        if h >= self.opening and h < self.closing:

            print(self.name, ": ", self.max_places - self.occ_places, "  ", self.mu_test)

            for i in self.floornames:

                temp, hum = self.floors[i].temp_hum(self.floors[i].temp, self.floors[i].hum, h, m)
                self.floors[i].occ_places = self.occ_places
                n0, n1, n2, n3 = self.floors[i].noise(h,m)

                flooroutput[0]= temp
                flooroutput[1]= hum

                if self.floors[i].name == 'ingresso':
                    flooroutput[2] = self.entrance(h,m)
                else:
                    flooroutput[2] = 0

                flooroutput[3]= n0
                flooroutput[4]= n1
                flooroutput[5]= n2
                flooroutput[6]= n3

                flooroutput[7]= score_functions.temp_hum_score(flooroutput[0],flooroutput[1])
                flooroutput[8]= score_functions.noise_score(flooroutput[3], flooroutput[4], flooroutput[5], flooroutput[6])

                flooroutput[9]= self.output[9]  

                print(self.name[0:3], self.floors[i].name[0:4], flooroutput)
                #print(flooroutput[2])

            self.output[9] = self.output[9] + 1                 
            #print('\n')

        elif h >= self.closing and m >=self.closing_min:
            self.occ_places = 0
            self.output[9] = 0

            
                
                

                

                

                    

                    




                    
                    
                
                

            
    


## TESTING FUNCTIONS
'''
l = Library("Dief", 0, 100)
ae = Library("Giuri", 50, 100)
g = Library("100%", 100, 100)


print(l.name, l.noise())
print(ae.name, ae.noise())
print(g.name, g.noise())'''