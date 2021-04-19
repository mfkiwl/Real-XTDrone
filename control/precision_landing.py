import rospy
from geometry_msgs.msg import Twist, PoseStamped, TransformStamped
from std_msgs.msg import String, Float32MultiArray
from tf2_ros import TransformListener, Buffer
import sys

def local_pose_callback(data):
    global local_pose
    local_pose = data

def land_param_callback(data):
    global land_vel, x_bias, y_bias, land_flag
    # print(data)
    land_vel = data.data[0]
    x_bias = data.data[1]
    y_bias = data.data[2]
    land_flag = True
    print('land_vel: ' + str(land_vel))
    print('x_bias: ' + str(x_bias))
    print('y_bias: ' + str(y_bias))

if __name__ == '__main__':
    vehicle_type = sys.argv[1]
    vehicle_id = sys.argv[2]
    rospy.init_node(vehicle_type+'_'+vehicle_id+'_precision_landing')
    tfBuffer = Buffer()
    tflistener = TransformListener(tfBuffer)
    cmd_vel_enu = Twist()   
    cmd = String()
    local_pose = PoseStamped()
    land_flag = False
    Kp_xy = 0.5
    Kp_z= 0.5
    land_vel = 0
    x_bias = 0
    y_bias = 0
    z_bias = 1
    not_find_time = 0
    get_time = False
    rospy.Subscriber(vehicle_type+'_'+vehicle_id+"/mavros/vision_pose/pose", PoseStamped, local_pose_callback)
    rospy.Subscriber('/xtdrone/'+vehicle_type+'_'+vehicle_id+'/land_param', Float32MultiArray, land_param_callback)
    cmd_vel_pub = rospy.Publisher('/xtdrone/'+vehicle_type+'_'+vehicle_id+'/cmd_vel_enu', Twist, queue_size=2)
    cmd_pub = rospy.Publisher('/xtdrone/'+vehicle_type+'_'+vehicle_id+'/cmd', String, queue_size=2)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        try:
            tfstamped = tfBuffer.lookup_transform('map', 'tag_'+vehicle_id, rospy.Time(0))
            get_time = False
            cmd_vel_enu.linear.x = Kp_xy * (tfstamped.transform.translation.x + x_bias - local_pose.pose.position.x)
            cmd_vel_enu.linear.y = Kp_xy* (tfstamped.transform.translation.y + y_bias - local_pose.pose.position.y)
            if land_flag:
                cmd_vel_enu.linear.z = -land_vel
            else:
                cmd_vel_enu.linear.z  =  Kp_z * (tfstamped.transform.translation.z + z_bias - local_pose.pose.position.z)
            print(cmd_vel_enu)
        except:
                if not get_time:
                    not_find_time = rospy.get_time()
                    get_time = True
                if rospy.get_time() - not_find_time > 2.0:
                    cmd_vel_enu.linear.x = 0.0
                    cmd_vel_enu.linear.y = 0.0
                    cmd_vel_enu.linear.z = 0.0
                    cmd = 'HOVER'
                    print(cmd)
                    get_time = False
        cmd_vel_pub.publish(cmd_vel_enu)
        cmd_pub.publish(cmd)
        rate.sleep()


