import rospy
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry
import math
from pyquaternion import Quaternion
from tf2_ros import TransformListener, Buffer
import sys

vehicle_type = sys.argv[1]
vehicle_id = sys.argv[2]
camera_pose = PoseStamped()
camera_pose.header.frame_id = 'map'
camera_odom = Odometry()



def odom_callback(data):
    global camera_odom, camera_pose
    camera_odom = data
    camera_odom.pose.pose.position = camera_pose.pose.position
    camera_odom.twist.twist.linear.x = -camera_odom.twist.twist.linear.x
    camera_odom.twist.twist.linear.y = -camera_odom.twist.twist.linear.y
    
rospy.init_node(vehicle_type+"_"+vehicle_id+'_ego_transfer')
rospy.Subscriber("/t265/odom/sample", Odometry, odom_callback)
pose_pub = rospy.Publisher("/camera_pose", PoseStamped, queue_size=2)
odom_pub = rospy.Publisher("/camera_odom", Odometry, queue_size=2)
rate = rospy.Rate(20) 
tfBuffer = Buffer()
tflistener = TransformListener(tfBuffer)

while not rospy.is_shutdown():
    try:
        tfstamped = tfBuffer.lookup_transform('map', 'camera', rospy.Time(0))
        camera_pose.header.stamp = rospy.Time.now()
        camera_pose.pose.position.x = tfstamped.transform.translation.x
        camera_pose.pose.position.y = tfstamped.transform.translation.y
        camera_pose.pose.position.z = tfstamped.transform.translation.z
        camera_pose.pose.orientation =  tfstamped.transform.rotation
        pose_pub.publish(camera_pose) 
        odom_pub.publish(camera_odom)
        rate.sleep()
    except:
        rate.sleep()

  
