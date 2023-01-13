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

import unittest

from mli.lib.str import str_sep_name_taxon


def suite():
    oSuite = unittest.TestSuite()
    oSuite.addTest(TestStr('test_str_sep_name_taxon'))

    return oSuite


class TestStr(unittest.TestCase):
    def test_str_sep_name_taxon(self):
        """ Check if str_sep_name_taxon work correctly. """
        sTestValue = '(kingdom) Fungi R.T.Moore'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Fungi R.T.Moore')

        sTestValue = '(species) Absconditella modesta (Zahlbr.) Vĕzda'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Absconditella modesta (Zahlbr.) Vĕzda')

        sTestValue = '(species) Acanthotrema martini ' \
                     '(Sogandares) Lafuente, Roca & Carbonell'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Acanthotrema martini (Sogandares) '
                                 'Lafuente, Roca & Carbonell')

        sTestValue = '(species) Acanthotheciopsis caesiocarnea'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Acanthotheciopsis caesiocarnea')

        sTestValue = 'Fungi R.T.Moore'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Fungi R.T.Moore')

        sTestValue = 'Absconditella modesta (Zahlbr.) Vĕzda'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Absconditella modesta (Zahlbr.) Vĕzda')

        sTestValue = 'Acanthotrema martini ' \
                     '(Sogandares) Lafuente, Roca & Carbonell'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Acanthotrema martini (Sogandares) '
                                 'Lafuente, Roca & Carbonell')

        sTestValue = 'Acanthotheciopsis caesiocarnea'
        sTaxon = str_sep_name_taxon(sTestValue)
        self.assertEqual(sTaxon, 'Acanthotheciopsis caesiocarnea')


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
