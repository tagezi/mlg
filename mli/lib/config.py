#     This code is a part of program Manual Lichen identification
#     Copyright (C) 2022  Valerii Goncharuk (aka tagezi)
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

import sys
from configparser import ConfigParser, NoSectionError

from mli.lib.str import str_get_file_patch


class ConfigProgram(ConfigParser):
    def __init__(self, sFilePath='config.ini'):
        super().__init__()

        self.sFilePath = str_get_file_patch(sys.path[0], sFilePath)
        self.read(self.sFilePath)
        self.lSections = self.sections()

    def get_config_value(self, sSection, sOptions):
        return self.get(sSection, sOptions)

    def set_config_value(self, sSection, sOptions, sValue=''):
        try:
            self.set(sSection, sOptions, sValue)
        except NoSectionError:
            self.add_section(sSection)
            self.set(sSection, sOptions, sValue)

        with open(self.sFilePath, 'w') as fConfigFile:
            self.write(fConfigFile)


if __name__ == '__main__':
    pass
