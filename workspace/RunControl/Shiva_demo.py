# author : Shivaraj M B, LHEP - Univ. Bern

from devices.feedtrough import *
from devices.laser import *
from devices.attenuator import *
#from devices.aperture import *
#from devices.mirror import *

import time
import re

#att = Attenuator()
#att.color = False

#RM = Feedtrough("rotary_actuator")
#LM = Feedtrough("linear_actuator")

laser = Laser(0)
laser.color = False
laser.comTimeout = 0.5
print(" ___________ All the best__________ ")
def InitialiseAll():
	laser.com_init()
	#att.com_init()
	#LM.com_init()
	#RM.com_init()
	""" Message colour"""
	#LM.color = True
	#RM.color = True
	""" Motors  """
	#RM.initAxis()
	#LM.initAxis()

def LaserWarming():
	laser.getStatus()
	print("Starting the Laser within 5 second")
	time.sleep(5)
	laser.start()
	print("Wait for 15 minute")
	#time.sleep(900)
	print("Now you are good to go....")
	

##________________ Shiva tried something___________________________

LHEP = [[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[1,2],[1,3],[1,4],[1,5],[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],[10,8],[5,9],[5,10],[5,11],[1,12],[2,12],[3,12],[4,12],[5,12],[6,12],[7,12],[8,12],[9,12],[10,12],[1,15],[2,15],[3,15],[4,15],[5,15],[6,15],[7,15],[8,15],[9,15],[10,15],[1,16],[1,17],[1,18],[1,19],[10,19],[10,18],[10,17],[10,16],[5,16],[5,17],[1,21],[2,21],[3,21],[4,21],[5,21],[6,21],[7,21],[8,21],[9,21],[10,21],[10,22],[10,23], [10,24], [10,25],[9,26],[9,27],[8,27],[7,27],[5,26],[5,25],[5,24],[5,23],[5,22],[5,21]]

HELP = [[1,8],[2,8],[3,8],[4,8],[5,8],[6,8],[7,8],[8,8],[9,8],[10,8],[5,9],[5,10],[5,11],[1,12],[2,12],[3,12],[4,12],[5,12],[6,12],[7,12],[8,12],[9,12],[10,12],[1,15],[2,15],[3,15],[4,15],[5,15],[6,15],[7,15],[8,15],[9,15],[10,15],[1,16],[1,17],[1,18],[1,19],[10,19],[10,18],[10,17],[10,16],[5,16],[5,17],[1,1],[2,1],[3,1],[4,1],[5,1],[6,1],[7,1],[8,1],[9,1],[10,1],[1,2],[1,3],[1,4],[1,5],[1,21],[2,21],[3,21],[4,21],[5,21],[6,21],[7,21],[8,21],[9,21],[10,21],[10,22],[10,23], [10,24], [10,25],[9,26],[9,27],[8,27],[7,27],[5,26],[5,25],[5,24],[5,23],[5,22],[5,21], [0,30],[0,31],[0,32],[1,32],[1,31],[1,30],[2,30],[2,31],[4,31],[5,31],[6,31],[7,31],[8,31],[9,31],[10,31] ]

Test = [[1,1],[1,10],[2,3],[3,12],[15,13],[2,5]]
LMEncoder = []
RMEncoder = []
LM_reading = []
RM_reading = []
LMfact = int(-45)
RMfact = int(-280)
def LaserPrint(List):
    for i in List:
        LM.moveAbsolute(i[0]*LMfact)
        RM.moveAbsolute(i[1]*RMfact)
        ELM = i[0]*LMfact
        ERM = i[1]*RMfact
        n = 0
        #LM.isMoving()
        #RM.isMoving()
        while n < 100:
            if LM.isMoving() == 0 and RM.isMoving() == 0:
                L = LM.getPosition
                R = RM.getPosition
                LMEncoder.append(float(L))
                RMEncoder.append(float(R))
                LM_reading.append(float(ELM))
                RM_reading.append(float(ERM))
                time.sleep(0.5)
                laser.singleShot()
                laser.singleShot()
                time.sleep(1)
                break
            else:
                time.sleep(1)
                n = n+1
def write(RMEnco, LMEnco):
    with open("example.csv", "a") as f:
        f.write(str(RMEnco)+ "  " + str(LMEnco) + "\n")


def LaserScanPattern(RMStep, RMLim, LMStep, LMLim):
    RM.toHome()
    #write this position to file
    LM.toHome()
    #write this position to file
    write(RM.getPosition(), LM.getPosition())
    write(RMStep, LMStep)
    write(RMLim, LMLim)
    j = 0
    while j< LMLim:
           
        i = 0
        while i< RMLim:
            #Laser.singleShot()  #!
            write(RM.getPosition(), LM.getPosition())
            #write "i" to another file
            RM.moveRelative(i+RMStep)
            i = i + RMStep        # or i+=20
        j = j+ LMStep
    
    
    
 
    
def TriggerDemo(self, LMSteps, Trigg):
    LM.moveRelative(LMSteps)
    while LM.isMoving():
        start_time = time.time()
        trigger = int(LM.getTriggerOutput())
        if trigger == Trigg:
            self.printMsg(bcolors.OKGREEN + "matching________start______"  + bcolors.ENDC)
            print("/////////////////////////////____", trigger,"__///////////////////////__")
            print("/////////////////////////////____", LM.getPosition(),"__///////////////////////__")
            self.printMsg(bcolors.OKGREEN + "matching________end_______"  + bcolors.ENDC)
            self.printMsg(bcolors.OKGREEN + "--- %s seconds ---" % (time.time() - start_time) + bcolors.ENDC)
            continue
        else:
            self.printError("______ not a trigger ___________")
            
    
    
    
    
    
              
	

