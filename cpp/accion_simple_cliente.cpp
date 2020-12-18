#include<ros/ros.h> //Ros c++
/*Nos permite interactuar con acciones desde el lado del cliente
su espacio de nombre (namespace) es actionlib, es necesario para acceder a
sus métodos
simple_action_client es la librería usada para implementar clientes simples
*/
#include<actionlib/client/simple_action_client.h>

#include<actionlib/TestAction.h> //Tipo de los mensajes de accion empleados

//Se llama al finalizar la acción
void doneCB(const actionlib::SimpleClientGoalState &state,const actionlib::TestResultConstPtr &result){
    ROS_INFO("state result %s", state.toString().c_str());
    ROS_INFO("The action was completed");
    ros::shutdown();

}
//Se llama al activarse la acción (una sola vez)
void activeCB()
{
    ROS_INFO("Starting to do funny things");
}

//Se llama cada vez que la accion nos informa de su proceso
void feedbackCB(const actionlib::TestFeedbackConstPtr & feedback)
{

   ROS_INFO("Doing funny things feedback");  
}
int main(int argc, char ** argv)
{
    ros::init(argc, argv, "action_client_name");//incializamos el nodo. El nombre se va a reempleazar en el launch
    //En este caso no necesitamos el NodeHandle porque las acciones se gestionan a través del actionlib

    /*El cliente para las acciones es una clase dentro de actionlib. Está implementada a través de una plantilla 
    (Las clases también tiene plantillas) por lo que es necesario especificar el tipo de acciones que va a gestionar
    Para saber el tipo de mensaje de acción que se usa es necesario consultar los topics creados para las acciones
    El constructor de la clase tiene 2 argumentos: 1) el nombre de la acción,2) un booleano que si es true automáticamente
    crea un hilo para el cliente y así no necesitamos gestionarlo nosotros 
    */
    std::string name_action_server="serv_acc_basico";
    
    actionlib::SimpleActionClient<actionlib::TestAction> actionclient(name_action_server, true);
    ROS_INFO("Waiting for the action server: %s", name_action_server.c_str());
    actionclient.waitForServer();//Espera hasta que el servidor de acciones esté disponible
    ros::Rate loop_rate(1);// para que el bucle vaya a 1 hz
    actionlib::TestActionGoal goalmsg;//Tipo de mensaje que necesitamos para iniciar la acción
    goalmsg.goal.goal=10;//consultar rosmsg info actionlib/TestActionGoal
    /*Llamamos a la accion. Solo el primer argumento es obligatorio
     actionclient.sendGoal(goalmsg.goal);
     */
    actionclient.sendGoal(goalmsg.goal,&doneCB,&activeCB,&feedbackCB);
    //actionclient.waitForResult();//bloquea hasta que la acción finalice. Sería como ejecutar un servicio

    actionlib::SimpleClientGoalState status=actionclient.getState(); //recogemos el estado actual de la acción
   /* int cont=1;
   
    while(status==actionlib::SimpleClientGoalState::ACTIVE or status==actionlib::SimpleClientGoalState::PENDING)
    {
        //Hacemos cosas mientras la acción aun se está ejecutando o está pendiente de empezar a ejecutarse
        ROS_INFO("Doing things....%i sec",cont);
        cont++;
        loop_rate.sleep();
        status=actionclient.getState();//recogemos el estado actual de la acción
        
    }*/

     //Una forma alternativa de hacer con un bucle for todo el proceso
    for(int cont=1;status==actionlib::SimpleClientGoalState::ACTIVE or status==actionlib::SimpleClientGoalState::PENDING;  cont++,loop_rate.sleep(),status=actionclient.getState())
        ROS_INFO("Doing things....%i sec",cont);
   
    return 0;
}
