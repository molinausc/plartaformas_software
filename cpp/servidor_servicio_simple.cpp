#include<ros/ros.h>//ROS para c++
#include<my_own_srv_pkg/ownsrv.h> //Mi paquete con mis mensajes


/*Ojo!!! recibe referencias que no son constantes. Esto significa que se cambian en la función y es la forma de devolver información*/
bool mySrvCallBack(my_own_srv_pkg::ownsrvRequest &request, my_own_srv_pkg::ownsrvResponse &response)
{
    ros::Rate loop_rate(1);
    ROS_INFO("Servicio iniciado");
    for (int i=0; i<request.duration; i++)
    {
        ROS_INFO("Segundos transcurridos: %i", i);
        loop_rate.sleep();

    }
    response.success=true;//modificamos la referencia al mensaje response para devolver un resultado

    return true;
}


int main(int argc, char ** argv){
    ros::init(argc,argv, "node_name");// inicializa el nodo. Este nombre se sobreescribe con el launch
    ros::NodeHandle nh; //clase para crear el cliente o el servidor de servicio
    ros::ServiceServer srvserver=nh.advertiseService<my_own_srv_pkg::ownsrvRequest,my_own_srv_pkg::ownsrvResponse>("servicio_extendido", mySrvCallBack);
    /*advertiseService es la función para crear el servidor de servicio. Es una plantilla pero en este caso no es necesario especificarle los tipos, 
     * los obtiene por inferencia (en el ejemplo están especificados). Si se ponen los tipos, éstos tienen que ser los que aparecen en el CallBack */
    ros::spin();
    return 0;
}
