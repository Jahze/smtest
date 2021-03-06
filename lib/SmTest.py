import os
import re
import shutil
import sys
import time

from config import config_value,config_has_value
from ftplib import FTP,all_errors

import CopyFileList
import FtpFileList
import Logger
import SpCompiler

class SmTest:
    SMX_TEMP_DIR = ".smx"

    def __init__( self, n, server ):
        self.server = server
        self.name = n
        self.files = {}
        self.deleteFiles = {}
        self.storedFiles = []
        self.sources = []
        self.smxs = []
        self.commands = []
        self.compiler = SpCompiler.SpCompiler(n)
        self.fileHandler = None

    def AddFile( self, local, remote, delete ):
        self.files[local] = remote
        self.deleteFiles[local] = delete

    def AddSource( self, source ):
        self.sources.append(source)

    def AddCommand( self, command ):
        self.commands.append(command)

    def AddInclude( self, include ):
        self.compiler.AddInclude(include)

    def PrefixLog( self, text ):
        Logger.Logger.Log("[" + self.name + "] " + text)

    def CompileSources( self ):
        for i in self.sources:
            if not self.compiler.Compile(i):
                return False

            outFile = self.compiler.GetLastOutputSmx()

            if not os.path.exists(SmTest.SMX_TEMP_DIR):
                self.PrefixLog("Creating " + SmTest.SMX_TEMP_DIR + " directory");
                os.makedirs(SmTest.SMX_TEMP_DIR)

            self.PrefixLog("  > cp " + outFile + " " + SmTest.SMX_TEMP_DIR)
            shutil.move(outFile, SmTest.SMX_TEMP_DIR)

            self.smxs.append(os.path.basename(outFile))

        return True

    def GetAllFiles( self ):
        files = self.files.copy()

        for smx in self.smxs:
            local = os.path.join(SmTest.SMX_TEMP_DIR, smx)
            remote = '/'.join([
                'addons/sourcemod/plugins',
                config_value('PLUGIN_PATH'),
                os.path.basename(local)
            ])

            files[local] = remote;

        return files

    def IsLocalServer( self ):
        return config_has_value('LOCAL_PATH')

    def CopyFiles( self ):
        if self.IsLocalServer():
            self.fileHandler = CopyFileList.CopyFileList(self.name)
        else:
            self.fileHandler = FtpFileList.FtpFileList(self.name)
        return self.fileHandler.CopyFiles(self.GetAllFiles(), self.deleteFiles)

    def DeleteFiles( self ):
        self.fileHandler.DeleteFiles()

    def RunCommands( self ):
        for command in self.commands:
            if re.search("^wait", command) != None:
                parts = re.split("\s+", command);
                self.PrefixLog("Waiting " + parts[1] + "s");
                sys.stdout.flush();
                sys.stderr.flush();
                time.sleep(int(parts[1]));
            else:
                self.Rcon(command, True)

    def Rcon( self, command, onStdout = False ):
        self.PrefixLog("rcon " + command)
        response = self.server.Rcon(command)

        if onStdout:
            print(response)
        else:
            self.PrefixLog(response)

        return response

    def Run( self ):
        self.Rcon("sm plugins unload_all")

        for smx in self.smxs:
            self.Rcon("sm plugins load " + config_value('PLUGIN_PATH') +
                "/" + smx)

        self.Rcon("sm plugins load_lock");
        self.RunCommands()

    def Prepare( self ):
        self.PrefixLog("Preparing");
        if not self.CompileSources():
            return False
        return self.CopyFiles()

    def Cleanup( self ):
        self.PrefixLog("Cleaning up");

        shutil.rmtree(SmTest.SMX_TEMP_DIR)
        self.DeleteFiles()

        self.Rcon("sm plugins load_unlock");
        self.Rcon("sm plugins unload_all")
        self.Rcon("sm plugins refresh")

