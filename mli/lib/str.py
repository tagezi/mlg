#     This code is a part of program Science Articles Orderliness
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

def order_str_to_dict(sString):
    lString = sString.split()

    dElements = {'order': '', 'name': '', 'author': ''}
    i = 0
    for sElement in lString:
        if i == 1:
            dElements['order'] = sElement
        elif i == 2:
            dElements['name'] = sElement
        else:
            dElements['author'] = f"{dElements['author']} {sElement}"

        i += 1

    return dElements


def text_to_list(sString):
    if sString:
        return sString.split('\n')
    return


if __name__ == '__main__':
    pass
