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

""" The module provides a means to get information from a taxon, as specified
in gbif .

function:
    gbif_get_children(sGBIF_id)
    gbif_get_id_from_gbif(sName, sLevel='species')
    gbif_get_id(oConnector, sName, sLevelEn)
    gbif_get_many(sURL, sGBIF_id)
    gbif_get_status_id(oConnector, sStatus)
    gbif_get_synonyms(sGBIF_id)
    gbif_get_taxon_info(sGBIF_id, sLevel='species')
    gbif_get_update(oConnector, iLevel)
    gbif_is_lichen(dTaxon)
    gbif_parser_name(sString)
    gbif_parser_taxon(dData)
    gbif_parsing_answer(oConnector, lAnswer, sType)
    gbif_parsing_species(oConnector, dAnswer)
    gbif_save_species(oConnector, dAnswer, iLevel)
    gbif_update(oConnector, dAnswer, iTaxonID)
"""

import re
import requests
from time import sleep

from pygbif import species
from sql import SQL


def gbif_is_lichen(dTaxon):
    """ Checks if the taxon is a lichen.

    :param dTaxon: Filed 'result' of answer from gbif.
    :type dTaxon: dict
    :return: True if taxon is lichen, and False if opposite.
    :rtype: bool
    """
    if 'class' in dTaxon and (dTaxon['class'] == 'Lecanoromycetes' or
                              dTaxon['class'] == 'Arthoniomycetes' or
                              dTaxon['class'] == 'Lichinomycetes'):
        return True

    if 'order' in dTaxon and (dTaxon['order'] == 'Pyrenulales' or
                              dTaxon['order'] == 'Verrucariales'):
        return True

    if 'family' in dTaxon and (dTaxon['family'] == 'Abrothallaceae' or
                               dTaxon['family'] == 'Aphanopsidaceae' or
                               dTaxon['family'] == 'Arthopyreniaceae' or
                               dTaxon['family'] == 'Coniocybaceae' or
                               dTaxon['family'] == 'Naetrocymbaceae' or
                               dTaxon['family'] == 'Sphinctrinaceae' or
                               dTaxon['family'] == 'Strigulaceae' or
                               dTaxon['family'] == 'Thelocarpaceae'):
        return True

    if 'genus' in dTaxon and (dTaxon['genus'] == 'Dictyonema' or
                              dTaxon['genus'] == 'Lichenomphalia' or
                              dTaxon['genus'] == 'Multiclavula'):
        return True

    return False


def gbif_get_id_from_gbif(sName, sLevel='species'):
    """ Looks up a taxon name in the gbif database.

    :param sName: The name of a taxon.
    :type sName: str
    :param sLevel: The rank of a taxon.
    :type sLevel:str
    :return: Key ID of the taxon in gbif.
    :rtype: str
    """
    if not sName:
        return

    sLevel = sLevel.upper()
    PARAMS = {
        'q': sName,
    }
    URL = 'https://api.gbif.org/v1/species/suggest'
    oSession = requests.Session()
    oRequest = oSession.get(url=URL, params=PARAMS)
    lData = oRequest.json()
    sleep(0.5)
    if not lData:
        return

    for dData in lData:
        if gbif_is_lichen(dData) and dData['rank'] == sLevel and \
                dData['canonicalName'] == sName:
            return lData[0]['key']

    return


def gbif_get_taxon_info(sGBIF_id, sLevel='species'):
    """ General information about the taxon by its ID.

    :param sGBIF_id: A key ID of taxon in gbif.
    :type: str
    :param sLevel: A level of the taxon.
    :type sLevel: str
    :return: A normalized dictionary of taxon information.
    :rtype: dict[str, bool, str, str, str, str, str, int]|None
    """
    if not sGBIF_id:
        return

    sLevel = sLevel.upper()
    URL = f'https://api.gbif.org/v1/species/{sGBIF_id}'
    oSession = requests.Session()
    oRequest = oSession.get(url=URL)
    dData = oRequest.json()
    sleep(0.5)
    if dData['rank'] == sLevel:
        return gbif_parser_taxon(dData)

    return


def gbif_get_synonyms(sGBIF_id):
    """ Generates an api link for obtaining synonyms from the server and
        returns a normalized response.

    :param sGBIF_id: A key ID of taxon in gbif.
    :type: str
    :return: A normalized response.
    :rtype: list[dict[str, bool, str, str, str, str, str, int]|None]
    """
    sURL = f'https://api.gbif.org/v1/species/{sGBIF_id}/synonyms'
    return gbif_get_many(sURL, sGBIF_id)


def gbif_get_children(sGBIF_id):
    """ Generates an api link for obtaining children from the server and
        returns a normalized response.

    :param sGBIF_id: A key ID of taxon in gbif.
    :type: str
    :return: A normalized response.
    :rtype: list[dict[str, bool, str, str, str, str, str, int]|None]
    """
    sURL = f'https://api.gbif.org/v1/species/{sGBIF_id}/children'
    return gbif_get_many(sURL, sGBIF_id)


def gbif_get_many(sURL, sGBIF_id):
    """ Generates an api link for obtaining children from the server and
        returns a normalized response.

    :param sURL: An URL for sending to gbif server.
    :type sURL: str
    :param sGBIF_id: A key ID of taxon in gbif.
    :type: str
    :return: A normalized response.
    :rtype: list[dict[str, bool, str, str, str, str, str, int]|None]
    """
    if not sGBIF_id:
        return

    bEndOfRecords = False
    iOffset = 0
    lAnswer = []
    oSession = requests.Session()
    while not bEndOfRecords:
        PARAMS = {
            'limit': 1000,
            'offset': iOffset
        }
        oRequest = oSession.get(url=sURL, params=PARAMS)
        dJSON = oRequest.json()
        sleep(0.5)
        if type(dJSON) == str:
            return

        bEndOfRecords = dJSON['endOfRecords']
        iOffset = iOffset + 1000
        lData = dJSON['results']
        if not lData and bEndOfRecords:
            return lAnswer
        if not lData:
            return

        for dData in lData:
            lAnswer.append(gbif_parser_taxon(dData))

    return lAnswer


def gbif_parser_taxon(dData):
    """ Selects from the server response the information necessary for further
     processing.

    :param dData: An answer of server.
    :type dData: dict
    :return: Selection from the server response with the necessary information.
    :rtype: dict[str, bool, str, str, str, str, str, int]|None
    """
    sName, sAuthor, iYear = gbif_parser_name(dData['scientificName'])
    if dData['synonym']:
        sParent = gbif_parser_name(dData['accepted'])[0]
    else:
        sParent = dData['parent']

    dAnswer = {'tax_status': dData['taxonomicStatus'],
               'synonym': dData['synonym'],
               'id': dData['key'],
               'rank': dData['rank'],
               'parent': sParent,
               'name': sName,
               'author': sAuthor,
               'year': iYear}

    return dAnswer


def gbif_parser_name(sString):
    """ Parsing a name of the taxon separating the canonical name from the
    name of the author and year, if possible.

    :param sString: A string with a name of the taxon.
    :type sString: str
    :return: A canonical name, an author name and a naming year of the taxon.
    :rtype: list[str, str, int]
    """
    lResponse = species.name_parser([sString])
    sName = ''
    sAuthor = ''
    iYear = None
    for dResponse in lResponse:
        if 'canonicalName' in dResponse:
            sName = dResponse['canonicalName']
        else:
            sName = dResponse['scientificName']
        if 'bracketAuthorship' in dResponse:
            sAuthor = f'({dResponse["bracketAuthorship"]}) '
        if 'authorship' in dResponse:
            sAuthor = f'{sAuthor}{dResponse["authorship"]}'
        if 'year' in dResponse and type(dResponse['year']) == int:
            iYear = int(dResponse['year'])

        if not sAuthor:
            sAuthor = None

        sleep(0.7)

        return sName, sAuthor, iYear


def gbif_get_id(oConnector, sName, sLevelEn):
    """ Checks if the taxon's id exists in the database, and if it doesn't,
    it gets it from the site.

    :param oConnector: An instance of the sqlite database api class.
    :type oConnector: SQL
    :param sName: A name of the taxon.
    :type sName: str
    :param sLevelEn: A name of the taxon rank in english language.
    :type sLevelEn: str
    :return: ID taxon in gbif.
    :rtype: int
    """
    sGBIF_id = oConnector.sql_get_id('DBIndexes', 'taxon_index',
                                     'id_taxon, id_source',
                                     (sName, 12,))
    if not sGBIF_id:
        sGBIF_id = gbif_get_id_from_gbif(sName, sLevelEn)

    return sGBIF_id


def gbif_parsing_answer(oConnector, lAnswer, sType):
    """ Parses the response a list of dictionaries with taxon information.

    :param oConnector: An instance of the sqlite database api class.
    :type oConnector: SQL
    :param lAnswer: A list of dictionaries with taxon information.
    :type lAnswer: list[dict[str, bool, str, str, str, str, str, int]|None]
    :param sType: The first word to output to the string. It makes sense to
                  indicate either 'Synonym' or 'Children'.
    :type sType: str
    :return: None
    """
    if lAnswer:
        for dAnswer in lAnswer:
            print(f'{sType}: {dAnswer["parent"]} - {dAnswer["name"]}')
            gbif_parsing_species(oConnector, dAnswer)


def gbif_get_update(oConnector, iLevel):
    """ Allows you to select all names from the database by level, start
    getting data from gbif and enter information into the database.

    :param oConnector: An instance of the sqlite database api class.
    :type oConnector: SQL
    :param iLevel: ID of a rank in database.
    :type iLevel: int
    :return: None
    """
    lRows = oConnector.get_all_by_level(iLevel)
    sLevelEn = oConnector.get_level_name('level_en_name', iLevel)[0][0]
    if lRows:
        for sRow in lRows:
            bBreak = oConnector.sql_get_id('UpdateTaxonGBIF',
                                           'id', 'id_taxon_sp', (sRow[0],))
            if bBreak:
                continue

            sGBIF_id = gbif_get_id(oConnector, sRow[1], sLevelEn)

            dAnswer = gbif_get_taxon_info(sGBIF_id, sLevelEn)
            if dAnswer:
                print(f'Name: {sRow[0]}\t{sRow[1]}')
                gbif_parsing_species(oConnector, dAnswer)

            lAnswer = gbif_get_children(sGBIF_id)
            gbif_parsing_answer(oConnector, lAnswer, 'Children')

            oConnector.insert_row('UpdateTaxonGBIF', 'id_taxon_sp', (sRow[0],))

        lRows = oConnector.get_all_by_level(iLevel)
        for sRow in lRows:
            bBreak = oConnector.sql_get_id('UpdateTaxonGBIF',
                                           'id', 'id_taxon_sn', (sRow[0],))
            if bBreak:
                continue

            sGBIF_id = gbif_get_id(oConnector, sRow[1], sLevelEn)
            lAnswer = gbif_get_synonyms(sGBIF_id)

            gbif_parsing_answer(oConnector, lAnswer, 'Synonym')
            oConnector.insert_row('UpdateTaxonGBIF', 'id_taxon_sn', (sRow[0],))


def gbif_parsing_species(oConnector, dAnswer):
    """ Specifies whether to make changes to the database.

    :param oConnector: An instance of the sqlite database api class.
    :type oConnector: SQL
    :param dAnswer: A dictionary with information about the taxon.
    :type dAnswer: dict[str, bool, str, str, str, str, str, int]
    :return: None
    """
    # Exclude taxa with type name SH1169675.09FU
    if bool(re.search(r'\d', dAnswer['name'])):
        return
    # Exclude taxa with missing rank
    if dAnswer['rank'] == 'UNRANKED':
        return

    iLevel = oConnector.get_level_id('level_en_name',
                                     (dAnswer['rank'].lower(),))[0][0]

    bContinue = oConnector.sql_get_id('Taxon', 'id_taxon',
                                      'id_level, taxon_lat_name, author',
                                      (iLevel, dAnswer['name'],
                                       dAnswer['author'],))
    if not bContinue:
        bContinue = gbif_save_species(oConnector, dAnswer, iLevel)
    else:
        gbif_update(oConnector, dAnswer, bContinue)

    bID = oConnector.sql_get_id('DBIndexes', 'id_db_index',
                                'id_taxon', (bContinue,))
    if not bID:
        tValues = (bContinue, 12, dAnswer['id'],)
        oConnector.insert_row('DBIndexes',
                              'id_taxon, id_source, taxon_index',
                              tValues)


def gbif_save_species(oConnector, dAnswer, iLevel):
    """ Saving information about the taxon in database.

    :param oConnector: An instance of the sqlite database api class.
    :type oConnector: SQL
    :param dAnswer: A dictionary with information about the taxon.
    :type dAnswer: dict[str, bool, str, str, str, str, str, int]
    :param iLevel: The level's ID in database.
    :type iLevel: int
    :return: The taxon's ID in database.
    :rtype: int or bool
    """
    print(f'Insert row - {dAnswer["name"]}')
    iStatus = gbif_get_status_id(oConnector, dAnswer['tax_status'])
    iParent = oConnector.get_id_by_name_status((dAnswer['parent'], 1,))

    sColumns = 'id_level, id_main_taxon, ' \
               'taxon_lat_name, author, year, id_status'
    tValues = (iLevel, iParent, dAnswer['name'],
               dAnswer['author'], dAnswer['year'], iStatus,)

    return oConnector.insert_row('Taxon', sColumns, tValues)


def gbif_get_status_id(oConnector, sStatus):
    """ Returns the status id from the database.

    :param oConnector: An instance of the sqlite database api class.
    :type oConnector: SQL
    :param sStatus: The name of the status, as is customary in gbif.
    :type sStatus: str
    :return: the status ID.
    :rtype: int or bool
    """
    return oConnector.sql_get_id('TaxonStatus', 'id_status',
                                 'status_name', (sStatus,))


def gbif_update(oConnector, dAnswer, iTaxonID):
    """ Updates information in the database about the author and naming year.

    :param oConnector: An instance of the sqlite database api class.
    :type oConnector: SQL
    :param dAnswer: A dictionary with information about the taxon.
    :type dAnswer: dict[str, bool, str, str, str, str, str, int]
    :param iTaxonID: The taxon's ID in database.
    :type iTaxonID: int
    :return: None
    """
    sName = dAnswer['name']
    lContinue = oConnector.sql_get_values('Taxon',
                                          'author, year, id_status, '
                                          'id_main_taxon',
                                          'taxon_lat_name', (sName,))

    if not lContinue[0][0] and dAnswer['author'] and \
            dAnswer['tax_status'] == 'ACCEPTED':
        oConnector.update('Taxon', 'author', 'id_taxon',
                          (dAnswer['author'], iTaxonID,))
        print(f'Enter author: {sName} - {dAnswer["author"]}')

    if dAnswer['year'] and not lContinue[0][1]:
        oConnector.update('Taxon', 'year', 'id_taxon',
                          (dAnswer['year'], iTaxonID,))
        print(f'Enter year: {sName} - {dAnswer["year"]}')


if __name__ == '__main__':
    pass
