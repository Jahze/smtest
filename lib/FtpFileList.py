import config
import ftplib
import os

import Logger

class FtpFileList:
    def __init__( self, name ):
        self.name = name
        self.storedFiles = []
        self.deleteFiles = {}
        
    def PrefixLog( self, text ):
        Logger.Logger.Log("[" + self.name + "] " + text)
        
    def ConnectToFtp( self ):
        self.PrefixLog("Connecting to ftp server " + config.config_value('FTP_HOST'))
        try:
            ftp = ftplib.FTP(
                config.config_value('FTP_HOST'),
                config.config_value('FTP_USER'),
                config.config_value('FTP_PASS')
            )
        except ftplib.all_errors:
            self.PrefixLog("Connection failed")
            return None

        return ftp
        
    def FtpFiles( self, ftpFiles, deleteFiles ):
        if len(ftpFiles) == 0:
            return True

        ftp = self.ConnectToFtp()
        if ftp == None:
            return False

        for local,remote in ftpFiles.items():
            try:
                file = open(local, "rb")
            except IOError:
                self.PrefixLog("Couldn't open " + local)
                ftp.quit()
                return False

            # Change to the correct firectory
            (folder,filename) = os.path.split(remote)
            folder = os.path.join(config.config_value("FTP_PATH"), folder)
            if folder:
                try:
                    self.PrefixLog("FTP: CD " + folder)
                    response = ftp.cwd(folder)
                    self.PrefixLog("FTP: " + response)
                except all_errors:
                    self.PrefixLog("FTP: Couldn't CD")
                    return False

            # Save the file
            try:
                self.PrefixLog("FTP: STOR " + filename)
                response = ftp.storbinary('STOR '+filename, file)
                self.PrefixLog("FTP: " + response)
            except all_errors:
                self.PrefixLog("FTP: Couldn't STOR " + filename)
                return False

            remotePath = '/'.join([folder,filename])
            self.storedFiles.append(remotePath)
            if local in deleteFiles:
                self.deleteFiles[remotePath] = deleteFiles[local]
            else:
                self.deleteFiles[remotePath] = True
                
        ftp.quit()
        
        return True

    def DeleteFiles( self ):
        if len(self.storedFiles) == 0:
            return

        ftp = self.ConnectToFtp()
        if ftp == None:
            return

        for remote in self.storedFiles:
            if not self.deleteFiles[remote]:
                continue

            (folder,filename) = os.path.split(remote)
            if folder:
                try:
                    self.PrefixLog("FTP: CD " + folder)
                    response = ftp.cwd(folder)
                    self.PrefixLog("FTP: " + response)
                except all_errors:
                    self.PrefixLog("FTP: Couldn't CD")
                    continue

            # Delete the file
            try:
                self.PrefixLog("FTP: DELETE " + filename)
                response = ftp.delete(filename)
                self.PrefixLog("FTP: " + response)
            except all_errors:
                self.PrefixLog("FTP: Couldn't delete " + filename)
