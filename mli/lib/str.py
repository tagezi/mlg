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

"""
The module contains a collection of functions for solving routine tasks with
strings.
"""
from os.path import join, normcase, split


def str_get_file_patch(sDir, sFile):
    """ Concatenates file path and file name based on OS rules.

        :param sDir: String with a patch to a file.
        :param sFile: String with a filename.
        :return: Patch to file based on OS rules.
        """
    return normcase(join(sDir, sFile))


def str_get_path(sFullFile):
    """ Splits a path to path and file name.

    :param sFullFile: Path with filename.
    :type sFullFile: str
    :return: The path to file.
    :rtype: str
    """
    return split(sFullFile)[0]


def str_sep_comma(sString):
    """ Separates a string by comma to list.

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

    :param sString: A string that needs to separate.
    :type sString: str
    :return: A separated string by dot.
    :rtype: list or None
    """
    if sString:
        return sString.split('.')
    return


def str_text_to_list(sString):
    if sString:
        return sString.split('\n')
    return


def str_sep_name_taxon(sString):
    """ Splits the string into taxon name and author, taking a string of the
        form '(rank) Taxon_name, authors'. It is permissible to indicate
        authors separated by commas, in brackets, using the '&' symbol.

    :param sString: A string that needed to separate.
    :type sString: str
    :return: A canonical form of taxon name and a string with the authors.
             Returns empty instead of author if no author was specified in
             the string.
    :rtype: list[str, str|None]
    """
    sString = ' '.join(sString.split(' ')[1:])
    print(sString)
    if sString.find(', ') != -1:
        sName = sString.split(', ')[0]
        sAuthor = ','.join(sString.split(',')[1:]).strip()
        print(sName, sAuthor)

        return sName, sAuthor
    return sString, None


if __name__ == '__main__':
    pass
