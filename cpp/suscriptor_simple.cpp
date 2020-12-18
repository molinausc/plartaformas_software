#include<ros/ros.h> //ros para c++
#include<std_msgs/Int32.h> // tipo de mensaje al que vamos a suscribirnos

/*Callback que será invocado cada vez que se reciba un mensaje en el topic.
 * La estructura de la función la proporciona ROS, no podemos modificarla
 * No puede devolver nada: void
 * el argumento de la función es una referencia (paso por referencia) al tipo: std_msgs::Int32ConstPtr y la 
 * referencia es constante (const) por lo que no se puede modificar internamente
*/
void contadorCallBack(const std_msgs::Int32ConstPtr & msg){ 

    ROS_INFO("CallBack contador: %i",msg->data);//Imprime el valor de data en el lugar del %i (entero)

}
int main (int argc, char ** argv){

    ros::init(argc, argv, "suscriptor_simple_node");// inicializa el nodo
    ros::NodeHandle nh;//El NodeHandle es la clase que nos permite crear suscriptores

    /*Subscribe es una template. Tenemos que decirle el tipo de mensaje al que va a 
     * suscribirse <std_msgs::Int32>
     * (nombre_del_topic,queue_size, callback)
     */
    ros::Subscriber sub=nh.subscribe<std_msgs::Int32>("contador",10,contadorCallBack);

    ros::spin();
    
    return 0;
}

