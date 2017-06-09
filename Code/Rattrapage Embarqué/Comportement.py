class Comportement(Enum):
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5
    ENABLEMAGNET = 6
    DISABLEMAGNET = 7

    def EsquiveObstacle(mutexSonar):
        while True:
        # Use BCM GPIO references
        # instead of physical pin numbers
        GPIO.setmode(GPIO.BCM)
        # Define GPIO to use on Pi
        GPIO_TRIGGER = 21
        GPIO_ECHO    = 26
        # Set pins as output and input
        GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  
        GPIO.setup(GPIO_ECHO,GPIO.IN)  
        # Set trigger to False (Low)
        GPIO.output(GPIO_TRIGGER, False)
        # Allow module to settle
        time.sleep(0.5)
        # Send 10us pulse to trigger
        GPIO.output(GPIO_TRIGGER, True)
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
        start = time.time()
        while GPIO.input(GPIO_ECHO)==0:
            start = time.time()
        while GPIO.input(GPIO_ECHO)==1:
            stop = time.time()
        # Calculate pulse length
        elapsed = stop-start
        # Distance pulse travelled in that time is time
        # multiplied by the speed of sound (cm/s)
        global distance
        distance = elapsed * 34300
        # That was the distance there and back so halve the value
        distance = distance / 2
        #print "Distance : %.1f" % distance
        # Reset GPIO settings
        GPIO.cleanup()
        
        return distance
