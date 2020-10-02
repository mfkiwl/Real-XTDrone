import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import math
from pyquaternion import Quaternion
import tf
import sys

vehicle_type = sys.argv[1]
vehicle_id = sys.argv[2]
local_pose = PoseStamped()
local_pose.header.frame_id = 'map'
quaternion = tf.transformations.quaternion_from_euler(0, -math.pi/2, math.pi/2)
q = Quaternion([quaternion[3],quaternion[0],quaternion[1],quaternion[2]])

def vio_callback(data):
    #rospy.loginfo(str(data.pose.position.x)+','+str(data.pose.position.y)+','+str(data.pose.position.z))
    
    local_pose.pose.position.x = -data.pose.pose.position.y
    local_pose.pose.position.y = data.pose.pose.position.x
    local_pose.pose.position.z = data.pose.pose.position.z
    q_= Quaternion([data.pose.pose.orientation.w,data.pose.pose.orientation.x,data.pose.pose.orientation.y,data.pose.pose.orientation.z])
    q_ = q_*q
    local_pose.pose.orientation.w = q_[0]
    local_pose.pose.orientation.x = q_[1]
    local_pose.pose.orientation.y = q_[2]
    local_pose.pose.orientation.z = q_[3]
    
rospy.init_node('vio_transfer')
rospy.Subscriber("/camera/odom/sample", Odometry, vio_callback)
position_pub = rospy.Publisher(vehicle_type + '_' + vehicle_id + "/mavros/vision_pose/pose", PoseStamped, queue_size=2)
rate = rospy.Rate(20) 

while True:
    local_pose.header.stamp = rospy.Time.now()
    position_pub.publish(local_pose) 
    rate.sleep()
  
