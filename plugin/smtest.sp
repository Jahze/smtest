#pragma semicolon 1

#include <sourcemod>

#define MAX_TEST_NAME_LENGTH    128

new Handle:testResults;
new Handle:testNames;

new Handle:fwd_startTests;

public Plugin:myinfo = {
    name = "SourceMod Testing Framework",
    author = "Jahze",
    description = "A testing framwork for sourcemod plugins",
    version = "1.0"
}

public APLRes:AskPluginLoad2(Handle:myself, bool:late, String:error[], err_max) {
    CreateNative("SMIS", _native_SMIS);
    CreateNative("SMISNT", _native_SMISNT);
    CreateNative("SMOK", _native_SMOK);

    RegPluginLibrary("smtest");
    return APLRes_Success;
}

public OnPluginStart() {
    RegConsoleCmd("sm_test_run", Cmd_StartTests);
    RegConsoleCmd("sm_test_output", Cmd_TestOutput);

    fwd_startTests = CreateGlobalForward("OnStartTests", ET_Ignore);

    testResults = CreateArray();
    testNames = CreateArray(MAX_TEST_NAME_LENGTH);
}

public _native_SMOK(Handle:plugin, numparams) {
    new bool:val = GetNativeCell(1);
    new len;

    GetNativeStringLength(2, len);

    new written;
    decl String:name[MAX_TEST_NAME_LENGTH];
    FormatNativeString(0, 2, 3, sizeof(name), written, name);

    return _:SMOK(val, name);
}

public _native_SMIS(Handle:plugin, numparams) {
    new any:v1 = GetNativeCell(1);
    new any:v2 = GetNativeCell(2);
    new len;

    GetNativeStringLength(3, len);

    new written;
    decl String:name[MAX_TEST_NAME_LENGTH];
    FormatNativeString(0, 3, 4, sizeof(name), written, name);

    return _:SMIS(v1, v2, true, name);
}

public _native_SMISNT(Handle:plugin, numparams) {
    new any:v1 = GetNativeCell(1);
    new any:v2 = GetNativeCell(2);
    new len;

    GetNativeStringLength(3, len);

    new written;
    decl String:name[MAX_TEST_NAME_LENGTH];
    FormatNativeString(0, 3, 4, sizeof(name), written, name);

    return _:SMIS(v1, v2, false, name);
}

bool:SMIS(any:value1, any:value2, bool:expect, const String:name[]="") {
    PushArrayString(testNames, name);
    PushArrayCell(testResults, (value1==value2) == expect);
    return (value1==value2) == expect;
}

bool:SMOK(bool:value, const String:name[]="") {
    PushArrayString(testNames, name);
    PushArrayCell(testResults, value);
    return value;
}

static TestOutput(client) {
    new numTests = GetArraySize(testNames);
    new passed = 0;

    for ( new i = 0; i < GetArraySize(testNames); i++ ) {
        decl String:name[128], String:c[1];
        GetArrayString(testNames, i, name, sizeof(name));
        new result = GetArrayCell(testResults, i);
        
        if ( result ) {
            c[0] = 'Y';
            passed++;
        }
        else {
            c[0] = 'N';
        }

        ReplyToCommand(client,"%c.......................%s", c[0], name);
    }

    ReplyToCommand(client, "%d / %d tests passed", passed, numTests);
}

public Action:Cmd_TestOutput(client, args) {
    TestOutput(client);
}

public Action:Cmd_StartTests(client, args) {
    new result;
    Call_StartForward(fwd_startTests);
    Call_Finish(result);
}

