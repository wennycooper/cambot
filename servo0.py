# Imports
import webiopi
import time

# Retrieve GPIO lib
GPIO = webiopi.GPIO

# -------------------------------------------------- #
# Initialization part                                #
# -------------------------------------------------- #

# Setup GPIOs
GPIO.setFunction(14, GPIO.PWM)

GPIO.pulseRatio(14, 0.065)   
time.sleep(5)
GPIO.pulseRatio(14, 0.085)
time.sleep(5)
GPIO.pulseRatio(14, 0.125)
time.sleep(5)
GPIO.pulseRatio(14, 0.085)




# -------------------------------------------------- #
# Main server part                                   #
# -------------------------------------------------- #

# Instantiate the server on the port 8000, it starts immediately in its own thread
#server = webiopi.Server(port=8000, login="webiopi", password="raspberry")
# or     webiopi.Server(port=8000, passwdfile="/etc/webiopi/passwd")

# -------------------------------------------------- #
# Loop execution part                                #
# -------------------------------------------------- #

# Run our loop until CTRL-C is pressed or SIGTERM received
webiopi.runLoop()

# -------------------------------------------------- #
# Termination part                                   #
# -------------------------------------------------- #

# Cleanly stop the server
#server.stop()

# Reset GPIO functions
GPIO.setFunction(14, GPIO.IN)
