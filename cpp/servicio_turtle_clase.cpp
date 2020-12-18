#include<ros/ros.h>
#include<msg_srv_pkg/turtlebotsrv.h>
#include<geometry_msgs/Twist.h>
#include<sensor_msgs/LaserScan.h>
#include<vector>




class TurtleBot{
  
    ros::NodeHandle nh;
    ros::Publisher pub;
    ros::Subscriber sub;
    ros::ServiceServer srvserver;
    std::vector<float> scanRanges;
    

    void scanCallBack(const sensor_msgs::LaserScanConstPtr & msg){
       
        ros::Rate loop_rate(1);
      
        scanRanges=msg->ranges;
      
    }
    void resetMovement(geometry_msgs::Twist & msg)
    {
        
        msg.linear.x=msg.linear.y=msg.linear.z=0;
        msg.angular.x=msg.angular.y=msg.angular.z=0;
        

    }
    void doLine(int width, geometry_msgs::Twist & msg){
        ros::Rate loop_rate(1);
        resetMovement(msg);
        msg.linear.x=0.3;
        ROS_INFO("Painting line....");
        for (int i=0; i<width; i++)
        {
            
            pub.publish(msg);
            loop_rate.sleep();
        }
         ;

    }
    void doTurn(geometry_msgs::Twist & msg){
        ros::Rate loop_rate(1);
        ROS_INFO("Turning....");
        resetMovement(msg);
        msg.angular.z=1.6;
        for (int i =0;i<2; i++){
            pub.publish(msg);
            loop_rate.sleep();  
    }
      
     

    }
    void doSquare(int area){
       
        geometry_msgs::Twist msg; 
        ROS_INFO("Starting square");
        for (int lado=0; lado<4; lado++)
        {
            doLine(area,msg);
            doTurn(msg);
        }
        ROS_INFO("Finishing square");
    }

    bool turtleServiceCallBack(msg_srv_pkg::turtlebotsrvRequest &request, msg_srv_pkg::turtlebotsrvResponse &response)
    {
        if (!scanRanges.empty())
        {
            ROS_INFO("Distancias.  centro:  %f - dcha: %f - izq: %f",scanRanges[0],scanRanges[scanRanges.size()-1],scanRanges[int(scanRanges.size()/2)]);
            if(scanRanges[0]>=1  &&  scanRanges[scanRanges.size()-1]>=1 &&  scanRanges[int(scanRanges.size()/2)]>=1)
            {
                for (int i=0; i<request.repeticiones; i++){
                    doSquare(request.area);
                    ROS_INFO("The square is finished");
                }
                response.status=true;
                
            }
            else{
                response.status=false;
            }
            return true;
        }
        else
            return false;
    }


    public:
    TurtleBot(){
        
        pub=nh.advertise<geometry_msgs::Twist>("/mobile_base/commands/velocity", 10);
        sub=nh.subscribe<sensor_msgs::LaserScan>("/scan",10, &TurtleBot::scanCallBack, this);
        srvserver=nh.advertiseService ("/turtlebotservice",&TurtleBot::turtleServiceCallBack,this);

    }



};


int main(int argc, char ** argv){

    ros::init(argc, argv, "name");
    TurtleBot bot;
    
    ros::spin();
    return 0;

}

