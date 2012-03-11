import config
import Logger
import Server
import TestParser

import optparse
import os
import sys

def RunTest( file, server ):
    parser = TestParser.TestParser(file, server)
    t = parser.Parse()

    if parser.HasError():
        print(parser.GetError())
        return None

    return t


parser = optparse.OptionParser()
parser.add_option("-l", "--log", dest="log", help="Display full log on STDERR", default=False, action="store_true")
parser.add_option("-p", "--allow-players", dest="allow_players", help="Allow tests to run whilst players are on the server", default=False, action="store_true")
parser.add_option("-c", "--config", dest="config_file", help="Location of config.ini", default="config.ini", action="store", type="string")
(options, args) = parser.parse_args()

Logger.Logger.Enable(options.log)

config.read_config(options.config_file)

if not len(args):
    print("No test files supplied")
else:
    server = Server.Server(
        config.config_value('RCON_HOST'),
        config.config_value('RCON_PORT'),
        config.config_value('RCON_PASS')
    );

    if not options.allow_players and server.HasPlayers():
        print("Players are on the server:")
        print(server.Status())
        os._exit(0)

    for i in args:
        t = RunTest(i, server)

        if t == None:
            continue

        if t.Prepare():
            t.Run()

        t.Cleanup() 
