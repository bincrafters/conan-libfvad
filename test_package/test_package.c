#include <stdlib.h>
#include <fvad.h>

int main() {
    Fvad *vad = fvad_new();
    fvad_set_mode(vad, 2);
    fvad_free(vad);

    return EXIT_SUCCESS;
}