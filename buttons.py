import RPi.GPIO as GPIO

handler = None

BUTTONS = [5, 6, 16, 24]

def init(func):
    global handler
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    for pin in BUTTONS:
        GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)
    handler = func

def handle_button(pin):
    handler(BUTTONS.index(pin))