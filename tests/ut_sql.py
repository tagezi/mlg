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

import unittest
from unittest import TestCase

from mli.lib.sql import *
from mli.lib.str import get_file_patch


def type_connector():
    """ Creates temporal object of sqlite3.Connection and return its type.

        :return: The type sqlite3.Connection.
        """
    oConnector = sqlite3.connect(":memory:")
    return type(oConnector)


def suite():
    oSuite = unittest.TestSuite()
    oSuite.addTest(TestSQLite('test_sql_get_columns'))
    oSuite.addTest(TestSQLite('test_sql__init__'))
    oSuite.addTest(TestSQLite('test_sql_execute'))
    oSuite.addTest(TestSQLite('test_sql_insert_row'))
    oSuite.addTest(TestSQLite('test_sql_select'))
    oSuite.addTest(TestSQLite('test_sql_sql_count'))
    oSuite.addTest(TestSQLite('test_sql_delete_row'))
    oSuite.addTest(TestSQLite('test_sql_sql_get_all'))
    oSuite.addTest(TestSQLite('test_sql_sql_get_id'))
    oSuite.addTest(TestSQLite('test_sql_sql_table_clean'))
    oSuite.addTest(TestSQLite('test_sql_export_db'))

    return oSuite


class TestSQLite(TestCase):
    def setUp(self):
        """ Creates temporal object of sqlite3.Connection for test. """
        file_script = get_file_patch('../../mli/db', 'db_structure.sql')
        self.oConnector = SQL(":memory:")
        sSQL = ''
        with open(file_script, "r") as f:
            for s in f:
                sSQL = sSQL + s

        self.oConnector.execute_script(sSQL)
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        del self.oConnector

    def test_sql_get_columns(self):
        """ Check if the function of separating column work. """
        sString = get_columns('check, check, check')
        sAnswer = 'check=? AND check=? AND check=?'
        self.assertEqual(sString, sAnswer)

        sString = get_columns('check')
        sAnswer = 'check=?'
        self.assertEqual(sString, sAnswer)

    def test_sql__init__(self):
        """ Check if the object being created has an instance of
            the sqlite3.Connection class.
            """
        oInstanceSQL = SQL(":memory:")
        self.assertEqual(type(oInstanceSQL.oConnector), type_connector(), )
        del oInstanceSQL

    def test_sql_execute(self):
        """ Check if execute_script and execute_query work. """
        oCursor = self.oConnector.execute_query('SELECT taxon_lat_name '
                                                'FROM Taxon '
                                                'WHERE taxon_lat_name="Biota"')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'Biota')

    def test_sql_insert_row(self):
        """ Check if insert_row work correctly. """
        bIns = self.oConnector.insert_row('Taxon',
                                          'taxon_lat_name', ('check',))
        self.assertTrue(bIns)

        oCursor = self.oConnector.execute_query('SELECT taxon_lat_name '
                                                'FROM Taxon '
                                                'WHERE taxon_lat_name="check"'
                                                )
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'check')

        bIns = self.oConnector.insert_row('Taxon',
                                          'taxon_lat_name',
                                          ('check_too', 1, 2))
        self.assertFalse(bIns)

    def test_sql_select(self):
        """ Check if select work correctly. """
        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        oCursor = self.oConnector.select('Taxon', 'taxon_lat_name',
                                         'taxon_lat_name', ('check',))
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'check')

        oCursor = self.oConnector.select('Taxon', 'taxon_lat_name')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'Biota')
        self.assertEqual(lRows[1][0], 'Fungi')
        self.assertEqual(lRows[2][0], 'check')

        oCursor = self.oConnector.select('Taxon', '*', sFunc='Count')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 3)

        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        oCursor = self.oConnector.select('Taxon',
                                         'taxon_lat_name', sFunc='DISTINCT')
        lRows = oCursor.fetchall()
        self.assertEqual(lRows[0][0], 'Biota')
        self.assertEqual(lRows[1][0], 'Fungi')
        self.assertEqual(lRows[2][0], 'check')

    def test_sql_delete_row(self):
        """ Check if delete_row work correctly. """
        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        iDel = self.oConnector.delete_row('Taxon',
                                          'taxon_lat_name', ('check',))
        self.assertTrue(iDel)
        oCursor = self.oConnector.select('Taxon', 'taxon_lat_name',
                                         'taxon_lat_name', ('check',))
        lRows = oCursor.fetchall()
        self.assertFalse(lRows)
        oCursor = self.oConnector.select('Taxon', 'taxon_lat_name',
                                         'taxon_lat_name', ('Biota',))
        lRows = oCursor.fetchall()
        self.assertTrue(lRows)

        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        iDel = self.oConnector.delete_row('Taxon')
        self.assertTrue(iDel)
        lRows = self.oConnector.sql_count('Taxon')
        self.assertEqual(lRows, 0)

    # TODO: test for export_db
    def test_sql_export_db(self):
        """ Check if export_db work correctly. """
        pass

    def test_sql_sql_count(self):
        """ Check if sql_count work correctly. """
        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        oCursor = self.oConnector.select('Taxon', '*', sFunc='Count')
        lRowsLow = oCursor.fetchall()
        lRowsAverage = self.oConnector.sql_count('Taxon')
        self.assertEqual(lRowsLow[0][0], lRowsAverage)

    def test_sql_sql_get_all(self):
        """ Check if sql_get_all work correctly. """
        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        oCursor = self.oConnector.select('Taxon', '*')
        lRowsLow = oCursor.fetchall()
        lRowsAverage = self.oConnector.sql_get_all('Taxon')
        self.assertEqual(lRowsLow[0][0], lRowsAverage[0][0])
        self.assertEqual(lRowsLow[1][0], lRowsAverage[1][0])

        lRows = self.oConnector.sql_get_all('Mistake')
        self.assertFalse(lRows)

    def test_sql_sql_get_id(self):
        """ Check if sql_get_id work correctly. """
        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        oCursor = self.oConnector.select('Taxon', 'id_taxon',
                                         'taxon_lat_name', ('check',))
        lRowsLow = oCursor.fetchall()
        lRowsAverage = self.oConnector.sql_get_id('Taxon',
                                                  'id_taxon',
                                                  'taxon_lat_name',
                                                  ('check',))
        self.assertEqual(lRowsLow[0][0], lRowsAverage)

        lRow = self.oConnector.sql_get_id('Mistake', 'id_taxon',
                                          'taxon_lat_name', ('check',))
        self.assertEqual(lRow, 0)

    def test_sql_sql_table_clean(self):
        """ Check if delete_row work correctly. """
        self.oConnector.insert_row('Taxon', 'taxon_lat_name', ('check',))
        iDel = self.oConnector.delete_row('Taxon')
        self.assertTrue(iDel)
        lRows = self.oConnector.sql_count('Taxon')
        self.assertEqual(lRows, 0)

        iDel = self.oConnector.delete_row('Mistake')
        self.assertFalse(iDel)


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
