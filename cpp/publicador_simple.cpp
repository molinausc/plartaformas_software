#include <ros/ros.h> //ros para c++
#include<std_msgs/Int32.h> //tipo de mensaje que vamos a publicar

int main(int argc,char ** argv){
    ros::init(argc, argv, "publicador_simple_node");//inicializa el nodo.
    ros::NodeHandle nh;//El NodeHandle nos permite crear publicadores

    ros::Publisher pub=nh.advertise<std_msgs::Int32>("contador", 10);
    /*el método advertise crea un publicador. Es una template, necesitamos indicarle el tipo de mensaje que va a publicar. \"contador\" es el nombre del topic en el que vamos a publicar. El segundo parámetro es el queue size*/
    ros::Rate loop_rate(2);
    std_msgs::Int32 msg; //Mensaje que vamos a publicar
    msg.data=0;//le damos valor al mensaje
    
    while(ros::ok()){
        pub.publish(msg);//publicamos el mensaje
        msg.data++;//actualizamos el valor del mensaje
        loop_rate.sleep();// el bucle se ejecuta a 2hz
    }

    return 0;//La función main tiene que devolver un entero. 0=todo ok
}   
