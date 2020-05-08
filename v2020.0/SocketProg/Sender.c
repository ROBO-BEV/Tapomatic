#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>


int main(int argc,char *argv[])

{

        int sock, bytes_recieved;  
        int RelayserverPORT;
        char send_data[1024],recv_data[1024],username[1024],password[1024];
        char Recievername[1024],RecieverPORT[1024];
        
        struct sockaddr_in  Relayserver_addr;  

        //host = gethostbyname("127.0.0.1");

        if(argc != 3)
        {
        printf("usage: RelayserverIP RelayserverPORT(5000+(4 BY 4)) \n ");
        exit(1);
        }       

        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
            perror("Socket");
            exit(1);
       }

        Relayserver_addr.sin_family = AF_INET;     
        RelayserverPORT=atoi(argv[2]);
        Relayserver_addr.sin_port = htons(RelayserverPORT);   
        
        inet_addr(argv[1],&Relayserver_addr.sin_addr.s_addr);
        bzero(&(Relayserver_addr.sin_zero),8); 

        if (connect(sock, (struct sockaddr *)&Relayserver_addr,
                    sizeof(struct sockaddr)) == -1) 
        {
            perror("Connect");
            exit(1);
        }
         
        printf("Welcome to Message Relay System \n");
 while(1)
{
        printf("\n Enter your username: \n");
        gets(username);
        send(sock,username,strlen(username),0);
        
        bytes_recieved=recv(sock,recv_data,1024,0);
        recv_data[bytes_recieved] = '\0';
        printf("\n %s " , recv_data);
        gets(password);
        send(sock,password,strlen(password),0);

        bytes_recieved=recv(sock,recv_data,1024,0);
        recv_data[bytes_recieved] = '\0';
       // printf("\n %s " , recv_data);
	if(strcmp(recv_data,"valid")==0)
        {
        printf("congratualtions \n");
        break;
        }
        else
       { 
        printf("you enterd wrong username or password");
        continue;
       }
}

 while(1)
{
        printf("\n Enter  Reciever name that you want to connect : \n");
        gets(Recievername);
        send(sock,Recievername,strlen(Recievername),0);

        bytes_recieved=recv(sock,recv_data,1024,0);
        recv_data[bytes_recieved] = '\0';
        printf("\n %s " , recv_data);
        gets(RecieverPORT);
        send(sock,RecieverPORT,strlen(RecieverPORT),0);

        bytes_recieved=recv(sock,recv_data,1024,0);
        recv_data[bytes_recieved] = '\0';
       // printf("\n %s " , recv_data);
        if(strcmp(recv_data,"valid")==0)
        {
        printf("congratualtions \n");
        break;
        }
        else
       {
        printf("you enterd wrong Recievername or port");
        continue;
       }
}


       while(1)
        {
        
             bytes_recieved=recv(sock,recv_data,1024,0);
             recv_data[bytes_recieved] = '\0';
             printf("\n %s \n" , recv_data);
             gets(send_data);
             if((strcmp(send_data , "q") == 0)|| ( strcmp(send_data , "Q") == 0))
             {
              send(sock,send_data,strlen(send_data), 0);
              close(sock);
              exit(1); 
             }
             while(1)
             {
                 printf("\n Enter data(press EOM or eom to indicate end of message): \n");
                 gets(send_data);
                 if(strcmp(send_data ,"eom") == 0)
                 {
                 send(sock,send_data,strlen(send_data), 0);
                 break;
                 }
                 else
                 {
                 send(sock,send_data,strlen(send_data), 0);
                 }
             }
        
             bytes_recieved=recv(sock,recv_data,1024,0);
             recv_data[bytes_recieved] = '\0';
             printf("\nLength of Longest common substring from Receiver = %s " , recv_data);
        } 
 
return 0;
}
