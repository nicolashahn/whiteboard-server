#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define BUF_SIZE 500

int main():
    HOST := "127.0.0.1"
    PORT := "65432"

    sockfd := socket(AF_INET, SOCK_STREAM, 0)
    struct addrinfo hints;
    struct addrinfo *result, *rp;
    char buf[BUF_SIZE]

    memset(&hints, 0, sizeof(struct addrinfo));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = 0;
    hints.ai_protocol = 0;

    s := getaddrinfo(HOST, PORT, &hints, &result)
    if s != 0:
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
        exit(EXIT_FAILURE);

    bytes_read := 0
    while true:
        if bytes_read == 0:
            connect(sockfd, result->ai_addr, result->ai_addrlen)
        message := "{\"a\":1}\n"
        write(sockfd, message, strlen(message))
        bytes_read = read(sockfd, buf, BUF_SIZE-1)
        buf[bytes_read] = 0
        print bytes_read, buf
        memset(buf, 0, BUF_SIZE)
        sleep(1)

