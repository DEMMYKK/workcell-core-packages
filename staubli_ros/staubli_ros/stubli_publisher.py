import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
import csv
import transforms3d

class ROSPoseSubscriberPublisher(Node):
    def __init__(self, sub_topic, sub_csv_file, pub_topic, pub_csv_file):
        super().__init__('pose_subscriber_publisher')
        self.sub_topic = sub_topic
        self.sub_csv_file = sub_csv_file
        self.pub_topic = pub_topic
        self.pub_csv_file = pub_csv_file
        # self.init_sub_csv()
        self.setup_subscriber()
        self.setup_publisher()

    def init_sub_csv(self):
        # Initialize the subscriber CSV file with headers for position and orientation in RPY format
        with open(self.sub_csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Position_X', 'Position_Y', 'Position_Z', 
                             'Roll', 'Pitch', 'Yaw'])

    def setup_subscriber(self):
        self.create_subscription(PoseStamped, self.sub_topic, self.callback, 10)

    def setup_publisher(self):
        self.publisher = self.create_publisher(PoseStamped, self.pub_topic, 10)

    def callback(self, data):
        try:
            # Extract position and orientation from the message
            timestamp = data.header.stamp.sec + data.header.stamp.nanosec * 1e-9
            position = data.pose.position
            orientation = data.pose.orientation
            
            # Convert quaternion to RPY
            # quaternion = (orientation.x, orientation.y, orientation.z, orientation.w)
            # rpy = transforms3d.euler.quat2euler(quaternion)
            rpy = (orientation.x, orientation.y, orientation.z)
            # Create a list of data to write to the subscriber CSV file
            pose_data = [timestamp, position.x, position.y, position.z, rpy[0], rpy[1], rpy[2]]
            
            # Open the subscriber CSV file and append the data
            with open(self.sub_csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(pose_data)
            self.get_logger().info(f"Data written to {self.sub_csv_file}: {pose_data}")
        except Exception as e:
            self.get_logger().error(f"Error processing message: {e}")

    def read_pub_csv_and_publish(self):
        try:
            with open(self.pub_csv_file, mode='r') as file:
                reader = csv.reader(file)
                row=next(reader)
                # Extract data from the publisher CSV row
                # timestamp = float(row['Timestamp'])
                # rospy.loginfo(f"row: {row[1]}")
                timestamp = self.get_clock().now().to_msg()
                x = float(row[0])#['Position_X'])
                y = float(row[1])#['Position_Y'])
                z = float(row[2])#['Position_Z'])
                roll = float(row[3])#['Roll'])
                pitch = float(row[4])#['Pitch'])
                yaw = float(row[5])#['Yaw'])
                file.close()
                # Convert RPY to quaternion
                # quaternion = transforms3d.euler.euler2quat(roll, pitch, yaw)
                
                # Create PoseStamped message
                pose_msg = PoseStamped()
                pose_msg.header.stamp = timestamp
                pose_msg.pose.position.x = x
                pose_msg.pose.position.y = y
                pose_msg.pose.position.z = z
                pose_msg.pose.orientation.x = roll#quaternion[0]
                pose_msg.pose.orientation.y = pitch#quaternion[1]
                pose_msg.pose.orientation.z = yaw#quaternion[2]
                pose_msg.pose.orientation.w = yaw#quaternion[3]
                    
                    
                # Publish the message
                self.publisher.publish(pose_msg)
                self.get_logger().info(f"Published pose: {pose_msg}")
                # rclpy.spin_once(self, timeout_sec=0.5)  # Adjust the sleep duration as needed
        except Exception as e:
            self.get_logger().error(f"Error reading CSV and publishing messages: {e}")

    def run(self):
        # Create a timer to periodically read the publisher CSV and publish
        self.create_timer(1.0, self.read_pub_csv_and_publish)
        rclpy.spin(self)

def main(args=None):
    rclpy.init(args=args)
    try:
        print("main")
        # Replace '/pose_topic', 'sub_data.csv', '/publish_topic', and 'pub_data.csv' with your specific topics and files
        subscriber_publisher = ROSPoseSubscriberPublisher('/pose_publish_topic', '/home/wcl-staubli-i/RoboDK/Library/Scripts/test.csv', '/pose_recived_topic', '/home/wcl-staubli-i/RoboDK/Library/Scripts/joints.csv')
        subscriber_publisher.run()
    except rclpy.exceptions.ROSInterruptException:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
