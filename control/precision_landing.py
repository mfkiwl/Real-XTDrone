import rospy
from geometry_msgs.msg import Twist, PoseStamped, TransformStamped
from std_msgs.msg import String
from tf2_ros import TransformListener, Buffer
import sys

def local_pose_callback(data):
    global local_pose
    local_pose = data

if __name__ == '__main__':
    vehicle_type = sys.argv[1]
    vehicle_id = sys.argv[2]
    rospy.init_node(vehicle_type+'_'+vehicle_id+'_precision_landing')
    tfBuffer = Buffer()
    tflistener = TransformListener(tfBuffer)
    cmd_vel_enu = Twist()   
    cmd = String()
    local_pose = PoseStamped()
    Kp = 1.0
    land_vel = 0.5
    not_find_time = 0
    get_time = False
    rospy.Subscriber(vehicle_type+'_'+vehicle_id+"/mavros/vision_pose/pose", PoseStamped, local_pose_callback)
    cmd_vel_pub = rospy.Publisher('/xtdrone/'+vehicle_type+'_'+vehicle_id+'/cmd_vel_enu', Twist, queue_size=2)
    cmd_pub = rospy.Publisher('/xtdrone/'+vehicle_type+'_'+vehicle_id+'/cmd', String, queue_size=2)
    rate = rospy.Rate(20)
    while not rospy.is_shutdown():
        try:
            tfstamped = tfBuffer.lookup_transform('map', 'tag_'+vehicle_id, rospy.Time(0))
            get_time = False
            print(tfstamped.transform.translation.x,tfstamped.transform.translation.y)
            cmd_vel_enu.linear.x = Kp * (tfstamped.transform.translation.x+0.3 - local_pose.pose.position.x)
            cmd_vel_enu.linear.y = Kp * (tfstamped.transform.translation.y - local_pose.pose.position.y)
            cmd_vel_enu.linear.z = -land_vel
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


