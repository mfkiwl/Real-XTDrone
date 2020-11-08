import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import sys

vehicle_type = sys.argv[1]
vehicle_id = sys.argv[2]
local_pose = PoseStamped()
local_pose.header.frame_id = 'map'

def vio_callback(data):
    local_pose.pose= data.pose.pose
       
rospy.init_node('vio_transfer')
rospy.Subscriber("/t265/odom/sample", Odometry, vio_callback)
position_pub = rospy.Publisher("/mavros/vision_pose/pose", PoseStamped, queue_size=2)
rate = rospy.Rate(20) 

while True:
    local_pose.header.stamp = rospy.Time.now()
    position_pub.publish(local_pose) 
    rate.sleep()
  