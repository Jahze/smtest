import config
import ftplib
import os
import shutil

import Logger

class CopyFileList:
    def __init__( self, name ):
        self.name = name
        self.storedFiles = []
        self.deleteFiles = {}

    def PrefixLog( self, text ):
        Logger.Logger.Log("[" + self.name + "] " + text)

    def CopyFiles( self, files, deleteFiles ):
        if len(files) == 0:
            return True

        for local,remote in files.items():
            fullRemote = '/'.join([config.config_value("LOCAL_PATH"), remote])
            self.PrefixLog("  > cp " + local + " " + fullRemote)
            shutil.copyfile(local, fullRemote);

        return True

    def DeleteFiles( self ):
        if len(self.storedFiles) == 0:
            return

        for f in self.storedFiles:
            if not self.deleteFiles[f]:
                continue

            self.PrefixLog("  > rm " + f)
            os.unlink(f);