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

""" The module provides an API for working with the database. It creates a
multi-level API that can be used in other modules to create requests using
a minimum of transmitted data.

Function:
    get_columns(sColumns, sConj='AND')

Class:
    SQL

Using:
    Foo = SQL(_DataBaseFile_)
"""

import logging
import sqlite3
from sqlite3 import DatabaseError

from mli.lib.log import start_logging
from mli.lib.str import str_get_file_patch


def check_connect_db(oConnector, sBasePath, sDBDir):
    """ Checks for the existence of a database and if it does not find it, then
        creates it with default values.

    :param oConnector: Instance attribute of SQL.
    :type oConnector: SQL
    :param sBasePath: A path of the executed script.
    :type sBasePath: str
    :param sDBDir: A dir when database is by default.
    :type sDBDir: str
    :return: None
    """
    # The list of tables in DB
    lTables = ['Colors', 'DBIndexes', 'DBSources', 'Images', 'Lang',
               'LangVariant', 'LifeForm', 'LifeFormTaxon', 'LocalName',
               'Metering', 'PartProperties', 'Parts', 'PartsColor',
               'PartsSize', 'Places', 'PlacesOfLive', 'Substrate',
               'SubstrateOfTaxon', 'Taxon', 'TaxonLevel', 'TaxonStatus']

    for sTable in lTables:
        bExist = oConnector.select('sqlite_master', '*', 'name, type',
                                   (sTable, 'table',)).fetchone()
        if not bExist:
            sDBPath = str_get_file_patch(sBasePath, sDBDir)
            sFile = str_get_file_patch(sDBPath, 'mli_backup.sql')
            with open(sFile) as sql_file:
                sql_script = sql_file.read()
                oConnector.execute_script(sql_script)
                break


def get_columns(sColumns, sConj='AND'):
    """ The function of parsing a string, accepts a list of table columns
    separated by commas and returns this list with '=? AND' or '=? OR'
    as separator.

    :param sColumns: A string with a list of table columns separated by commas.
    :type sColumns: str
    :param sConj: The one from 'AND' or 'OR' operator condition.
        By default, is used 'AND'.
    :type sConj: str or None
    :return: The string with a list of table columns separated
        by '=? AND' or '=? OR'.
    :rtype: str
    """
    return sColumns.replace(', ', '=? ' + sConj + ' ') + "=?"


def get_increase_value(sColumns, tValues):
    """ Checks counting elements of values, and if them fewer,
     then makes them equal.

     Note:
        In the rison that tuple can't be multiplied on flot, the process
        of increasing the tuple becomes somewhat resource-intensive. So,
        tValues should be consisting of one element.

    :param sColumns: Colum(s) in query.
    :type sColumns: str
    :param tValues: Values should be specified in the request.
    :type tValues: tuple or list
    :return: A tuple with values, which equal to sColumns.
    :rtype: list
    """
    if len(sColumns.split(',')) > len(tValues) == 1:
        return tValues * len(sColumns.split(', '))

    logging.error('The tuple must be filled or consist of one element.'
                  f'The columns: {sColumns} \n The tuple: {tValues}')
    return


class SQL:
    # TODO: PyCharm does not want to define standard reStructureText
    #  designation. I don't how it can fix now. So, I use available methods
    #  to structure text.
    """
    Provides interface for working with database from others scripts.

    *Methods*
      # Standard methods.
        * __init__ -- Method initializes a cursor of sqlite database.
        * __del__ -- Method closes the cursor of sqlite database.
      # Low level methods.
        * export_db -- Method exports from db to sql script.
        * execute_script -- Method imports from slq script to db.
        * execute_query -- Method execute sql_search query.
        * insert_row -- Method inserts a record in the database table.
        * delete_row -- Method deletes a row from the table.
        * update -- Method updates value(s) in record of the database table.
        * select -- Method does selection from the table.
      # Average level API.
        * sql_get_id: Finds id of the row by value(s) of table column(s).
        * sql_get_all: Method gets all records in database table.
        * sql_count: Method counts number of records in database table.
        * sql_table_clean: Method cleans up the table.
    """

    # Standard methods
    def __init__(self, sFileDB):
        """ Initializes connect with database.

        :param sFileDB: Path to database as string.
        :type sFileDB: str
        """
        self.logging = start_logging()
        try:
            self.oConnector = sqlite3.connect(sFileDB)
        except DatabaseError as e:
            self.logging.exception(f"An error has occurred: {e}.\n"
                                   f"String of query: {sFileDB}\n")

    def __del__(self):
        """ Closes connection with the database. """
        self.oConnector.close()

    # Low methods level
    def export_db(self):
        """ Method exports from db to sql script. """
        return self.oConnector.iterdump()

    def execute_script(self, sSQL):
        """ Method executes sql script.

        The main difference from the method is the ability to execute
        several commands at the same time. For example, using this method,
        you can restore the database from sql dump.

        :param sSQL: SQL Script as string.
        :type sSQL: str
        :return: True if script execution is successful, otherwise False.
        :rtype: bool
        """
        oCursor = self.oConnector.cursor()
        try:
            oCursor.executescript(sSQL)
        except DatabaseError as e:
            logging.exception(f'An error has occurred: {e}.\n'
                              f'String of query: {sSQL}\n')
            return False

        return True

    def execute_query(self, sSQL, tValues=None):
        """ Method executes sql script.

        :param sSQL: SQL query.
        :type sSQL: str
        :param tValues: value(s) that need to safe inserting into query
            (by default, None).
        :type tValues: tuple or list or None
        :return: Cursor or bool -- True if script execution is successful,
            otherwise False.
        """
        oCursor = self.oConnector.cursor()
        try:
            if tValues is None:
                oCursor.execute(sSQL)
            else:
                oCursor.execute(sSQL, tValues)
        except DatabaseError as e:
            logging.exception(f'An error has occurred: {e}.\n'
                              f'String of query: {sSQL}\n'
                              f'Parameters: {tValues}')
            return False

        return oCursor

    def insert_row(self, sTable, sColumns, tValues):
        """ Inserts a record in the database table.

        :param sTable: Table name as string.
        :type sTable: str
        :param sColumns: Columns names of the table by where needs inserting.
        :type sColumns: str
        :param tValues: Value(s) as tuple for inserting.
        :type tValues: tuple or list
        :return: ID of an inserted row  if the insert was successful.
            Otherwise, False.
        :rtype: str or bool
        """
        sSQL = ("?, " * len(sColumns.split(", ")))[:-2]
        sqlString = f'INSERT INTO {sTable} ({sColumns}) VALUES ({sSQL})'
        oCursor = self.execute_query(sqlString, tValues)
        if oCursor:
            self.oConnector.commit()
            return oCursor.lastrowid

        return False

    def delete_row(self, sTable, sColumns=None, tValues=None):
        """ Deletes row in the database table by value(s).

        :param sTable: A table as string in where need to delete row.
        :type sTable: str or None
        :param sColumns: Column(s) where the value(s) will be found.
            (by default, None).
        :type sColumns: str or None
        :param tValues: value(s) as tuple for search of rows.
            (by default, None).
        :type tValues: tuple or list
        :return: True if the deletion is successful, otherwise False.
        :rtype: bool
        """
        if sColumns is not None:
            sSQL = f'DELETE FROM {sTable} WHERE {get_columns(sColumns)}'
            oCursor = self.execute_query(sSQL, tValues)
        else:
            sSQL = f'DELETE FROM {sTable}'
            oCursor = self.execute_query(sSQL)

        if oCursor:
            self.oConnector.commit()
            return True

        return False

    def update(self, sTable, sSetUpdate, sWhereUpdate, tValues):
        """ Updates value(s) in the record of the database table.

        :param sTable: A Table as string where update is need to do.
        :type sTable: str
        :param sSetUpdate: Column(s) where the value are writen.
        :type sSetUpdate: str
        :param sWhereUpdate: A column where values correspond to the required.
        :type sWhereUpdate: str
        :param tValues: value(s) as tuple for search corresponding rows.
        :type tValues: tuple or list
        :return: True if the insert was successful, otherwise False.
        :rtype: bool
        """
        sSetUpdate = sSetUpdate + "=?"
        sWhereUpdate = get_columns(sWhereUpdate)
        sSQL = f'UPDATE {sTable} SET {sSetUpdate} WHERE {sWhereUpdate}'
        oCursor = self.execute_query(sSQL, tValues)
        if oCursor:
            self.oConnector.commit()
            return True

        return False

    def select(self, sTable, sGet, sWhere='', tValues='', sConj='', sFunc=''):
        """ Looks for row by value(s) in table column(s).

        :param sTable: Table name as string.
        :type sTable: str
        :param sGet: Name of the column of the table, which will be returned.
        :type sGet: str
        :param sWhere: Names of columns of the table, by which to search
            (by default, empty).
        :type sWhere: str or None
        :param sConj: The one from 'AND' or 'OR' operator condition.
            By default, is used 'AND'.
        :type sConj: str or None
        :param tValues: Value(s) as tuple for search
            (by default, empty).
        :type tValues: tuple or list or None
        :param sFunc: Function name of sqlite, which need to apply
            (by default, empty). Note: Now, you can use only two sqlite
            functions: Count and DISTINCT.
        :type sFunc: str or None
        :return: Cursor or bool -- Cursor object within rows that was found,
            or False, if the row not found.
        """
        if sFunc == 'Count':
            sGet = f'Count({sGet})'
        elif sFunc == 'DISTINCT':
            sGet = f'{sFunc} {sGet}'

        if sWhere:
            if sConj:
                sCol = get_columns(sWhere, sConj)
            else:
                sCol = get_columns(sWhere)

            sSQL = f'SELECT {sGet} FROM {sTable} WHERE {sCol}'
            oCursor = self.execute_query(sSQL, tValues)
        else:
            oCursor = self.execute_query(f'SELECT {sGet} FROM {sTable}')

        if oCursor:
            return oCursor

        return False

    # Average API level
    def sql_get_values(self, sTable, sID, sWhere, tValues, sConj=''):
        """ Looks for ID of the row by value(s) of table column(s).

        :param sTable: Table name as string.
        :type sTable: str
        :param sID: Name of the column of the table by which to search.
        :type sID: str
        :param sWhere: Names of columns of the table by which to search.
        :type sWhere: str
        :param tValues: Value(s) as tuple for search.
        :type tValues: tuple or list
        :param sConj: The one from 'AND' or 'OR' operator condition.
            By default, is used 'AND'.
        :type sConj: str or None
        :return: ID as Number in the row cell, or 0, if the row not found.
        :rtype: list or bool
        """
        if sWhere:
            if sConj:
                tValues = get_increase_value(sWhere, tValues)
                sWhere = get_columns(sWhere, sConj)
            else:
                sWhere = get_columns(sWhere)
        sSQL = f'SELECT {sID} FROM {sTable} WHERE {sWhere}'
        oCursor = self.execute_query(sSQL, tValues)
        if oCursor:
            lRows = oCursor.fetchall()
            if lRows:
                return lRows

        return False

    def sql_get_id(self, sTable, sID, sWhere, tValues, sConj=''):
        lRows = self.sql_get_values(sTable, sID, sWhere, tValues, sConj)
        if lRows:
            return lRows[0][0]

        return False

    def sql_get_all(self, sTable):
        """ Gets all records in database table.

        :param sTable: Table name as string where records should be received.
        :type sTable: str
        :return: Tuple of all rows of table.
        :rtype: tuple or bool
        """
        oCursor = self.execute_query(f'SELECT * FROM {sTable}')
        if oCursor:
            return oCursor.fetchall()

        return False

    def sql_count(self, sTable):
        """ Counts number of records in database table.

        :param sTable: Table name as string where records should be count.
        :type sTable: str
        :return: Number of found records.
        :rtype: int or bool
        """
        # sTable, sGet, sWhere, tValues, sFunc=None
        oCursor = self.select(sTable, sGet='*', sFunc='Count')
        if oCursor:
            row = oCursor.fetchall()
            return row[0][0]

        return False

    def sql_table_clean(self, lTable):
        """ Cleans up the table.

        :param lTable: Table names as list or tuple of string, or table name
            as string where cleaning is need to do.
        :type lTable: tuple or list
        :return: True, if execution is successful. Otherwise, False.
            Note: False is returned even if cleaning the last table in
            the tuple was not successful.
        :rtype: bool
        """
        if type(lTable) == str:
            lTable = [lTable]

        for sTable in lTable:
            bDel = self.delete_row(str(sTable))
            if not bDel:
                return False

        return True

    # Top API level
    def get_all_by_level(self, iLevel):
        return self.execute_query(
            'SELECT id_taxon, taxon_name '
            'FROM Taxon WHERE  id_level=? '
            'ORDER BY taxon_name ASC', (iLevel,))

    def get_garbage(self):
        sSQL = "SELECT taxon_name, author, COUNT(*) c " \
               "FROM Taxon GROUP BY taxon_name, author HAVING c > 1"
        lRow = self.execute_query(sSQL).fetchall()
        if lRow:
            return lRow

        return False

    def del_garbage(self, sSource='GBIF'):
        lGarbage = self.get_garbage()
        if lGarbage:
            for lRow in lGarbage:
                sAuthor = lRow[1]
                lDelete = self.sql_get_values('Taxon', 'id_taxon',
                                              'taxon_name, author',
                                              (lRow[0], sAuthor,))
                if not lDelete:
                    lDelete = self.execute_query('SELECT id_taxon FROM Taxon '
                                                 f'WHERE taxon_name=? '
                                                 f'AND author is NULL ',
                                                 (lRow[0],)).fetchall()
                iSource = self.get_source_id(sSource)
                if lDelete and iSource:
                    while len(lDelete) > 1:
                        iID = self.sql_get_id('DBIndexes', 'id_db_index',
                                              'id_taxon, id_source',
                                              (lDelete[-1][0], iSource,))
                        self.delete_row('DBIndexes', 'id_db_index', (iID,))
                        self.delete_row('Taxon', 'id_taxon', lDelete[-1])
                        lDelete.pop(-1)

    def get_id_by_name_author(self, tValue, sTable='Taxon'):
        if tValue[1]:
            return self.sql_get_id(sTable, 'id_taxon',
                                   'taxon_name, author', tValue)
        else:
            return self.sql_get_id(sTable, 'id_taxon',
                                   'taxon_name', (tValue[0],))

    def get_id_by_name_status(self, tValue, sTable='Taxon'):
        return self.sql_get_id(sTable, 'id_taxon',
                               'taxon_name, id_status', tValue)

    def get_level_id(self, sColumns, sValues):
        return self.sql_get_id('TaxonLevel', 'id_level', sColumns, (sValues,))

    def get_level_name(self, sColumns, iValues):
        return self.sql_get_values('TaxonLevel', sColumns,
                                   'id_level', (iValues,))

    def get_synonyms(self, iValue):
        sSQL = 'SELECT TaxonLevel.level_name, Taxon.taxon_name, ' \
               'Taxon.author ' \
               'FROM Taxon ' \
               'JOIN TaxonLevel ON Taxon.id_level=TaxonLevel.id_level ' \
               f'WHERE Taxon.id_main_taxon=? AND  Taxon.id_status<>? ' \
               'ORDER BY Taxon.id_level ASC, Taxon.taxon_name ASC;'
        return self.execute_query(sSQL, (iValue, 1,)).fetchall()

    def get_source_id(self, sValue):
        return self.sql_get_id('DBSources', 'id_source',
                               'source_abbr', (sValue,))

    def get_status_id(self, sValue, sColumn='status_local_name'):
        return self.sql_get_id('TaxonStatus', 'id_status',
                               sColumn, (sValue,))

    def get_statuses(self):
        return self.sql_get_all('TaxonStatus')

    def get_substrate_id(self, sValue):
        return self.sql_get_id('Substrate', 'id_substrate',
                               'substrate_name', (sValue,))

    def get_synonym_id(self, sName, sAuthor):
        return self.sql_get_id('Taxon', 'id_taxon',
                               'taxon_name, author', (sName, sAuthor,))

    def get_taxon_id(self, sName, sAuthor, sStatus='ACCEPTED'):
        iIDStatus = self.get_status_id(sStatus, 'status_name')
        if sAuthor:
            tValues = (sName, sAuthor, iIDStatus,)
            return self.sql_get_id('Taxon', 'id_taxon',
                                   'taxon_name, author, id_status', tValues)
        else:
            sSQL = 'SELECT id_taxon FROM Taxon ' \
                   'WHERE taxon_name=? AND author is NULL AND id_status=?;'
            tValues = (sName, iIDStatus,)
            iTaxonID = self.execute_query(sSQL, tValues).fetchone()
            if iTaxonID:
                return iTaxonID[0]

        return

    def get_taxon_children(self, iID, sName, sAuthor, sStatus='ACCEPTED'):
        sStatus = sStatus.upper()
        iIDStatus = self.sql_get_id('TaxonStatus', 'id_status', 'status_name',
                                    (sStatus,))
        if sAuthor:
            iMainID = self.sql_get_id('Taxon', 'id_taxon',
                                      'taxon_name, author',
                                      (sName, sAuthor))
        else:
            sSQL = 'SELECT id_taxon FROM Taxon ' \
                   'WHERE taxon_name=? AND author is NULL'
            iMainID = self.execute_query(sSQL, (sName,))

        oCursor = self.select('Taxon',
                              'id_taxon, taxon_name, author, year',
                              'id_main_taxon, id_status',
                              (iID, iMainID, iIDStatus,))

        return oCursor.fetchone()

    def get_taxon_list(self, sStatus):
        sSQL = 'SELECT Taxon.id_level, TaxonLevel.level_name, ' \
               'Taxon.taxon_name, Taxon.author ' \
               'FROM Taxon ' \
               'JOIN TaxonLevel ON Taxon.id_level=TaxonLevel.id_level ' \
               'JOIN TaxonStatus ON Taxon.id_status=TaxonStatus.id_status ' \
               f'WHERE TaxonStatus.status_name=? ' \
               'ORDER BY Taxon.id_level ASC, Taxon.taxon_name ASC;'
        return self.execute_query(sSQL, (sStatus,)).fetchall()

    def get_taxon_info(self, sName, sAuthor):
        sSQL = "SELECT Taxon.id_main_taxon, " \
               "MTaxonLevel.level_name AS Main_Taxon_level, " \
               "MainTaxon.taxon_name AS Main_Taxon_name, " \
               "MainTaxon.author AS Main_Taxon_author, " \
               "Taxon.id_level, " \
               "TaxonLevel.level_name, " \
               "Taxon.id_taxon, " \
               "Taxon.taxon_name, " \
               "Taxon.author, " \
               "Taxon.year," \
               "TaxonStatus.status_local_name " \
               "FROM Taxon " \
               "JOIN Taxon MainTaxon " \
               "ON MainTaxon.id_taxon=Taxon.id_main_taxon " \
               "JOIN TaxonLevel " \
               "ON Taxon.id_level=TaxonLevel.id_level " \
               "JOIN TaxonStatus " \
               "ON Taxon.id_status=TaxonStatus.id_status " \
               "JOIN TaxonLevel MTaxonLevel " \
               "ON MTaxonLevel.id_level=MainTaxon.id_level "

        if sAuthor:
            sSQL = f"{sSQL}WHERE Taxon.taxon_name=? AND Taxon.author=? "
            return self.execute_query(sSQL, (sName, sAuthor,)).fetchone()
        else:
            sSQL = f"{sSQL}WHERE Taxon.taxon_name=? " \
                   f"AND Taxon.author is NULL "
            return self.execute_query(sSQL, (sName,)).fetchone()

    def insert_taxon(self, lValues):
        self.insert_row('Taxon', 'id_level, id_main_taxon, '
                        'taxon_name, author, year, id_status',
                        lValues)
