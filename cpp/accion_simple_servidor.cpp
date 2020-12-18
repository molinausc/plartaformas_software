#include<ros/ros.h>
#include<actionlib/server/simple_action_server.h>
#include<my_own_action_msgs/simpleactionmsgAction.h>
#include<iostream>
using namespace std;


actionlib::SimpleActionServer<my_own_action_msgs::simpleactionmsgAction> *action_server;
void goalCallBack(const my_own_action_msgs::simpleactionmsgGoalConstPtr & goal){

    my_own_action_msgs::simpleactionmsgFeedback server_feedback;
    my_own_action_msgs::simpleactionmsgResult server_result;
        int cont=0;
        ros::Rate loop_rate(1); 
        bool success=true;
        for(cont=0; cont<goal->number; cont++){
            ROS_INFO("Doing things: %i sec.",cont);
            if (action_server->isPreemptRequested())
                {
                    ROS_INFO("Cancelling action");
                    success=false;
                    //action_server->setPreempted();
                    break;


                }
            server_feedback.partial=cont;
            action_server->publishFeedback(server_feedback);
            loop_rate.sleep();

        }
    
        server_result.msg=(success)?"Terminado":"Cancelado";
        server_result.total=cont;
        if (success)
            action_server->setSucceeded(server_result);
        else 
            action_server->setPreempted(server_result);
}
int main(int argc, char ** argv)
{
    ros::init(argc,argv, "name");
    ros::NodeHandle nh;

   
  
   action_server= new actionlib::SimpleActionServer<my_own_action_msgs::simpleactionmsgAction>(nh,"simple_action_server",&goalCallBack,false);
    
    action_server->start();

    ros::spin();    
    return 0;
}
