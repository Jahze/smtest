import config
import os
import re
import subprocess
import sys

import Logger

def _GetBaseName( file ):
    file = os.path.basename(file)
    m = re.search("^(.*)[.][^.]*", file)
    if ( m == None ):
        return file
    else:
        return m.group(1)
            
class SpCompiler:
    def __init__( self, name ):
        self.name = name
        self.outputFile = ''
        self.baseCommand = [
            config.config_value('SPCOMP'),
            '-i' + config.config_value('SP_INCLUDE_DIR')
        ]
        
    def AddInclude( self, include ):
        self.baseCommand.append('-i' + include)
        
    def Compile( self, source ):
        command = ' '.join(self.baseCommand + [source]);
        
        Logger.Logger.Log("[" + self.name + "]   > " + command);
        
        proc = subprocess.Popen(command, 0, None, None, subprocess.PIPE, subprocess.PIPE)
        proc.wait();
        Logger.Logger.Log(proc.stderr.read().decode('utf-8'))
        Logger.Logger.Log(proc.stdout.read().decode('utf-8'))
        
        if proc.returncode != 0:
            Logger.Logger.Log("[" + self.name + "] Error (" + str(proc.returncode) + ")")
            self.outputFile = ''
            return False
        
        self.outputFile = _GetBaseName(source) + ".smx"
        
        if re.search("(?i)win", sys.platform) != None:
            (outDir, outFile) = os.path.split(source)
            self.outputFile = os.path.join(outDir, _GetBaseName(source) + ".smx")
        
        return True
        
    def GetLastOutputSmx( self ):
        return self.outputFile
