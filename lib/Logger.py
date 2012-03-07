import sys

class Logger:
    enabled = False

    def Enable( y ):
        Logger.enabled = y

    def Log( text ):
        if Logger.enabled:
            sys.stderr.write(text+"\n")
