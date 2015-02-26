# Imports
import webiopi
import thread
import time

# Retrieve GPIO lib
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

state = 5
# Left motor GPIOs
L1=17 # H-Bridge 1
L2=27 # H-Bridge 2
LS=22 # H-Bridge 1,2EN

LV1=9
LV2=11
LVLASTPHASE=0
LVCOUNTER=0

RV1=8
RV2=7
RVLASTPHASE=0
RVCOUNTER=0

# Right motor GPIOs
R1=23 # H-Bridge 3
R2=24 # H-Bridge 4
RS=25 # H-Bridge 3,4EN




# -------------------------------------------------- #
# Convenient PWM Function                            #
# -------------------------------------------------- #

# Set the speed of two motors
def set_speed(Lspeed, Rspeed):
    GPIO.pulseRatio(LS, Lspeed)
    GPIO.pulseRatio(RS, Rspeed)

# -------------------------------------------------- #
# Left Motor Functions                               #
# -------------------------------------------------- #

def left_stop():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.LOW)

def left_forward():
    GPIO.output(L1, GPIO.HIGH)
    GPIO.output(L2, GPIO.LOW)

def left_backward():
    GPIO.output(L1, GPIO.LOW)
    GPIO.output(L2, GPIO.HIGH)

# -------------------------------------------------- #
# Right Motor Functions                              #
# -------------------------------------------------- #
def right_stop():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.LOW)

def right_forward():
    GPIO.output(R1, GPIO.HIGH)
    GPIO.output(R2, GPIO.LOW)

def right_backward():
    GPIO.output(R1, GPIO.LOW)
    GPIO.output(R2, GPIO.HIGH)

# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #

def go_forward():
    global state
    state=8
    left_forward()
    right_forward()

def go_backward():
    global state
    state=2
    left_backward()
    right_backward()

def turn_left():
    global state
    state=4
    left_backward()
    right_forward()

def turn_right():
    global state
    state=6
    left_forward()
    right_backward()

def stop():
    global state
    state=5
    left_stop()
    right_stop()
    

count = 0
# -------------------------------------------------- #
# My thread
# -------------------------------------------------- #
def threadForLeft(threadName):
    global LVCOUNTER
    global LVLASTPHASE
    while 1:
        if state == 8:
            t = GPIO.input(LV1) * 2 + GPIO.input(LV2)
            if t == 0:
                if LVLASTPHASE == 0:
                    pass
                else:
                    LVCOUNTER += 1

            if t == 1:
                if LVLASTPHASE == 0 or LVLASTPHASE == 1:
                    pass
                if LVLASTPHASE == 3 or LVLASTPHASE == 2:
                    LVCOUNTER += 1

            if t == 3:
                if LVLASTPHASE == 0 or LVLASTPHASE == 1 or LVLASTPHASE == 3:
                    pass
                if LVLASTPHASE == 2:
                    LVCOUNTER += 1

            if t == 2:
                pass

            LVLASTPHASE = t
            # print "GPIO9:GPIO11 = %d:%d" %(GPIO.input(LV1), GPIO.input(LV2))
            print "LVCOUNTER = %d" %(LVCOUNTER)


#            if LVCOUNTER > RVCOUNTER:
#                set_speed(1.0*RVCOUNTER/LVCOUNTER, 1.0)
#            if LVCOUNTER < RVCOUNTER:
#                set_speed(1.0, 1.0*LVCOUNTER/RVCOUNTER)
        else:
            set_speed(1.0, 1.0)
        

def threadForRight(threadName):
    global RVCOUNTER
    global RVLASTPHASE
    while 1:
        if state == 8:
            t = GPIO.input(RV1) * 2 + GPIO.input(RV2)
            if t == 0:
                if RVLASTPHASE == 0:
                    pass
                else:
                    RVCOUNTER += 1

            if t == 1:
                if RVLASTPHASE == 0 or RVLASTPHASE == 1:
                    pass
                if RVLASTPHASE == 3 or RVLASTPHASE == 2:
                    RVCOUNTER += 1

            if t == 3:
                if RVLASTPHASE == 0 or RVLASTPHASE == 1 or RVLASTPHASE == 3:
                    pass
                if RVLASTPHASE == 2:
                    RVCOUNTER += 1

            if t == 2:
                pass

            RVLASTPHASE = t
            # print "GPIO8:GPIO7 = %d:%d" %(GPIO.input(RV1), GPIO.input(RV2))
            print "RVCOUNTER = %d" %(RVCOUNTER)



# -------------------------------------------------- #
# Creat two thread to caculate rotary speed
# -------------------------------------------------- #
thread.start_new_thread( threadForLeft, ("threadForLeft", ) )
thread.start_new_thread( threadForRight, ("threadForRight", ) )

# -------------------------------------------------- #
# Initialization part                                #
# -------------------------------------------------- #

# Setup GPIOs
GPIO.setFunction(LV1, GPIO.IN)
GPIO.setFunction(LV2, GPIO.IN)
GPIO.setFunction(LS, GPIO.PWM)
GPIO.setFunction(L1, GPIO.OUT)
GPIO.setFunction(L2, GPIO.OUT)

GPIO.setFunction(RV1, GPIO.IN)
GPIO.setFunction(RV2, GPIO.IN)
GPIO.setFunction(RS, GPIO.PWM)
GPIO.setFunction(R1, GPIO.OUT)
GPIO.setFunction(R2, GPIO.OUT)

set_speed(1.0, 1.0)
stop()

# -------------------------------------------------- #
# Main server part                                   #
# -------------------------------------------------- #


# Instantiate the server on the port 8000, it starts immediately in its own thread
server = webiopi.Server(port=8000, login="cambot", password="cambot")

# Register the macros so you can call it with Javascript and/or REST API

server.addMacro(go_forward)
server.addMacro(go_backward)
server.addMacro(turn_left)
server.addMacro(turn_right)
server.addMacro(stop)

# -------------------------------------------------- #
# Loop execution part                                #
# -------------------------------------------------- #

# Run our loop until CTRL-C is pressed or SIGTERM received
webiopi.runLoop()

# -------------------------------------------------- #
# Termination part                                   #
# -------------------------------------------------- #

# Stop the server
server.stop()

# Reset GPIO functions
GPIO.setFunction(LS, GPIO.IN)
GPIO.setFunction(L1, GPIO.IN)
GPIO.setFunction(L2, GPIO.IN)

GPIO.setFunction(RS, GPIO.IN)
GPIO.setFunction(R1, GPIO.IN)
GPIO.setFunction(R2, GPIO.IN)

