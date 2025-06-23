import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16, Bool
import serial
import time

class ArduinoWrapper(Node):

    def __init__(self):
        super().__init__('arduino_gripper')
        self.serial = serial.Serial("/dev/ttyACM0", 115200)
        time.sleep(1)
        # self.reset_encoders()
        self.pub_a = self.create_publisher(Int16, 'Encoder_A', 10)
        #self.pub_b = self.create_publisher(Int16, 'Encoder_B', 10)
        timer_period = 0.1  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subscription = self.create_subscription(Bool, 'grip_cmd', self.open_gripper, 10)
        self.subscription  # prevent unused variable warning
    
    def open_gripper(self, msg):
        open_cmd = msg.data
        if open_cmd == True:    
            open_command = "1" 
            self.serial.write((open_command + "\n").encode()) 

        else:
            open_command = "0"
            self.serial.write((open_command + "\n").encode())  
        print(open_command)
        #self.get_logger().info("Sent reset command (1) to Arduino")
    
 
def main(args=None):
    rclpy.init(args=args)

    node = ArduinoWrapper()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
