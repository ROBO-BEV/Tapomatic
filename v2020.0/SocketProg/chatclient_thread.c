/*
 ** client.c -- a stream socket client demo
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>

#include <arpa/inet.h>

#define PORT "4444" // the port client will be connecting to 

#define MAXDATASIZE 500 // max number of bytes we can get at once 

// get sockaddr, IPv4 or IPv6:
void *get_in_addr(struct sockaddr *sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}
	
	return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(int argc, char *argv[])
{
	int sockfd, numbytes;  
	char send_data[MAXDATASIZE],recv_data[MAXDATASIZE];
	struct addrinfo hints, *servinfo, *p;
	int rv;
	char s[INET6_ADDRSTRLEN];
	
	if (argc != 2) {
	    fprintf(stderr,"usage: client hostname\n");
	    exit(1);
	}
	
	memset(&hints, 0, sizeof hints);
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	
	if ((rv = getaddrinfo(argv[1], PORT, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}
	
	// loop through all the results and connect to the first we can
	for(p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype,
							 p->ai_protocol)) == -1) {
			perror("client: socket");
			continue;
		}
		
		if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("client: connect");
			continue;
		}
		
		break;
	}
	
	if (p == NULL) {
		fprintf(stderr, "client: failed to connect\n");
		return 2;
	}
	
	inet_ntop(p->ai_family, get_in_addr((struct sockaddr *)p->ai_addr),
			  s, sizeof s);
	printf("client: connecting to %s\n", s);
	
	freeaddrinfo(servinfo); // all done with this structure
	
	
	
	
	
	
	
	 while(1)
	 {
	 
	 numbytes=recv(sockfd,recv_data,MAXDATASIZE-1,0);
	 recv_data[numbytes] = '\0';
	 
	 if (strcmp(recv_data , "q") == 0 || strcmp(recv_data , "Q") == 0)
	 {
	 close(sockfd);
	 break;
	 }
	 
	 else
	 printf("\nRecieved data = %s " , recv_data);
	 
	 printf("\nSEND (q or Q to quit) : ");
	 gets(send_data);
	 
	 if (strcmp(send_data , "q") != 0 && strcmp(send_data , "Q") != 0)
	 send(sockfd,send_data,strlen(send_data), 0); 
	 
	 else
	 {
	 send(sockfd,send_data,strlen(send_data), 0);   
	 close(sockfd);
	 break;
	 }
	 
	 }   
	 
	
	if ((numbytes = recv(sockfd, recv_data, MAXDATASIZE-1, 0)) == -1) {
	    perror("recv");
	    exit(1);
	}
	
	
	/*recv_data[numbytes] = '\0';
	
	printf("client: received '%s'\n",recv_dat);
	
	
	send( sockfd,"i am client1 thank you for sending hellow world ", strlen("i am client1 thank you for sending hellow world "), 0);
	
	
	close(sockfd);*/
	
	
	return 0;
}


