#include <err.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  char buf[32] = "";

  system("/bin/echo 'addr?'");
  read(STDIN_FILENO, buf, sizeof(buf));
  char *addr = (char*) strtoull(buf, NULL, 16);

  system("/bin/echo 'len?'");
  read(STDIN_FILENO, buf, sizeof(buf));
  size_t len = strtoull(buf, NULL, 16);

  system("/bin/echo 'data?'");
  read(STDIN_FILENO, addr, len);

  return 0;
}
