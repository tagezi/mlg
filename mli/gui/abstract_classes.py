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
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QPushButton


class AToolDialogButtons(QDialog):
    """An abstract class that creates a block of Apply, OK, Cancel buttons and
    reserves action methods for them."""

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(AToolDialogButtons, self).__init__(oParent)
        self.oConnector = oConnector
        self.init_UI_button_block()
        self.connect_actions_button()

    def init_UI_button_block(self):
        """ Creates a block of buttons for further use in child dialog classes.
        """
        self.oHLayoutButtons = QHBoxLayout()
        self.oButtonApply = QPushButton(_('Apply'), self)
        self.oButtonApply.setFixedWidth(80)
        self.oButtonOk = QPushButton(_('Ok'), self)
        self.oButtonOk.setFixedWidth(80)
        self.oButtonCancel = QPushButton(_('Cancel'), self)
        self.oButtonCancel.setFixedWidth(80)

        self.oHLayoutButtons.addWidget(self.oButtonApply,
                                       alignment=Qt.AlignRight)
        self.oHLayoutButtons.addWidget(self.oButtonOk)
        self.oHLayoutButtons.addWidget(self.oButtonCancel)

    def connect_actions_button(self):
        """ The method of linking signals and button slots. """
        self.oButtonApply.clicked.connect(self.onClickApply)
        self.oButtonOk.clicked.connect(self.onClickOk)
        self.oButtonCancel.clicked.connect(self.onCancel)

    def onCancel(self):
        """ The method closes the dialog without saving the data. """
        self.close()

    def onClickApply(self):
        """ Reserves the Apply dialog button method for future use. """
        pass

    def onClickOk(self):
        """ The method saves the data and closes the dialog In order for the
        data to be saved, you must override the method onClickApply."""
        self.onClickApply()
        self.close()


if __name__ == '__main__':
    pass
