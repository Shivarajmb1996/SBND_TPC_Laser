__author__ = 'matthias'

from math import copysign
from base.motor import *

import re

class Feedtrough(Motor):
    def __init__(self, name, RunNumber=0, axis=0):
        self.name = name
        super(Feedtrough, self).__init__(name=self.name, RunNumber=RunNumber)
        self.state = 0
        self.comport = "/dev/ttyUSB0"
        self.comBaudrate = 9600
        self.InfoInstruction = None
        self.InfoMsgLength = 800
        self.StandartMsgLength = 10
        self.comEnd = "\n"

        self.comEcho = False

        # TODO: Implement this class into new Motor class
        self.InstructionSet = {"getInfo": "PR ALL"}
        self.comInfoReplyLength = 800

        self.axis = axis

        self.config_load()
        self.MICROSTEPS = None
        self.ACCELERATION = None
        self.DECELLERATION = None
        self.INITIALVELOCITY = None
        self.ENDVELOCITY = None
        self.HOLDCURRENT = None
        self.RUNCURRENT = None
        self.HOMINGVELOCITY = None
        self.MAX_HOMING_OVERSHOOT = None
        ######################
        self.ENCODER = None

        self.init()

    def init(self):
        self.axis = self.config.AXIS
        self.MICROSTEPS = self.config.MICROSTEPS
        self.ACCELERATION = self.config.ACCELERATION
        self.DECELLERATION = self.config.DECELLERATION
        self.INITIALVELOCITY = self.config.INITIALVELOCITY
        self.ENDVELOCITY = self.config.ENDVELOCITY
        self.HOLDCURRENT = self.config.HOLDCURRENT
        self.RUNCURRENT = self.config.RUNCURRENT
        self.HOMINGVELOCITY = self.config.HOMINGVELOCITY
        self.MAX_HOMING_OVERSHOOT = self.config.MAX_HOMING_OVERSHOOT
        self.HOME_SWITCH = self.config.HOME_SWITCH
        self.HOME_DIRECTION = self.config.HOME_DIRECTION
        self.IDLE_POSITION = self.config.IDLE_POSITION
        #########################
        #self.CLOCKRATIO = self.config.CLOCKRATIO
        #self.CLOCKWIDTH = self.config.CLOCKWIDTH
        self.ENCODER = self.config.ENCODER
        self.STALLFACTOR = self.config.STALLFACTOR
        self.STALLMODE = self.config.STALLMODE
        #self.DEADBAND = self.config.DEADBAND
        #self.ENCODERLINE = self.config.ENCODERLINE
        #aelf.POSITIONMAINTENANCE = self.config.POSITIONMAINTENANCE
        #self.COUNTER1 = self.config.COUNTER1
        #self.COUNTER2 = self.config.COUNTER2
        self.USER1 = self.config.USER1
        self.HOMING_MOVEMENT_DIRECTION = self.config.HOMING_MOVEMENT_DIRECTION
        

        self.comPrefix = str(self.axis)  # this string is put in front of any message transmitted


    def com_write_(self, msg):
        """ write message to, overwriting the base.com_write function adding the axis preamble """
        try:
            self.com.isOpen()
            self.printDebug(str(self.axis) + msg + self.comEnd)
            print("_____feedthrough.py_______ 67", msg)
            self.com.write(str(self.axis) + msg + self.comEnd)

        except:
            self.printError("Could not write message \"" + str(msg) + "\" to com port (" + str(self.com.portstr) + ")")

    def initAxis(self):
        self.printMsg("---------------- init axis -----------------")
        self.setParameter("MS", self.MICROSTEPS)
        self.setParameter("A", self.ACCELERATION)
        self.setParameter("D", self.DECELLERATION)
        self.setParameter("VI", self.INITIALVELOCITY)
        self.setParameter("VM", self.ENDVELOCITY)

        self.setParameter("HC", self.HOLDCURRENT)
        self.setParameter("RC", self.RUNCURRENT)
        #########################
        self.setParameter("EE", self.ENCODER)

        # disable unused switches
        #self.setParameter("S3", "0,0,0")
        self.setParameter("S4", "0,0,0")
        self.setLimitSwitches(0)
        
        
        if (self.axis == 1):
            self.setTriggerInput(0)
            
            #self.TRIGGER = self.config.TRIGGER
            #self.INPUT13 = self.config.INPUT13
            #self.FILTERCAPTURE = self.FILTERCAPTURE
            
            #self.setParameter("FC", self.FILTERCAPTURE)
            #self.setParameter("TE", self.TRIGGER)
            


    def setParameter(self, parameter, value):
        msg = str(parameter) + "=" + str(value)
        self.com_write(msg)
        SetValue = self.getParameter(parameter)

        string = "Set " + parameter + "=" + str(value)
        ############################################
        print("______feedthrough 126___",str(SetValue),"____", str(value))
        #start = (str(SetValue).find("="))+1
        #end = len(str(value))
        #print(start, end, SetValue[start: start+end])
        #required = SetValue[start: start+end]
        
        
        ############################################
        #after changing the getParameter
        SetValue = SetValue.replace(" ", "")
        Need = SetValue.replace('\r', '')
        Final = Need.replace('\n', '')
        print("______feedthrough 137____", Final)
        
        #########################################
        #if SetValue.replace(" ", "") == str(value):
        #if (str(SetValue).find(str(value))) != 0 :  $$$ this is more appropriate$$$
        #if required == str(value):
        if Final == str(value):
            if self.color is True:
                self.printMsg(string + bcolors.OKGREEN + " -> OK" + bcolors.ENDC)
            else:
                self.printMsg(string + " -> OK")
            return 0
        else:
            self.printError(string + " failed")
            return -1

    def getParameter(self, parameter):
       # msg = "PR " + parameter                                # original
       # print("_________feedthrough.py 121_________ ", msg)
        #self.com_write(msg)                                    # original
       # reply = self.com_recv()                                # original
        #return reply[:-2]                                      # original
               
    # cant you put flush here?? because getVariable will be incomplete if we do it.
        msg = "PR " + parameter
        self.com_write(msg)
        if parameter == str('AL'):
            print(parameter == str('AL'))
            reply = self.com_recv(msg_length=1000000000)
            #print("__________ output is changed here to float point. feedthrough 164___________")
            return reply[:-2]
        else:
            reply = self.com_recv(msg_length=100)
            ###########################
            print("_______feedthrough 157",reply)
            reply = reply.decode()
            print("_______feedthrough___ 159", reply)
            
            PR_point = reply.find("PR")
            new_reply = reply[PR_point+2 +len(parameter)+1: -3]
            print("_______feedthrough __163", new_reply)
            
            return new_reply
            
            #m = reply.find('\n')
            #print("_____ feedthrough___", m)

    def sendCommand(self, command, attribute=""):
        msg = (command + " " + str(attribute))
        print("_____feedthrough 190__", msg.encode())
        self.com_write(msg)

    def stopMovement(self):
        self.sendCommand("\x1B")
        move = self.getParameter("MV")
        self.printMsg("Stopping MV=" + str(move))

    def isMoving(self):
        # returns: 1 if axis is moving, 0 if not. And -1 for non-identifiable answer
        reply = self.getParameter("MV")
        print ("________feedthrough___183_ isMoving MV =", reply)
        if ('0' in reply):
            return 0
        elif ('1' in reply):
            return 1
        else:
            return -1

    def getPosition(self):
        reply = self.getParameter("P")
        print("___feedthrough.py 193__", reply)
        return int(reply)

    def moveRelative(self, microsteps, monitor=False):
        self.printMsg("Moving " + str(microsteps) + " microsteps") 
        self.sendCommand("MR", microsteps)
        print("_______feedthrough 199_ moveRelative_end")
        if monitor:
            self.monitorMovement()

    def moveAbsolute(self, microsteps, monitor=False):
        self.printMsg("Moving to position: " + str(microsteps))
        self.sendCommand("MA", microsteps)
        if monitor:
            self.monitorMovement()

    def setLimitSwitches(self, attempts):
        if attempts == 4:
            self.printError("Setting the limit switch failed 5 times -> exiting")
            sys.exit(-1)
        if self.axis == 1:
            self.printMsg("Set S1 and S2 as limit switches for Linear Motor")
            set = self.setParameter("S1", "2,1,0")  # set counterclockwise endswitch as home switch
            set += self.setParameter("S2", "3,1,0")  # set counterclockwise endswitch as home switch
        elif self.axis== 2:
            self.printMsg("Set S1 and S2 as limit switches")
            set = self.setParameter("S1", "2,0,0")  # set counterclockwise endswitch as home switch
            set += self.setParameter("S2", "3,0,0")  # set counterclockwise endswitch as home switch
        time.sleep(0.5)
        # check if S2 was set correctly
        if set != 0:
            self.printMsg("limit switches were not set correctly")
            self.setLimitSwitches(attempts + 1)
            self.stopMovement()

    def setHomeSwitch(self, attempts):
        if attempts == 4:
            self.stopMovement()
            self.printError("Setting the home switch failed 5 times -> exiting")
            sys.exit(-1)

        self.printMsg("Set " + self.HOME_SWITCH + " as home switch")
        set = self.setParameter(self.HOME_SWITCH.encode(), "1,0,0")  # set counterclockwise endswitch as home switch
        time.sleep(0.5)
        # check if S1 was set correctly
        if set != 0:
            self.printMsg("home switch was not set correctly")
            self.setHomeSwitch(attempts + 1)

    def homeAxis(self):
        # check if manual homing was performed
        counts = int(self.getParameter("R1"))
        if counts < 1:
            self.printMsg("Manual homing was not performed, aporting homing procedure")
            return -1

        self.setParameter("VM", self.HOMINGVELOCITY)
        self.setHomeSwitch(0)
        self.printMsg("Homing")
        self.sendCommand("HM", self.HOME_DIRECTION)

        # monitor the movement and abort in the movement goes out too far from the known zero position
        self.printMsg("Position:")
        out_of_bounds = False
        change_dir = False
        pos_old = self.getPosition()
        if self.HOME_DIRECTION == 1:
            homing_dir = -1
            dir_old = -1  # we home in the negative direction
        elif self.HOME_DIRECTION == 3:
            homing_dir = 1
            dir_old = 1
        while self.isMoving():
            time.sleep(0.2)
            pos_now = self.getPosition()

            dir_now = copysign(1, pos_now - pos_old)

            if dir_now != dir_old:
                change_dir = True
            if self.HOME_DIRECTION == 1:
                if pos_now < self.MAX_HOMING_OVERSHOOT * homing_dir:
                    out_of_bounds = True
                if pos_now > abs(self.MAX_HOMING_OVERSHOOT) and change_dir is True:
                    out_of_bounds = True

            if self.HOME_DIRECTION == 3:
                if pos_now > self.MAX_HOMING_OVERSHOOT * homing_dir:
                    out_of_bounds = True
                if abs(pos_now) > abs(self.MAX_HOMING_OVERSHOOT) and change_dir is True:
                    out_of_bounds = True

            if out_of_bounds is True:
                self.stopMovement()
                self.setParameter("R1", 0)
                self.setLimitSwitches(0)
                self.printError(" Position went to far over home switch, movement was stopped")
                return -1
            self.printMsg("homing, current position: " + str(pos_now))
            pos_old = pos_now
            dir_old = dir_now

        self.setLimitSwitches(0)
        self.setParameter("VM", self.ENDVELOCITY)
        self.setParameter("R1", counts + 1)

    def gotoIdlePosition(self):
        self.printMsg("Going to idle position: " + str(self.IDLE_POSITION))
        self.moveAbsolute(self.IDLE_POSITION, monitor=False)


    def monitorMovement(self, show=True):
        while self.isMoving():
            if show:
                pos = self.getPosition()
                self.printMsg("current position: " + str(pos))

        pos = self.getPosition()
        self.printMsg("final position: " + str(pos))

# To home function

    def toHome(self):
        self.setParameter("R1", self.USER1) ### added extra
        # check if manual homing was performed
        counts = int(self.getParameter("R1"))
        if counts < 1:
            self.printMsg("Manual homing was not performed, aborting homing procedure")
            return -1

        self.setParameter("VM", self.HOMINGVELOCITY)
        self.setHomeSwitch(0)
        self.printMsg("Homing")
        Direction = int(self.HOMING_MOVEMENT_DIRECTION)
        
        if self.axis == 2:         # Rotary Motor
            self.moveRelative(Direction*25000)
            print(" ____________ Please wait for 1 minute_____________________")
            time.sleep(100)
        
            self.printMsg(bcolors.OKGREEN + "Current Encoder Reading:  " + str(self.getPosition())  + bcolors.ENDC)
            time.sleep(3)   
                
            self.homeAxis()
            self.printMsg(bcolors.OKGREEN + "________Please wait 20 sec.________  " + bcolors.ENDC)
            time.sleep(20)
            self.homeAxis()
            time.sleep(20)
            self.printMsg(bcolors.OKGREEN + "Current Encoder Reading corresping to Homing:  " + str(self.getPosition())  + bcolors.ENDC)
            
        elif self.axis == 1:         # Linear Motor.
            self.moveRelative(Direction*4000)             # set 'HOMING_MOVEMENT_DIRECTION' to +1 and Direction*'some positive number' here
            						    # or 'HOMING_MOVEMENT_DIRECTION' to -1 and Direction*'negetive number'
            print(" ____________ Please wait for a minute_____________________")
            time.sleep(60)
        
            self.printMsg(bcolors.OKGREEN + "Current Encoder Reading:  " + str(self.getPosition())  + bcolors.ENDC)
            self.printMsg(bcolors.OKGREEN + "Current Encoder Reading corresping to Homing:  " + str(self.getPosition())  + bcolors.ENDC)
            
            
        else:
            print(" Error in recognising the motor. Please check the configuration file and also verify the connections. ")
            



        
        
# The following set of code is for trigger from photodiode.

    
    def setTriggerInput(self, attempts):
        
        if attempts == 4:
            self.printError("Setting the trigger input failed 5 times -> exiting")
            sys.exit(-1)
        if self.axis == 1:
            self.printMsg("Set trigger from Photodiode to Linear encoder.")
            set = self.setParameter("S3", "0,0,0")  # takes input , 1 means active when high
            print("____feedthrough____385",set)
        elif self.axis== 2:
            self.printMsg("Cant set trigger to rotary motor, if needed please change the code __feedthrough__323_")
        time.sleep(0.5)
        # check if S3 was set correctly
        if set != 0:
            self.printMsg("Trigger is not set correctly")
            self.setTriggerInput(attempts + 1)
            self.stopMovement()
    
    def getTriggerOutput(self):
        reply = self.getParameter("I3")
        print("___feedthrough.py 397__", reply)
        return(reply)
        
            

        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
