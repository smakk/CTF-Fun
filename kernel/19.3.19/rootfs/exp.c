#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/stat.h>

int main(){
	int fd1,fd2;
	fd1 = open("/dev/babydev",O_RDWR);	
	fd2 = open("/dev/babydev",O_RDWR);
	
	ioctl(fd1,0x10001,168);
	close(fd1);
	if(fork()>0){
		wait(NULL);
	}else{
		char buffer[30];
		write(fd2,buffer,28);
	}
	close(fd2);
	return 0;
}
