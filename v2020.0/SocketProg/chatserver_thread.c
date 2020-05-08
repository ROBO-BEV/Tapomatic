/*
 ** server.c -- a stream socket server demo
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/wait.h>
#include <signal.h>
#include <pthread.h>

#define PORT "4444"       // the port users will be connecting to
#define MAXDATASIZE 500   // max number of bytes we can get at once 
#define NUM_THREADS 50    //max number of threads to contact with clients
#define BACKLOG 10	      // how many pending connections queue will hold

struct mystructure
{
	int socketfd;
	int new_fd1;
};


 
	
	        int client_fd[50];      //new file descriptor for communication with client 
	
	        int client_count=0;     //no of clients at present connected to server




	
	
void *chat(void *info)
{
	//thread for new connection
	char recv_data[MAXDATASIZE],send_data[MAXDATASIZE];
	int  numbytes;
	int  fd,nfd;
	int  i;
	
	struct mystructure *sockinfo;
	sockinfo=(struct mystructure *) info;
	fd=sockinfo->socketfd;
	nfd=sockinfo->new_fd1;
	
	
	
	
	while (1)
	{
		printf("\n SEND (q or Q to quit) : ");
		gets(send_data);
		
		if (strcmp(send_data , "q") == 0 || strcmp(send_data , "Q") == 0)
		{
			send(nfd, send_data,strlen(send_data), 0); 
			close(nfd);
			break;
		}
		
		else
			send(nfd, send_data,strlen(send_data), 0);  
		
		if((numbytes = recv(nfd,recv_data,MAXDATASIZE-1,0))==-1)
         {
         perror("recv");
         exit(1);
		 }
		
         recv_data[numbytes] = '\0';
		
		
		if (strcmp(recv_data , "q") == 0 || strcmp(recv_data , "Q") == 0)
		{
			close(nfd);
			break;
		}
		
		
		else 
			printf("\n RECIEVED DATA = %s \n" , recv_data);
		
		for(i=1;i<=client_count;i++)
		{
			send(client_fd[i], recv_data,strlen(recv_data), 0);
		}
		
		    fflush(stdout);
	}
	

pthread_exit(NULL);


}




// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}
	
	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}




int main(void)
{
	int sockfd, new_fd;             // listen on sock_fd, new connection on new_fd
	struct addrinfo hints, *servinfo, *p;
	struct sockaddr_storage their_addr;  // connector's address information
	struct mystructure ms;
	socklen_t sin_size;
	int yes=1;
	char s[INET6_ADDRSTRLEN];
	int rv;
	
	pthread_t threads;
	
	int rc;
	
	
	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE; // use my IP
	
	if ((rv = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}
	
	// loop through all the results and bind to the first we can
	for(p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
							 p->ai_protocol)) == -1) {
			perror("server: socket");
			continue;
		}
		
		if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes,
					   sizeof(int)) == -1) {
			perror("setsockopt");
			exit(1);
		}
		
		if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("server: bind");
			continue;
		}
		
		break;
	}
	
	if (p == NULL)  {
		fprintf(stderr, "server: failed to bind\n");
		return 2;
	}
	
	freeaddrinfo(servinfo); // all done with this structure
	
	if (listen(sockfd, BACKLOG) == -1) {
		perror("listen");
		exit(1);
	}
	
		
	printf("server: waiting for connections...\n");
	
	
	
	
	//while
	
	while(1) {  // main accept() loop
		
		
		
		sin_size = sizeof their_addr;
		new_fd   = accept(sockfd, (struct sockaddr *)&their_addr, &sin_size);
		
		
		    if (new_fd == -1)  {
			                        perror("accept");
			                        continue;
						        }
		
		inet_ntop(their_addr.ss_family,
				  get_in_addr((struct sockaddr *)&their_addr),
				  s, sizeof s);
		printf("server: got connection from %s\n", s);
		
		
		
		client_count=client_count+1;
		
		client_fd[client_count]=new_fd;
		
		
		
		
		
		ms.socketfd=sockfd;
		ms.new_fd1=new_fd;
		
		
		
		rc = pthread_create(&threads, NULL, chat, (void *) &ms);
		if (rc){
			printf("ERROR; return code from pthread_create() is %d\n", rc);
			exit(-1);
		}
		
		
		
		
	}  //while ended
	
	
	
	
	
	close(sockfd);
		pthread_exit(NULL);
	
		return 0;
}

