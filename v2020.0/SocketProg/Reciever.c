#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
int x[1000];
#define MAX_STR1_LEN 100
#define MAX_STR2_LEN 100


unsigned int  lcs(const char *str1, const char *str2, int str1_len, int str2_len)
{
    // Table where lenght[i][j] denotes length of
    // Longest common substring between str1[0...i] & str2[0...j]
     
   int k;
   int length[MAX_STR1_LEN][MAX_STR2_LEN];
   unsigned int i, j, lar_i = 0, max_len = 0;

   /* Check if inputs are valid */
   if(str1 == NULL || str2 == NULL)
   return 0;
   if(str1_len <= 0 || str2_len <=0 )
   {
    printf(" Invalid Lenghts %d %d", str1_len, str2_len);
    return 0;
   }

   /* Initialize the table */
   for(i = 0; i < MAX_STR1_LEN; i++)
   {
    for(j = 0; j < MAX_STR2_LEN; j++)
    length[i][j] = 0;
   }

  for(i = 0; i < str1_len; i++)
  {
    for(j = 0; j < str2_len; j++)
    {
    if(str1[i] == str2[j])
    {
   if(i == 0 || j == 0)
    {
     length[i][j] = 1;
    }
   else
   {
   length[i][j] = length[i-1][j-1] + 1;
   }

  /*
  max_len holds lenght of LCS found so far
  lar_i is the last character of the LCS of size max_len
  */
  if( length[i][j] > max_len)
  {
  max_len = length[i][j];
  lar_i = i;
  }
 }
}
   }

  printf("Longest Substring:");
  /* Print the longest Substring */
  j = 0;
  for(i = lar_i - max_len + 1; j < max_len; i++,j++)
  {
  printf("%c",str1[i]);
  strcpy(x,str1);
  }
  printf("\n");
//  printf("%s",x);

 return max_len;

 }




int main()
{
        int sock, sender_fd, bytes_recieved , true = 1;
        int  R_PORT;
        char send_data [1024] , recv_data[1024],RecieverPORT[1024];
        char username[1024],password[1024],Recievername[1024],RecieverIP[100];
        char buf[1000],str1[1000],str2[1000];
        int i,l;
        struct sockaddr_in server_addr,client_addr,Reciever_addr;
        int sin_size;
        char ch[100];
        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
            perror("Socket");
            exit(1);
        }

        if (setsockopt(sock,SOL_SOCKET,SO_REUSEADDR,&true,sizeof(int)) == -1) {
            perror("Setsockopt");
            exit(1);
        }

        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(57296);
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

         
          printf("reciever waiting on port 57296");
          fflush(stdout);

          sin_size = sizeof(struct sockaddr_in);
          sender_fd = accept(sock, (struct sockaddr *)&client_addr,&sin_size);
          printf("\n  Got a connection from (%s , %d)",inet_ntoa(client_addr.sin_addr),ntohs(client_addr.sin_port));
          bytes_recieved = recv(sender_fd,recv_data,1024,0);
          recv_data[bytes_recieved] = '\0';
          printf("%s",recv_data);
          while(1)
          {        strcpy(buf,"");
                   strcpy(x,"");
                   i=0;
                   strcpy(str1,"");
                   strcpy(str2,"");
                   bytes_recieved = recv(sender_fd,recv_data,1024,0);
                   recv_data[bytes_recieved] = '\0';
                   if((strcmp(recv_data , "q") == 0) || (strcmp(recv_data , "Q") == 0))
                   {
                     close(sock);
                     exit(1);
                   }
                 
                  while(1)
                   {
                    i++;
                    bytes_recieved = recv(sender_fd,recv_data,1024,0);
                    recv_data[bytes_recieved] = '\0';
                    strcpy(ch,"eom");
                    if(strcmp(recv_data ,ch) == 0 )
                    {
                        send(sender_fd,str2,strlen(str2),0);
                        break;
                    }
                    else
                    {
                    strcat(buf,recv_data);
                    strcat(buf,"\n");
                    strcpy(str1,recv_data);
                    if(i==1)
                    strcpy(str2,str1);
                                    
                    l= lcs(str1,str2,strlen(str1),strlen(str2));
                    
                    strcpy(str2,x);
                     
                   // printf("%s",recv_data);
                    fflush(stdout);
                   }
                 }
                    if (buf!= NULL)
                    {
			//printf("----- Waiting for Multicasted message ----- \n");
			printf("\n Received multicast message ==> %s \n", buf);
		     }

                   }
            
      
      return 0;
}





