#include <stdio.h>
#include <unistd.h>

char *msga = "Allow";
char *msgb = "Deny";

void allow() {
    printf("%s\n", msga);
}

void deny() {
    printf("%s\n", msgb);
}

int main(int argc, char **argv) {
    deny();
    int runExternal = 0;
    if (runExternal) {
        char* lsargs[] = {"ls", "-l", NULL};
        execvp("ls", lsargs);
    }
}
