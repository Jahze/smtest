/**
 * Checks if value is true and adds the result to the test output.
 *
 * @param value1
 * @param value2
 * @param name      test name
 * @return bool     true if the test passed
 */
native bool:SMOK(bool:value, const String:name[]="", ...);

/**
 * Checks that value1 is equal to value2 and adds the result to the test output.
 *
 * @param value1
 * @param value2
 * @param name      test name
 * @return bool     true if the test passed
 */
native bool:SMIS(any:value1, any:value2, const String:name[]="", ...);

/**
 * Checks that value1 is not equal to value2 and adds the result to the test output.
 *
 * @param value1
 * @param value2
 * @param name      test name
 * @return bool     true if the test passed
 */
native bool:SMISNT(any:value1, any:value2, const String:name[]="", ...);

/**
 * Checks that two strings are equal and adds the result to the test output.
 *
 * @param str1
 * @param str2
 * @param name      test name
 * @return bool     true if the test passed
 */
native bool:SMSTREQ(const String:str1[], const String:str2[], const String:name[]="", ...);

/**
 * Called when the "sm_test_run" command is run.
 *
 * @note Test plugins should use this to kick of their tests.
 * @note When all the tests have finished "sm_test_output" can be used to retrieve a break-down of which tests passed. 
 * @noreturn
 */
forward OnStartTests();

public SharedPlugin:__pl_smtest = {
    name = "smtest",
    file = "smtest.smx",
#if defined REQUIRE_PLUGIN
    required = 1,
#else
    required = 0,
#endif
};

public __pl_smtest_SetNTVOptional() {
    MarkNativeAsOptional("SMIS");
    MarkNativeAsOptional("SMISNT");
    MarkNativeAsOptional("SMOK");
    MarkNativeAsOptional("SMSTREQ");
}

