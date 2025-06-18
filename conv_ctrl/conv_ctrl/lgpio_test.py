from time import sleep
from gpiozero import LED

led = LED(23)
GPIO = 23
#h = lgpio.gpiochip_open(0)

#lgpio.gpio_claim_output(h, 0, GPIO, 0)

for _ in range(10):
    led.on()
    sleep(1.0)
    led.off()
    sleep(1.0)
    #lgpio.gpio_write(h, GPIO, 1)
    #time.sleep(1)
    #lgpio.gpio_write(h, GPIO, 0)
   # time.sleep(1)

#lgpio.gpiochip_close(h)
print("done")
    
