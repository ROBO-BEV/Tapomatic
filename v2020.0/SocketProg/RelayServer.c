#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include<netdb.h>

int main()
{
        int sock,rsock, sender_fd,reciever_fd, bytes_recieved , true = 1;
        int  R_PORT;  
        char send_data [1024] , recv_data[1024],RecieverPORT[1024]; 
        char username[1024],password[1024],Recievername[1024],RecieverIP[100];     

        struct sockaddr_in server_addr,client_addr,Reciever_addr;    
        int sin_size;
        
        //creating socket
        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
            perror("Socket");
            exit(1);
        }
       
        
        if (setsockopt(sock,SOL_SOCKET,SO_REUSEADDR,&true,sizeof(int)) == -1) {
            perror("Setsockopt");
            exit(1);
        }
        
        //binding and filling address by hands
        server_addr.sin_family = AF_INET;         
        server_addr.sin_port = htons(57295);     
        server_addr.sin_addr.s_addr = INADDR_ANY; 
        bzero(&(server_addr.sin_zero),8); 

        if (bind(sock, (struct sockaddr *)&server_addr, sizeof(struct sockaddr))
                                                                       == -1) {
            perror("Unable to bind");
            exit(1);
        }

        if (listen(sock, 5) == -1) {
            perror("Listen");
            exit(1);
        }
		
	printf("\n Relayserver waiting on  port 57295");
        fflush(stdout);


  while(1) {  

     sin_size = sizeof(struct sockaddr_in);
     sender_fd = accept(sock, (struct sockaddr *)&client_addr,&sin_size); //file descriptor used for conatcting with SENDER
     printf("\n  Got Sender connection from (%s , %d)",inet_ntoa(client_addr.sin_addr),ntohs(client_addr.sin_port));
     while(1){  //loop for user name and pwd authentication
        //getting username 
        bytes_recieved=recv(sender_fd,username,1024,0);
        username[bytes_recieved]='\0';          
        send(sender_fd,"Enter your password:",strlen("Enter your password:"),0);
        
        //getting password
        bytes_recieved=recv(sender_fd,password,1024,0);
        password[bytes_recieved]='\0';
    
        //authentication 
        if((strcmp(username,"anna")==0 && strcmp(password,"a86H6T0c")==0) || (strcmp(username,"barbara")==0 && strcmp(password,"G6M7p8az")==0) 
        || (strcmp(username,"cathie")==0 && strcmp(password,"Pd82bG57")==0) || (strcmp(username,"dohas")==0 && strcmp(password,"jO79bNs1")==0) 
        || (strcmp(username,"eli")==0 && strcmp(password,"uCh781fY")==0) || (strcmp(username,"farah")==0 && strcmp(password,"Cfw61RqV")==0) 
        || (strcmp(username,"shaz")==0 && strcmp(password,"Kuz07YLv")==0)||(strcmp(username,"murali")==0 && strcmp(password,"murali1234")==0))
        { 
           send(sender_fd,"valid",strlen("valid"),0);
            break;
         }else{
            send(sender_fd,"not valid user",strlen("not valid user"),0);
         }
            
      } 

     while(1){  //loop for retrieving receiver RECEIVER IP
         //getting Reciever name
         bytes_recieved=recv(sender_fd,Recievername,1024,0);
         Recievername[bytes_recieved]='\0';
         send(sender_fd,"Enter RecieverPORT:",strlen("Enter RecieverPORT:"),0);
         
         //getting Receiver port number 
         bytes_recieved=recv(sender_fd,RecieverPORT,1024,0);
         RecieverPORT[bytes_recieved]='\0';
         
         //Validating receiver username and port number 
         if((strcmp(Recievername,"gpel1.cs.ou.edu")==0)|| (strcmp(Recievername,"gpel2.cs.ou.edu")==0) || (strcmp(Recievername,"gpel3.cs.ou.edu")==0)
         || (strcmp(Recievername,"gpel4.cs.ou.edu")==0) || (strcmp(Recievername,"gpel5.cs.ou.edu")==0) || (strcmp(Recievername,"gpel6.cs.ou.edu")==0)
         || (strcmp(Recievername,"murali.ou.edu")==0))
         {
            send(sender_fd,"valid",strlen("valid"),0);
            
         }else{
            send(sender_fd,"You Enter a Invalid Recievername and PORT ",strlen("Enter valid Recievername and PORT"),0);
            continue;
         }
         if(strcmp(Recievername,"murali.ou.edu")==0)
         strcpy(RecieverIP,"192.168.2.7");
         else if(strcmp(Recievername,"gpel1.cs.ou.edu")==0)
         strcpy(RecieverIP,"129.15.78.11");
         else if(strcmp(Recievername,"gpel2.cs.ou.edu")==0)
         strcpy(RecieverIP,"129.15.78.12");
         else if(strcmp(Recievername,"gpel3.cs.ou.edu")==0)
         strcpy(RecieverIP,"129.15.78.13");
         else if(strcmp(Recievername,"gpel4.cs.ou.edu")==0)
         strcpy(RecieverIP,"129.15.78.14");
         else if(strcmp(Recievername,"gpel5.cs.ou.edu")==0)
         strcpy(RecieverIP,"129.15.78.15");
         else if(strcmp(Recievername,"gpel6.cs.ou.edu")==0)
         strcpy(RecieverIP,"129.15.78.16");
         else if(strcmp(Recievername,"gpel7.cs.ou.edu")==0)
         strcpy(RecieverIP,"129.15.78.17");
         break;
     }
        strcpy(RecieverIP,"192.168.2.7");   
     //creating a new socket for maintaining connections with RECEIVER
     if ((rsock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
       perror("Socket");
       exit(1);
     }
     if (setsockopt(rsock,SOL_SOCKET,SO_REUSEADDR,&true,sizeof(int)) == -1) {
       perror("Setsockopt");
       exit(1);
     }
    strcpy(RecieverPORT,"57296");
    Reciever_addr.sin_family = AF_INET;
    R_PORT=atoi(RecieverPORT);
    Reciever_addr.sin_port = htons(R_PORT);
    Reciever_addr.sin_addr.s_addr=inet_addr(RecieverIP);
    bzero(&(Reciever_addr.sin_zero),8);
    if (connect(rsock, (struct sockaddr *)&Reciever_addr,sizeof(struct sockaddr)) == -1){
      perror("Connect");
      printf("\n sorry");
      exit(1);
    } 
    send(rsock,"hai this is relayserver",strlen("hai this is relayserver"),0);
    
    while (1)
    {
         send(sender_fd,"Enter q or Q to exit ",strlen("Enter q or Q to exit"), 0); 
       
         bytes_recieved = recv(sender_fd,recv_data,1024,0);
         recv_data[bytes_recieved] = '\0';
         if (strcmp(recv_data , "q") == 0 || strcmp(recv_data , "Q") == 0)
         {
         send(rsock,recv_data,strlen(recv_data),0);
         break;
         }
        // send(sender_fd,"Enter Message to Receiver",strlen("Enter Message to Receiver"), 0);
         while(1)
         {  
            bytes_recieved = recv(sender_fd,recv_data,1024,0);
            recv_data[bytes_recieved] = '\0';
            if(strcmp(recv_data , "eom") == 0)
            {
               send(rsock,recv_data,strlen(recv_data),0);
               break;
            }
            else
            { 
               send(rsock,recv_data,strlen(recv_data),0);
               fflush(stdout);
            } 
          }
         
               
               bytes_recieved = recv(rsock,recv_data,1024,0);
               recv_data[bytes_recieved] = '\0';
               send(sender_fd,recv_data,strlen(recv_data),0);
    }

  
     close(sender_fd);
     close(rsock);
}

close(sock);
return 0;
} 
          
