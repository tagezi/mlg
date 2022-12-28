#     This code is a part of program Manual Lichen identification
#     Copyright (C) 2022 contributors Manual Lichen identification
#     The full list is available at the link
#     https://github.com/tagezi/mli/blob/master/contributors.txt
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

import csv

from mli.lib.sql import SQL


def inat_get_file(oConnector):
    with open('../../db/inat.csv', newline='') as fCSVFile:
        oData = csv.DictReader(fCSVFile, delimiter=';')
        inat_parser(oConnector, oData)


def inat_parser(oConnector, oData):
    for lRow in oData:
        sName, sIDiNat = lRow['Name'], lRow['ID']

        iTaxonID = 0
        tAnswer = oConnector.sql_get_values('Taxon', 'id_taxon',
                                            'taxon_name, id_status',
                                            (sName, 1,))
        if tAnswer:
            iTaxonID = tAnswer[0][0]

        iID = oConnector.sql_get_values('DBIndexes', 'id_db_index',
                                        'id_taxon, id_source',
                                        (iTaxonID, 1))
        iIDiNat = sIDiNat.replace('https://www.inaturalist.org/taxa/', '')
        print(sName)

        if iTaxonID and not iID:
            oConnector.insert_row('DBIndexes',
                                  'id_taxon, id_source, taxon_index',
                                  (iTaxonID, 1, iIDiNat,))


if __name__ == '__main__':
    pass
