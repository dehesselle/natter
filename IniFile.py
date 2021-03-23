# SPDX-License-Identifier: MIT
# https://github.com/dehesselle/natter

# usage:
#
#   ini = IniFile.IniFile("test.ini")
#   ini["mysection"] = {}
#   ini["mysection"]["mykey"] = "myvalue"


import configparser
import os
import errno
from pathlib import Path
import atexit
from xdg import XDG_CONFIG_HOME


class IniFile:
    def __init__(self, filename="", create=True):
        if not filename:
            raise ValueError("filename required")

        self.file = Path(filename)

        if self.file.parent == Path():  # no directory has been specified
            self.file = XDG_CONFIG_HOME.joinpath(self.file)

        if not self.file.exists():
            if create:
                self.file.touch()
            else:
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), self.file)

        self.configParser = configparser.ConfigParser()
        self.configParser.read(self.file)
        atexit.register(self.save)  # save ini

    def save(self):
        try:
            with open(self.file, "w") as config:
                self.configParser.write(config)
        except OSError as e:
            print("unable to save:", self.file)

    def __getitem__(self, item):
        return self.configParser[item]

    def __contains__(self, key):
        return self.configParser.__contains__(key)

    def __setitem__(self, item1, item2="", item3=""):
        if not item3:
            self.configParser[item1] = item2
        else:
            self.configParser[item1][item2] = item3
