#!usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16, Float64
import time
import lgpio

relay1 = 23
relay2 = 17

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, relay1)
lgpio.gpio_claim_output(h, relay2)

class ConvCtrl(Node):
    def __init__(self):
        super().__init__("conveyor3node")
        self.cmd_sub = self.create_subscription(Int16, "conv_cmd", self.ctrl_callback, 10)


    def ctrl_callback(self, msg):
        flag = msg.data

        if flag == 0:
            lgpio.gpio_write(h, relay1, 0)
            lgpio.gpio_write(h, relay2, 0)

        elif flag == 1 :
            lgpio.gpio_write(h, relay1, 1)
            lgpio.gpio_write(h, relay2, 0)

        elif flag == -1:
            lgpio.gpio_write(h, relay1, 0)
            lgpio.gpio_write(h, relay2, 1)
        
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
