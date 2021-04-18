import rospy
from geometry_msgs.msg import PoseStamped
import sys

vehicle_type = sys.argv[1]
vehicle_id = sys.argv[2]
local_pose = PoseStamped()
local_pose.header.frame_id = 'map'

def mocap_callback(data):
    global local_pose
    local_pose= data
       
rospy.init_node(vehicle_type+"_"+vehicle_id+'_mocap_transfer')
rospy.Subscriber("/vrpn_client_node/quad0176/pose", PoseStamped, mocap_callback)
position_pub = rospy.Publisher(vehicle_type+"_"+vehicle_id+"/mavros/vision_pose/pose", PoseStamped, queue_size=2)
rate = rospy.Rate(20) 

while True:
    local_pose.header.stamp = rospy.Time.now()
    position_pub.publish(local_pose) 
    rate.sleep()
  
