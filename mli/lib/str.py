#     This code is a part of program Manual Lichen identification
#     Copyright (C) 2021  Valerii Goncharuk (aka tagezi)
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

from os.path import join, normcase


def str_get_file_patch(sDir, sFile):
    """ Concatenates file path and file name based on OS rules.

        :param sDir: String with a patch to a file.
        :param sFile: String with a filename.
        :return: Patch to file based on OS rules.
        """
    return normcase(join(sDir, sFile))


def order_str_to_dict(sString):
    lString = sString.split()

    :param sString: A string that needs to separate.
    :type sString: str
    :return: A separated string by comma.
    :rtype: list or None
    """
    if sString:
        return sString.split(', ')
    return


def str_sep_dot(sString):
    """ Separates a string by dot to list.



def str_text_to_list(sString):
    if sString:
        return sString.split('\n')
    return

def str_sep_name_taxon(sString):
    sName = sString.split(') ')[1]
    if sName.find(', ') != -1:
        lName = sName.split(', ')
        return lName
    return sName, None



if __name__ == '__main__':
    pass
