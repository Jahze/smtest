import os
import pprint
import re

import SmTest

SECTIONS = ['files', 'source', 'commands', 'includes']

class TestParser:
    def __init__( self, file, server ):
        self.server = server
        self.file = file
        self.haveError = False
        self.errorString = ""

    def Error( self, str ):
        self.haveError = True
        self.errorString = str

    def HasError( self ):
        return self.haveError

    def GetError( self ):
        return self.errorString

    def Parse( self ):
        section = ''
        t = SmTest.SmTest(os.path.basename(self.file), self.server)

        f = open(self.file, 'r')
        for line in f:
            if re.search('^#', line) != None:
                continue

            # Ignore white space
            m = re.search('^\s*$', line)

            if m != None:
                continue;

            # Try to find a section
            m = re.search('^\[(\w+)\]\s*$', line)

            if m != None:
                found = False

                for sec in SECTIONS:
                    if ( m.group(1) == sec ):
                        section = sec
                        found = True
                        break

                if not found:
                    self.Error("Unknown section: " + m.group(1))
                    return;
            elif section == "":
                self.Error("No section specified at:\n  " . line)
                return;
            else:
                # Trim the line
                line = line.strip()

                # Add stuff to the current section
                if section == "files":
                    parts = re.split('\s+', line)
                    delete = True
                    if len(parts) > 2 and parts[2] == "nodelete":
                        delete = False
                    t.AddFile(parts[0], parts[1], delete)
                elif section == "commands":
                    t.AddCommand(line)
                elif section == "source":
                    t.AddSource(line)
                elif section == "includes":
                    t.AddInclude(line)

        return t
