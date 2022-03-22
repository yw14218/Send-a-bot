import rospy
import actionlib
from geometry_msgs.msg import Point, Pose, Twist, Vector3
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from math import pi

class Pipeline:
    def __init__(self):
        self.cord = None
        self.loop_rate = rospy.Rate(30)
        self.twist_rotate = Twist(Vector3(0.00, 0.00, 0.00), Vector3(0.00, 0.00, 10 * pi / 180))
        self.twist_stop = Twist(Vector3(0.00, 0.00, 0.00), Vector3(0.00, 0.00, 0.00))
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.Subscriber('/OAKD/CloestPerson3D', Point, self.callback_spatialCord)
        self.pub_cmd_vel = rospy.Publisher(
            'RosAria/cmd_vel',
            Twist,
            queue_size=1000
        )
            
    def callback_spatialCord(self, data):
        self.cord = data

    def goal_pose(self):
        goal_pose = MoveBaseGoal()
        goal_pose.target_pose.header.frame_id = 'map'
        goal_pose.target_pose.header.stamp = rospy.Time.now()
        goal_pose.target_pose.pose = Pose(self.cord, quaternion_from_euler(0, 0, 0))
        print(goal_pose)
        return goal_pose

    def rotate_clockwise(self):
        self.pub_cmd_vel.publish(self.twist_rotate)

    def stop_robot(self):
        self.pub_cmd_vel.publish(self.twist_stop)
        
    def start(self):        
        while not rospy.is_shutdown():
            if self.cord is not None:
                self.stop_robot()
                # self.move_base.wait_for_server()
                goal = self.goal_pose()
                self.move_base.send_goal(goal)
                print("-----Approaching a person-----")
                self.move_base.wait_for_result()
                if self.cord.z < 0.5:
                    print("-----Approached a person-----")
                    # invoking ros speech service

            else:
                print("-----Rotating robot-----")
                self.rotate_clockwise()

            self.loop_rate.sleep()
        
if __name__ == '__main__':
    rospy.init_node('main', anonymous=True)
    pipeline = Pipeline()
    pipeline.start()
    