import RPi.GPIO as GPIO
import time

CLKPin = 11
DTPin = 12
SWPin = 13
BuzzerPin = 15

globalCounter = 0

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(CLKPin, GPIO.IN)
    GPIO.setup(DTPin, GPIO.IN)
    GPIO.setup(SWPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BuzzerPin, GPIO.OUT)
    rotaryClear()

def rotaryDeal():
    global globalCounter
    last_dt_status = GPIO.input(DTPin)
    while not GPIO.input(CLKPin):
        current_dt_status = GPIO.input(DTPin)
        if last_dt_status != current_dt_status:
            globalCounter += 1
            print('globalCounter = %d' % globalCounter)
            if globalCounter == 20:
                trigger_buzzer()
                globalCounter = 0
        last_dt_status = current_dt_status

def trigger_buzzer():
    GPIO.output(BuzzerPin, GPIO.HIGH)
    time.sleep(0.4)
    GPIO.output(BuzzerPin, GPIO.LOW)

def clear(ev=None):
    global globalCounter
    globalCounter = 0
    print('globalCounter = %d' % globalCounter)
    time.sleep(1)

def rotaryClear():
    GPIO.add_event_detect(SWPin, GPIO.FALLING, callback=clear)

def loop():
    while True:
        rotaryDeal()

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
