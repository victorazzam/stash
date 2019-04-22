#include <stdio.h>

int main() {
  for (int a = 255; a >= 0; a--) {
    fprintf(stderr, "%d\n", a);
    for (int b = 255; b >= 0; b--) {
      for (int c = 255; c >= 0; c--) {
        for (int d = 255; d >= 0; d--) {
          printf("%d.%d.%d.%d\n", a, b, c, d);
        }
      }
    }
  }
}
