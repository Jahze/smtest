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

    // No test name
    SMIS(100,100);

    SMIS(INVALID_HANDLE, 8.9, "INVALID_HANDLE == 8.9 (this should fail)")
    SMIS(6, 6.0, "6 == 6.0 (this should fail)");
    SMIS(true, false, "true == false (this should fail)");
}
