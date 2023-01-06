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

from gettext import gettext as _
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout

from mli.gui.dialog_elements import ADialogApplyButtons, HComboBox, HLineEdit
from mli.gui.message_box import warning_this_exist


class AColor(ADialogApplyButtons):
    """An abstract class that creates fields and functionality common to all
    dialogs of color. """

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(AColor, self).__init__(oConnector, oParent)
        self.init_UI()

    def init_UI(self):
        """ initiating a dialog view """
        self.oComboColors = HComboBox(_('Old color name:'))
        self.oLineEditColor = HLineEdit(_('New color name:'))
        self.oLineEditHEXCode = HLineEdit(_('HEX code of color:'), 200)

    def onClickApply(self):
        """ Realization of the abstract method of the parent class. """
        pass

    def save_(self, tValues):
        """ Method for saving information about a color in the database.

        :param tValues: Type of color to be entered into the database.
        :type tValues: tuple
        """
        self.oConnector.insert_row('Colors', 'color_local_name', tValues)


class EditColor(AColor):
    """ Dialog window which allows user to change color type. """

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(EditColor, self).__init__(oConnector, oParent)

    def init_UI(self):
        """ Creating a dialog window. """
        super().init_UI()
        self.setWindowTitle(_('Edit color.'))
        self.setModal(Qt.ApplicationModal)

        self.oComboColors.set_combo_list(
            sorted(self.create_colors_list('Colors')))

        oVLayout = QVBoxLayout()
        oVLayout.addLayout(self.oComboColors)
        oVLayout.addLayout(self.oLineEditColor)
        oVLayout.addLayout(self.oHLayoutButtons)
        self.setLayout(oVLayout)

    def create_colors_list(self, sDB):
        """ Filling the drop-down list with color.

        :param sDB: A name table when information on color is saved.
        :type sDB: str
        :return: A list of color types.
        :rtype: list[str]
        """
        oCursor = self.oConnector.sql_get_all(sDB)
        lValues = []
        for tRow in oCursor:
            lValues.append(tRow[1])
        return lValues

    def onClickApply(self):
        """ Realization of the abstract method of the parent class. """
        # OldName
        sColor = self.oLineEditColor.get_text()
        sHEXCode = self.oLineEditHEXCode.get_text()

        bColor = self.oConnector.get_color_id_by_name(sColor)
        if bColor:
            warning_this_exist('color', sColor)
            return

        bHEX = self.oConnector.get_color_id_by_hex(sHEXCode)
        if bHEX:
            warning_this_exist('color', sColor)
            return

        self.save_((sColor,))
        self.oLineEditColor.set_text('')


class NewColor(AColor):
    """ Dialog window which adds new color. """

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(NewColor, self).__init__(oConnector, oParent)

    def init_UI(self):
        """ Creating a dialog window. """
        super().init_UI()
        self.setWindowTitle(_('Add new color.'))
        self.setModal(Qt.ApplicationModal)

        oVLayout = QVBoxLayout()
        oVLayout.addLayout(self.oLineEditColor)
        oVLayout.addLayout(self.oLineEditHEXCode)
        oVLayout.addLayout(self.oHLayoutButtons)
        self.setLayout(oVLayout)

    def onClickApply(self):
        """ Realization of the abstract method of the parent class. """
        sColor = self.oLineEditColor.get_text()
        sHEXCode = self.oLineEditHEXCode.get_text()

        bColor = self.oConnector.get_color_id_by_name(sColor)
        if bColor:
            warning_this_exist('color', sColor)
            return

        bHEX = self.oConnector.get_color_id_by_hex(sHEXCode)
        if bHEX:
            warning_this_exist('color', sColor)
            return

        self.save_((sColor,))
        self.oLineEditColor.set_text('')


if __name__ == '__main__':
    pass
