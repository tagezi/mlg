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

from gettext import gettext as _

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

from mli.gui.abstract_classes import AToolDialogButtons
from mli.gui.dialog_elements import HComboBox, HLineEdit


class ASubstrateDialog(AToolDialogButtons):
    """An abstract class that creates fields and functionality common to all
    dialogs of the substrate. """

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(ASubstrateDialog, self).__init__(oConnector, oParent)
        self.init_UI_failed()

    def init_UI_failed(self):
        """ initiating a dialog view """
        self.oComboSubstrateLevel = HComboBox(_('Old substrate name:'))
        self.oLineEditSubstrate = HLineEdit(_('New substrate name:'))

    def onClickApply(self):
        """ Realization of the abstract method of the parent class. """
        sSubstrate = self.oLineEditSubstrate.get_text()
        bSubstrate = self.oConnector.get_substrate_id(sSubstrate)

        if not bSubstrate:
            self.save_((sSubstrate,))
            self.oLineEditSubstrate.set_text('')

    def save_(self, tValues):
        """ Method for saving information about the substrate in the database.

        :param tValues: Type of substrate to be entered into the database.
        :type tValues: tuple
        """
        self.oConnector.insert_row('Substrate', 'substrate_name', tValues)


class EditSubstrateDialog(ASubstrateDialog):
    """ Dialog window which allows user to change substrate type. """

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(EditSubstrateDialog, self).__init__(oConnector, oParent)
        self.init_UI()

    def init_UI(self):
        """ Creating a dialog window. """
        self.setWindowTitle(_('Edit substrate...'))
        self.setModal(Qt.ApplicationModal)

        self.oComboSubstrateLevel.set_combo_list(
            sorted(self.create_substrate_list('Substrate')))

        oVLayout = QVBoxLayout()
        oVLayout.addLayout(self.oComboSubstrateLevel)
        oVLayout.addLayout(self.oLineEditSubstrate)
        oVLayout.addLayout(self.oHLayoutButtons)
        self.setLayout(oVLayout)

    def create_substrate_list(self, sDB):
        """ Filling the drop-down list with substrate types.

        :param sDB: A name table when information on substrate is saved.
        :type sDB: str
        :return: A list of substrate types.
        :rtype: list[str]
        """
        oCursor = self.oConnector.sql_get_all(sDB)
        lValues = []
        for tRow in oCursor:
            lValues.append(tRow[1])
        return lValues


class NewSubstrateDialog(ASubstrateDialog):
    """ Dialog window which adds new substrate type. """

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(NewSubstrateDialog, self).__init__(oConnector, oParent)
        self.init_UI()

    def init_UI(self):
        """ Creating a dialog window. """
        self.setWindowTitle(_('Add new substrate...'))
        self.setModal(Qt.ApplicationModal)

        oVLayout = QVBoxLayout()
        oVLayout.addLayout(self.oLineEditSubstrate)
        oVLayout.addLayout(self.oHLayoutButtons)
        self.setLayout(oVLayout)


if __name__ == '__main__':
    pass
