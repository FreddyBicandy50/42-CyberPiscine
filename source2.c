#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char input[64];
    char result[16];
    int i = 2, j = 1;

    printf("Please enter key: ");
    scanf("%23s", input);


    if (input[0] != '0' || input[1] != '0') {
        puts("Nope.");
        return 1;
    }

    result[0] = 100;
    while (input[i]) {
        char tmp[4] = {0};
        strncpy(tmp, &input[i], 3);
        result[j++] = (char)atoi(tmp);
        i += 3;
    }

    result[j] = '\0';

    if (strcmp(result, "delabere") == 0)
        puts("Good job.");
    else
        puts("Nope.");

    return 0;
}
