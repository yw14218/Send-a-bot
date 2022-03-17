#ifndef ___ROBOTTHREAD_H___
#define ___ROBOTTHREAD_H___

#include <QThread>
#include <QObject>
#include <QStringList>
#include <stdlib.h>
#include <iostream>
#include "assert.h"

#include <ros/ros.h>
#include <ros/network.h>
#include <std_msgs/String.h>
#include <sensor_msgs/LaserScan.h>
#include <geometry_msgs/Twist.h>
#include <turtlesim/Velocity.h>
#include <turtlesim/Pose.h>
#include <nav_msgs/Odometry.h>
#include <actionlib/client/simple_action_client.h>
#include <move_base_msgs/MoveBaseAction.h>

namespace server {

typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveBaseClient;

class RobotThread : public QThread {
	Q_OBJECT
public:
    RobotThread(int argc, char **pArgv);
    virtual ~RobotThread();

    double getXPos();
    double getXSpeed();
    double getASpeed();
    double getYPos();
    double getAPos();

    bool init();

    void callback(nav_msgs::Odometry msg);
    //void callback(turtlesim::Pose msg);
    void scanCallBack(sensor_msgs::LaserScan scan);

	void SetSpeed(double speed, double angle);
    void setPose(QList<double> to_set);
    void goToXYZ(geometry_msgs::Point goTo);
    void setCommand(QString cmd);
    void run();

    Q_SIGNAL void newPose(double,double,double);
    Q_SIGNAL void newMidLaser(double);

private:
    QString command;
	
    int m_Init_argc;
    char** m_pInit_argv;

    double m_speed;
    double m_angle;

    double m_xPos;
    double m_yPos;
    double m_aPos;

    double m_maxRange;
    double m_minRange;

    QList<double> ranges;

    ros::Publisher cmd_publisher;
    ros::Publisher sim_velocity;

    ros::Subscriber pose_listener;
    ros::Subscriber scan_listener;
};
}//end namespace
#endif

