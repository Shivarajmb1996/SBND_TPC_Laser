#!/usr/bin/env python

import sys, time, glob
import serial
from characters import *

sgn = lambda x : (x>0) - (x<0)

MAXVELOCITY = 1000             # maximum velocity in microsteps/s
MICROSTEPS = 256                # one full evolution of the motor has:
                                #   - steps: 200 
                                #   - microsteps: 200*MS (200*256=51200)        
ONETURN = 200*MICROSTEPS        # steps of on full turn

########################### Feed-trough control ################################
def initAxis1():
        print "----------- Axis 1 (Rotary) Initialization -----------"
        # first signal on the connection        
        serFeedtrough.write("\n")       

        # set microstep resolution to maximum 
        serFeedtrough.write("\n1MS"+str(256)+"\n")
        
        # set acceleration and deceleration to 100000 microsteps/s
        serFeedtrough.write("\n1A=1000\n")
        serFeedtrough.write("\n1D=1000\n")
        
        # set start speed and end speed of the movement
        serFeedtrough.write("\n1VI=500\n")
        serFeedtrough.write("\n1VM=3000\n")

        # set holding and run current in percent
        serFeedtrough.write("\n1HC=5\n")
        serFeedtrough.write("\n1RC=80\n")

        
        reply = getInfo(2)
        ##maxVelocity = float(readValue(reply,"VM"))
        
        ##initialVelocity = float(readValue(reply,"VI"))
        ##acceleration =  float(readValue(reply,"A"))
        ##tstart = (maxVelocity-initialVelocity)/acceleration

def initAxis2():
        print '----------- Axis 2 (Linear) Initialization -----------'  
        # first signal on the connection        
        serFeedtrough.write("\n")       

        # set motor settling time in ms 
        #serFeedtrough.write("\n2MT=2000\n")

        # set microstep resolution to maximum 
        serFeedtrough.write("\n2MS"+str(MICROSTEPS)+"\n")
        
        # set acceleration and deceleration to 100000 microsteps/s
        serFeedtrough.write("\n2A=5000\n")
        serFeedtrough.write("\n2D=5000\n")
        
        # set start speed and end speed of the movement
        serFeedtrough.write("\n2VI=5")
        serFeedtrough.write("\n2VM="+str(MAXVELOCITY)+"\n")

        # set holding and run current in percent
        serFeedtrough.write("\n2HC=10\n")
        serFeedtrough.write("\n2RC=80\n")

        
        reply = getInfo(2)
        ##maxVelocity = float(readValue(reply,"VM"))
        
        ##initialVelocity = float(readValue(reply,"VI"))
        ##acceleration =  float(readValue(reply,"A"))
        ##tstart = (maxVelocity-initialVelocity)/acceleration
        
def readValue(feed, inst):
        # read the value of the given string from the feed obtained by getInfo
        n = len(inst) + 3
        start = feed.find(inst + " = ")
        end = feed.find('\n',start)
        
        ##if inst in feed[start:end]:     
        ##        print inst + " = " + feed[start+n:end]
        ##        return float(feed[start+n:end])
        ##else: sys.exit('Error while reading setup')

def getInfo(AxisNr):
        # obtain all the control parameters from the motor
        serFeedtrough.write("\n\n"+ str(AxisNr) + "PR AL\n")
        reply = serFeedtrough.read(850)
        print reply
        return reply

def moveVertical(inst):
        if sgn(inst) == 1: print 'Axis2: going up ' + str(inst) + ' microsteps'
        else: print 'Axis2: going down ' + str(-inst) + ' microsteps'
        
        serFeedtrough.write('\n2MR ' + str(inst) + '\n')
        
        ##while AxisMoving(2):
        ##        print 'Axis2 Position: ' + getPosition(2)

def moveHorizontal(inst):
        if sgn(inst) == 1: print 'Axis1: going left ' + str(inst) + ' microsteps'
        else: print 'Axis1: going right ' + str(-inst) + ' microsteps'
        
        serFeedtrough.write('\n1MR ' + str(inst) + '\n')
        
        ##while AxisMoving(1):
        ##        print 'Axis1 Position: ' + getPosition(1)


def getPosition(AxisNr):
        serFeedtrough.write("\n"+ str(AxisNr) + "PR P\n")
        reply = serFeedtrough.read(25)
        return reply

def AxisMoving(AxisNr):
        # returns: 1 if axis is moving, 0 if not. And -1 for non-identifiable answer
        serFeedtrough.write("\n"+ str(AxisNr) + "PR MV\n")
        reply = serFeedtrough.readline()        
        if ('0' in reply): return 0
        elif('1' in reply): return 1    
        else: return -1 

########################### Laser control ################################      
def initLaser():
        print '---------------- Laser Initialization ----------------'  
        
        timeout=0.1
        print "Get Laser status:"
        serLaser.write("SE\r")
        reply = serLaser.read(20)
        print " My Status is: ", reply

        time.sleep(timeout)  

        print "Get Laser shots:"
        serLaser.write("SC\r")
        reply = serLaser.read(9)
        print " I have been shooting: ", reply

        time.sleep(timeout)  

        print "Turn Laser on:"
        #serLaser.write("ST 1\r")
        reply = serLaser.read(20)
        print " Laser is on: ", reply

        time.sleep(2) 

        print "Set single shot mode"
        serLaser.write("PD 000\r")
        reply = serLaser.read(20)
        print " current mode ", reply
        print '------------------------------------------------------'  
def startLaser():
        print "Start Laser:"
        serLaser.write("ST 1\r")
        reply = serLaser.read(20)
        print "Laser on:", reply

def singleModeLaser():
        print "Enter Single Mode:"
        serLaser.write("PD 000\r")
        reply = serLaser.read(20)
        print "Laser in single mode:", reply
        
def openShutter():
        print "Open shutter:"
        serLaser.write("SH 1\r")
        reply = serLaser.read(20)
        print "Shutter is:", reply
        time.sleep(5)
        
def closeShutter():
        print "Close shutter:"
        serLaser.write("SH 0\r")
        reply = serLaser.read(20)
        print "Shutter is:", reply

def SHOOT():
        time.sleep(0.5)
        print "SHOOT"
        serLaser.write("SS\r")
        reply = serLaser.read(20)
        print "answer:", reply

def SHOOT10Hz():
        serLaser.write("PD 001\r")
        reply = serLaser.readline()
        print "answer:", reply
        
        time.sleep(1)
        print "Stop SHOOT at 10Hz"
        serLaser.write("PD 000\r")
        reply = serLaser.readline()
        print "answer:", reply        
        

def SHOOT():
        time.sleep(0.5)
        print "SHOOT"
        serLaser.write("SS\r")
        reply = serLaser.read(20)
        print "answer:", reply


def makeChar(character):
        charNR = ord(character)-65
        h = 1 # scale factor horizontal
        v = 1 # scale factor vertical
        microstepsUp = v*100
        microstepsRight = h*350
        bigStep = 3000
        for k in range (7):  #7
                moveVertical(-bigStep)
                time.sleep(10)
                moveVertical(-microstepsUp)
                time.sleep(4)
                for i in range (8):  #8
                        if characters[charNR][k][i]: SHOOT10Hz()
                        #SHOOT10Hz()
                        moveVertical(-microstepsUp)
                        time.sleep(6)
                        
                moveHorizontal(-2000)        
                moveVertical(9*microstepsUp+bigStep)  #9
                time.sleep(4.5)
                moveHorizontal(1900)
                time.sleep(4.5)

# open serial ports

try:
 serFeedtrough = serial.Serial(12, 9600, 8, 'N', 1, timeout=0.2)
 serLaser = serial.Serial(4, 9600, 8, 'N', 1, timeout=0.5) 
  
except:
   print "Error opening com port. Quitting."
   sys.exit(0)

print "Opening " + serFeedtrough.portstr 
print serFeedtrough.isOpen()
print serFeedtrough.portstr

########################### Init laser ##########################
print "RR at 10Hz"
serLaser.write("RR 10\r")
reply = serLaser.readline()


########################### Init laser ##########################

microstepsUp = -2500
wait = 4.5
initAxis1()
initAxis2()

##for i in range(7):
##        moveHorizontal(-2000)
##        time.sleep(wait)
##        moveHorizontal(1900)
##        time.sleep(wait)


startLaser()
#singleModeLaser()
openShutter()
makeChar("L")
makeChar("H")
makeChar("E")
makeChar("P")


closeShutter()
