native bool:SMOK( bool:value, const String:name[]="" );
native bool:SMIS( any:value1, any:value2, const String:name[]="" );
native bool:SMISNT( any:value1, any:value2, const String:name[]="" );

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
}

