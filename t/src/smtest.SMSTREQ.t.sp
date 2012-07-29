#include <sourcemod>
#include <smtest>

public OnStartTests() {
    SMSTREQ("TEST", "TEST", "\"TEST\" == \"TEST\"");
    SMSTREQ("test", "TEST", "\"TEST\" == \"test\" (this should fail)");
    SMSTREQ("one", "one", "\"one\" == \"one\"");
}
