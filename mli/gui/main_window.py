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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, qApp

from mli.gui.file_dialogs import OpenFileDialog
from mli.gui.help_dialog import About
from mli.gui.setting_dialog import SettingDialog
from mli.gui.taxon_dialogs import EditTaxonDialog, NewTaxonDialog
from mli.lib.sql import SQL


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        sTitleProgram = _('Manual Lichen identification')
        self.setWindowTitle(sTitleProgram)

        self.create_actions()
        self.connect_actions()
        self.set_menu_bar()

        self.showMaximized()

    def create_actions(self):
        """ Method collect all actions which can do from GUI of program. """
        # File menu
        self.oOpenDB = QAction(_('Open &DataBase...'), self)
        self.oPrint = QAction(_('P&rint...'))
        self.oSetting = QAction(_('&Setting...'))
        self.oExitAct = QAction(QIcon.fromTheme('SP_exit'), _('&Exit'), self)
        self.oExitAct.setShortcut('Ctrl+Q')
        self.oExitAct.setStatusTip(_('Exit application'))

        # Edit
        self.oUndo = QAction(_('Undo'), self)
        self.oUndo.setShortcut('Ctrl+Z')
        self.oRedo = QAction(_('Redo'), self)
        self.oRedo.setShortcut('Ctrl+Z')
        self.oNewTaxon = QAction(_('&New taxon...'))
        self.oEditTaxon = QAction(_('&Edit taxon...'))
        self.oFind = QAction(_('Find...'), self)
        self.oFind.setShortcut('Ctrl+F')

        # Help
        self.oOpenHelp = QAction(_('&Help'), self)
        self.oAbout = QAction(_('&About'), self)

    def set_menu_bar(self):
        """ Method create Menu Bar on main window of program GUI. """
        oMenuBar = self.menuBar()

        # Create file menu
        oFileMenu = oMenuBar.addMenu(_('&File'))
        oFileMenu.addAction(self.oOpenDB)
        oFileMenu.addSeparator()
        oFileMenu.addAction(self.oPrint)
        oFileMenu.addSeparator()
        oFileMenu.addAction(self.oSetting)
        oFileMenu.addSeparator()
        oFileMenu.addAction(self.oExitAct)

        # Create Edit menu
        oEdit = oMenuBar.addMenu(_('&Edit'))
        oEdit.addAction(self.oUndo)
        oEdit.addAction(self.oRedo)
        oEdit.addSeparator()
        oEdit.addAction(self.oNewTaxon)
        oEdit.addAction(self.oEditTaxon)
        oEdit.addSeparator()
        oEdit.addAction(self.oFind)

        # Create View menu
        oView = oMenuBar.addMenu(_('&View'))

        # Create Run menu
        oView = oMenuBar.addMenu(_('&Run'))

        # Create Tool menu
        oTools = oMenuBar.addMenu(_('&Tools'))

        # Create Help menu
        oHelpMenu = oMenuBar.addMenu(_('&Help'))
        oHelpMenu.addAction(self.oOpenHelp)
        oHelpMenu.addAction(self.oAbout)

    def set_status_bar(self, sMassage='Ready'):
        """ Method create Status Bar on main window of program GUI. """
        self.oStatusBar = self.statusBar().showMessage(sMassage)

    def connect_actions(self):
        """ It is PyQt5 slots or other words is connecting from GUI element to
        method or function in program. """
        # Menu File
        self.oOpenDB.triggered.connect(self.onOpenDB)
        self.oSetting.triggered.connect(self.onOpenSetting)
        self.oExitAct.triggered.connect(qApp.quit)

        # Menu Edit
        self.oNewTaxon.triggered.connect(self.onNewTaxon)
        self.oEditTaxon.triggered.connect(self.onEditTaxon)
        # Menu Help
        self.oAbout.triggered.connect(self.onDisplayAbout)

    def onDisplayAbout(self):
        """ Method open dialog window with information about the program. """
        oAbout = About(self)
        oAbout.exec_()

    def onOpenDB(self):
        dParameter = {'name': _('Open Database'),
                      'filter': _('DB file (*.db)')}
        oOpenDBFile = OpenFileDialog(self, dParameter)
        sFileNameDB = oOpenDBFile.exec()
        if sFileNameDB is not None:
            sFilePath = sFileNameDB[0]
            self.oConnector = SQL(str(sFilePath))
            self.oComboBoxSets.set_connector(self.oConnector)
            self.oComboBoxSets.update_combobox()

    def onOpenSetting(self):
        oSettingDialog = SettingDialog(self)
        oSettingDialog.exec_()

    def onEditTaxon(self):
        oEditTaxonDialog = EditTaxonDialog(self)
        oEditTaxonDialog.exec_()

    def onNewTaxon(self):
        oNewTaxonDialog = NewTaxonDialog(self)
        oNewTaxonDialog.exec_()
