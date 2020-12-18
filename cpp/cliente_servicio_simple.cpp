#include<ros/ros.h> //Ros para c++
#include<std_srvs/Empty.h>//tipo de mensaje de servicio que usaremos para activar el servicio


int main(int argc, char** argv){
    ros::init(argc,argv, "cliente_servicio_name");//inicializa el nodo
    ros::NodeHandle nh;// nos permite crear  clientes de servicios 
    ros::ServiceClient srvc=nh.serviceClient<std_srvs::Empty>("servicio_roberto"); /* crea el cliente para el servicio. Es una plantilla por lo que se necesita especificar el tipo de mensaje de servicio que se va a emplear*/
    std_srvs::Empty srvmsg; // mensaje para llamar al servicio. Normalmente es una estructura con request y response. En el caso de Empty las dos partes están vacías
    srvc.waitForExistence();// Se espera hasta que el servicio esté activo.
   // ros::service::waitForService("servicio_roberto");// Se espera hasta que el servicio esté activo. Equivalente a srvc.waitForExistence();
    if(srvc.call(srvmsg)){ //se llama al servicio y queda bloqueado hasta obtener respuesta. call es una función que devuelve un bool
	/*Una vez que la función call termina, podríamos acceder al contenido del mensaje (en este caso Empty no tiene nada)
	 * a través de srvmsg.response
	 * Recordad que en el lado del servidor este mensaje se procesa como una referencia y se modifica desde el lado del servidor
	 * por lo que al volver al lado del cliente las modificaciones persisten (paso por referencia significa que se pasa el mismo objeto)
	 */
        ROS_INFO("Todo ok");
        return 0;
    }
    else{
        ROS_INFO("Algo ha fallado");
        return 1;
    }


}
