#include <sourcemod>
#include <smtest>

public OnStartTests() {
    SMISNT(1, 2, "1 != 2");
    SMIS(5, 5, "5 == 5");
    SMIS(1+5, 6, "1+5 == 6");

    SMISNT(1.0, 5.0, "1.0 != 5.0");
    SMIS(2.0, 2.0, "2.0 == 2.0");
    SMIS(6.789, 6.789, "6.789 == 6.789");
    SMISNT(5.1, 5.0999, "5.1 != 5.0999");
}
