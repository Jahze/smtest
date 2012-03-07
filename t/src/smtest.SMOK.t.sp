#pragma semicolon 1

#include <sourcemod>
#include <smtest>

public OnStartTests() {
    SMOK(true, "true is true");
    SMOK( !SMOK(false, "false is true"), "it's true that false is not true" );
}

