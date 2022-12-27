import random
import time
import datetime
from temp_hum_score import temp_hum_score
from room_generator import Room


class Library():

    def __init__(self, name, floornames, avg_temp, avg_hum, max_places = 100, opening = 9, closing = 20):
        #temp, hum, entrance, s0, s1, s2, s3, progr
        self.name = name
        self.floornames = floornames
        self.output = [0,0,0,0,0,0,0,0]
        self.max_places = max_places
        self.occ_places = 0
        self.opening = opening
        self.closing = closing
        self.avg_temp = avg_temp
        self.avg_hum = avg_hum

        self.floors = {}

        for i in range(len(self.floornames)):
            self.floors[self.floornames[i]]= Room(self.floornames[i], self.occ_places, self.max_places, self.avg_temp, self.avg_hum)
            

    def __str__(self):
        print(self.name + " (Max places: " + str(self.max_places),", Open: "  + str(self.opening) + ":00, ", "Closes : " + str(self.closing)+ ":00)")

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


        if self.occ_places < self.max_places and self.occ_places > 0:

            if r > 0.3:
                entrance = 1
            elif -r > 0.3:
                entrance = -1
        
        elif self.occ_places == self.max_places:
            if abs(r) > 0.35:
                entrance = -1
                
        elif self.occ_places == 0:
            if abs(r) > 0.35:
                entrance = 1
                
        self.occ_places = self.occ_places + entrance
                    
        return entrance 
    
    def generate_values(self, h, m):
        
        flooroutput = [0,0,0,0,0,0,0,0]
        if h > self.opening and h < self.closing:

            print(self.name, "Posti disponibili: ", self.max_places - self.occ_places)

            for i in self.floornames:

                temp, hum = self.floors[i].temp_hum(self.floors[i].temp, self.floors[i].hum, h, m)
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
                flooroutput[7]= self.output[7]  

                print(self.name[0:3], self.floors[i].name[0:4], flooroutput)

            self.output[7] = self.output[7] + 1                 
            print('\n')

        elif h >= self.closing:
            self.places = 0

            
                
                

                

                

                    

                    




                    
                    
                
                

            
    


## TESTING FUNCTIONS
'''
l = Library("Dief", 0, 100)
ae = Library("Giuri", 50, 100)
g = Library("100%", 100, 100)


print(l.name, l.noise())
print(ae.name, ae.noise())
print(g.name, g.noise())'''