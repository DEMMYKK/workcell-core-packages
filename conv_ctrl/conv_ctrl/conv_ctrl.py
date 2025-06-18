#!usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16, Float64
import time
#import lgpio
from gpiozero import LED

relay1 = LED(23)
relay2 = LED(17)

#h = lgpio.gpiochip_open(0)
#lgpio.gpio_claim_output(h, relay1)
#lgpio.gpio_claim_output(h, relay2)

class ConvCtrl(Node):
    def __init__(self):
        super().__init__("conveyor3node")
        self.cmd_sub = self.create_subscription(Int16, "conv3_cmd", self.ctrl_callback, 10)


    def ctrl_callback(self, msg):
        flag = msg.data
        
        print(flag)
        if flag == 0:
            relay1.off()
            relay2.off()

        elif flag == 1 :
            #print("now running")
            relay1.on()
            relay2.off()
        elif flag == -1:
            relay1.on()
            relay2.on()
        
        else:
            print("waiting for valid flag")

def main(args=None):
    rclpy.init(args=args)
    conv_ctrl = ConvCtrl()
    rclpy.spin(conv_ctrl)
    conv_ctrl.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
