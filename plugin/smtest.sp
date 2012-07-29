#pragma semicolon 1

#include <sourcemod>

#define MAX_ERROR_MSG_LENGTH            512
#define MAX_VALUE_LENGTH                64
#define MAX_TEST_NAME_LENGTH            128

#define DEFAULT_TEST_OUTPUT_FILENAME    "smtest.txt"

new g_NumTests;
new g_PassedTests;

new Handle:g_FwdStartTests;
new Handle:g_File = INVALID_HANDLE;

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
    CreateNative("SMSTREQ", _native_SMSTREQ);

    RegPluginLibrary("smtest");
    return APLRes_Success;
}

public OnPluginStart() {
    RegServerCmd("sm_test_run", Cmd_StartTests);
    RegServerCmd("sm_test_output", Cmd_TestOutput);

    g_FwdStartTests = CreateGlobalForward("OnStartTests", ET_Ignore);
}

public _native_SMOK(Handle:plugin, numparams) {
    new bool:val = GetNativeCell(1);
    new written;
    decl String:name[MAX_TEST_NAME_LENGTH];
    FormatNativeString(0, 2, 3, sizeof(name), written, name);
    GenerateTestName(name, sizeof(name));

    return _:SMOK(plugin, val, name);
}

public _native_SMIS(Handle:plugin, numparams) {
    new any:v1 = GetNativeCell(1);
    new any:v2 = GetNativeCell(2);
    new tag1 = GetNativeCell(4);
    new tag2 = GetNativeCell(5);

    decl String:name[MAX_TEST_NAME_LENGTH];
    GetNativeString(3, name, sizeof(name)); 
    GenerateTestName(name, sizeof(name));

    return _:SMIS(plugin, v1, v2, tag1, tag2, true, name);
}

public _native_SMISNT(Handle:plugin, numparams) {
    new any:v1 = GetNativeCell(1);
    new any:v2 = GetNativeCell(2);
    new tag1 = GetNativeCell(4);
    new tag2 = GetNativeCell(5);

    decl String:name[MAX_TEST_NAME_LENGTH];
    GetNativeString(3, name, sizeof(name)); 
    GenerateTestName(name, sizeof(name));

    return _:SMIS(plugin, v1, v2, tag1, tag2, false, name);
}

public _native_SMSTREQ(Handle:plugin, numparams) {
    new strlen1;
    GetNativeStringLength(1, strlen1);
    decl String:str1[strlen1+1];
    GetNativeString(1, str1, strlen1+1);

    new strlen2;
    GetNativeStringLength(2, strlen2);
    decl String:str2[strlen2+1];
    GetNativeString(2, str2, strlen2+1);

    new written;
    decl String:name[MAX_TEST_NAME_LENGTH];
    FormatNativeString(0, 3, 4, sizeof(name), written, name);
    GenerateTestName(name, sizeof(name));

    return _:SMSTREQ(plugin, str1, str2, name);
}

bool:SMIS(Handle:plugin, any:value1, any:value2, tag1, tag2, bool:expect, const String:name[]="") {
    new bool:value = (value1==value2) == expect;
    
    decl String:preVal1[MAX_VALUE_LENGTH];
    decl String:sVal1[MAX_VALUE_LENGTH];
    ValueToString(preVal1, sizeof(preVal1), value1, tag1);

    if (! expect)
        Format(sVal1, sizeof(sVal1), "not %s", preVal1);
    else
        strcopy(sVal1, sizeof(sVal1), preVal1);

    decl String:sVal2[MAX_VALUE_LENGTH];
    ValueToString(sVal2, sizeof(sVal2), value2, tag2);

    decl String:error[MAX_ERROR_MSG_LENGTH];
    FormatErrorMessage(error, sizeof(error), plugin, name, sVal1, sVal2);

    TestResult(value, name, error);
    return value;
}

bool:SMOK(Handle:plugin, bool:value, const String:name[]="") {
    decl String:pluginName[PLATFORM_MAX_PATH];
    GetPluginFilename(plugin, pluginName, sizeof(pluginName));

    decl String:error[MAX_ERROR_MSG_LENGTH];
    Format(error, sizeof(error), "#   Failed test '%s'\n#   in %s", name, pluginName);

    TestResult(value, name, error);
    return value;
}

bool:SMSTREQ(Handle:plugin, const String:str1[], const String:str2[], const String:name[]="") {
    new bool:value = StrEqual(str1, str2);

    decl String:error[MAX_ERROR_MSG_LENGTH];
    FormatErrorMessage(error, sizeof(error), plugin, name, str1, str2);

    TestResult(value, name, error);
    return value;
}

// XXX: This function looks a little weird because spcomp on Windows crashes
// in a bunch of weird circumstances when tagof is used. Examples:
//
//  * static function using static var = tagof(Tag:)
//  * if (tag == tagof(Tag:))
//  * case (tagof(Tag:))
ValueToString(String:buffer[], length, any:value, tag) {
    static FloatTag = tagof(Float:);
    static BoolTag = tagof(bool:);
    static HandleTag = tagof(Handle);

    if (tag == FloatTag) {
        Format(buffer, length, "%f", value);
    }
    else if (tag == HandleTag) {
        if (Handle:value == INVALID_HANDLE)
            strcopy(buffer, length, "INVALID_HANDLE");
        else
            Format(buffer, length, "%d", value);
    }
    else if (tag == BoolTag) {
        if (bool:value)
            strcopy(buffer, length, "true");
        else
            strcopy(buffer, length, "false");
    }
    else {
        Format(buffer, length, "%d", value);
    }
}

static GenerateTestName(String:buffer[], length) {
    if (strlen(buffer) == 0)
        Format(buffer, length, "test %d", g_NumTests+1); 
}

static FormatErrorMessage(String:buffer[], length, Handle:plugin, const String:name[], const String:expected[], const String:got[]) {
    decl String:pluginName[PLATFORM_MAX_PATH];
    GetPluginFilename(plugin, pluginName, sizeof(pluginName));
    Format(buffer, length, "#   Failed test '%s'\n#   in %s\n#     expected: %s\n#          got: %s", name, pluginName, expected, got);
}

static TestResult(bool:value, const String:name[], const String:error[]="") {
    WriteFileLine(g_File, "%c.......................%s", value ? 'Y' : 'N', name);

    if (!value && strlen(error))
        WriteFileLine(g_File, error);

    g_NumTests++;
    if (value)
        g_PassedTests++;
}

static PrintNumPassedTests() {
    WriteFileLine(g_File, "%d / %d tests passed", g_PassedTests, g_NumTests);
}

static TestOutput() {
    decl String:path[PLATFORM_MAX_PATH];
    BuildPath(Path_SM, path, sizeof(path), DEFAULT_TEST_OUTPUT_FILENAME);

    new Handle:file = OpenFile(path, "rb");
    if (file == INVALID_HANDLE)
        ThrowNativeError(1, "SMTest unable to open file for reading: %s", path);

    decl String:line[512];
    while (ReadFileLine(file, line, sizeof(line))) {
        new l = strlen(line);
        while (l && (line[l-1] == '\n' || line[l-1] == '\r'))
            line[l-1] = 0;
        PrintToServer(line);
    }

    CloseHandle(file);
}

public Action:Cmd_TestOutput(args) {
    PrintNumPassedTests();

    if (g_File != INVALID_HANDLE)
        CloseHandle(g_File);

    TestOutput();
}

public Action:Cmd_StartTests(args) {
    decl String:path[PLATFORM_MAX_PATH];
    BuildPath(Path_SM, path, sizeof(path), DEFAULT_TEST_OUTPUT_FILENAME);

    if (g_File != INVALID_HANDLE)
        CloseHandle(g_File);

    g_File = OpenFile(path, "wb");
    if (g_File == INVALID_HANDLE)
        ThrowNativeError(1, "SMTest unable to open file for writing: %s", path);

    g_NumTests = 0;
    g_PassedTests = 0;
    new result;
    Call_StartForward(g_FwdStartTests);
    Call_Finish(result);
}

