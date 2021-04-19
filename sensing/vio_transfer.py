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
    local_pose.pose.position.x = - local_pose.pose.position.x
    local_pose.pose.position.y = - local_pose.pose.position.y
       
rospy.init_node(vehicle_type+"_"+vehicle_id+'_vio_transfer')
rospy.Subscriber("/t265/odom/sample", Odometry, vio_callback)
position_pub = rospy.Publisher(vehicle_type+"_"+vehicle_id+"/mavros/vision_pose/pose", PoseStamped, queue_size=2)
rate = rospy.Rate(20) 

while not rospy.is_shutdown():
    local_pose.header.stamp = rospy.Time.now()
    position_pub.publish(local_pose) 
    rate.sleep()
  
