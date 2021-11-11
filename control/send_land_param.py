import rospy
from std_msgs.msg import  Float32MultiArray
import sys

vehicle_type = sys.argv[1]
vehicle_id = sys.argv[2]
rospy.init_node(vehicle_type+'_'+vehicle_id+'_send_land_param')
land_vel = 0.3
x_bias = 0
y_bias = -0.6
land_param = Float32MultiArray()
land_param.data.append(land_vel)
land_param.data.append(x_bias)
land_param.data.append(y_bias)
rate = rospy.Rate(10)
while not rospy.is_shutdown():
    land_param_pub = rospy.Publisher('/xtdrone/'+vehicle_type+'_'+vehicle_id+'/land_param', Float32MultiArray, queue_size=1)
    land_param_pub.publish(land_param)
    rate.sleep()