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

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QComboBox, QCompleter, \
    QInputDialog, QMainWindow, QTextBrowser

from mli.gui.color_dialogs import NewColor, EditColor
from mli.gui.file_dialogs import OpenFileDialog
from mli.gui.substract_dialogs import EditSubstrateDialog, NewSubstrateDialog
from mli.gui.help_dialog import About
from mli.gui.setting_dialog import SettingDialog
from mli.gui.tab_widget import CentralTabWidget
from mli.gui.table_widget import TableWidget
from mli.gui.taxon_dialogs import EditTaxonDialog, EditSynonymDialog,\
    NewTaxonDialog
from mli.gui.taxon_info import TaxonBrowser

from mli.lib.config import ConfigProgram
from mli.lib.sql import SQL, check_connect_db
from mli.lib.str import str_get_file_patch, str_get_path


class MainWindow(QMainWindow):
    def __init__(self, sPath):
        super().__init__()

        self.sPathApp = sPath
        oConfigProgram = ConfigProgram(self.sPathApp)
        sBasePath = oConfigProgram.sDir
        sDBPath = oConfigProgram.get_config_value('DB', 'db_path')
        sDBDir = oConfigProgram.get_config_value('DB', 'db_dir')
        if not sDBPath:
            sDBFile = oConfigProgram.get_config_value('DB', 'db_file')
            sDBPath = str_get_file_patch(sBasePath, sDBDir)
            sDBPath = str_get_file_patch(sDBPath, sDBFile)

        self.oConnector = SQL(sDBPath)
        check_connect_db(self.oConnector, sBasePath, sDBDir)

        self.setWindowTitle(_('Manual Lichen identification'))
        self.oCentralWidget = CentralTabWidget(self, 'Tab 1')
        self.create_actions()
        self.connect_actions()
        self.set_menu_bar()
        self.setCentralWidget(self.oCentralWidget)
        self.onSetStatusBarMessage()

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
        self.oFind = QAction(_('Find...'), self)
        self.oFind.setShortcut('Ctrl+F')
        self.oNewTaxon = QAction(_('&New taxon...'))
        self.oEditTaxon = QAction(_('&Edit taxon...'))
        self.oEditSynonym = QAction(_('Edit synonym taxon...'))
        self.oNewColor = QAction(_('New color...'))
        self.oNewColorsTaxon = QAction(_('New color for taxon...'))
        self.oEditColor = QAction(_('Edit color...'))
        self.oEditColorsTaxon = QAction(_('Edit colors of taxon...'))
        self.oNewSubstrate = QAction(_('New substrate...'))
        self.oEditSubstrate = QAction(_('Edit substrate...'))

        # Tools
        self.oTaxonInfo = QAction(_('Information on Taxon...'))

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
        oTaxa = oEdit.addMenu(_('Taxa'))
        oTaxa.addAction(self.oNewTaxon)
        oTaxa.addAction(self.oEditTaxon)
        oTaxa.addAction(self.oEditSynonym)

        oColor = oEdit.addMenu(_('Color'))
        oColor.addAction(self.oNewColor)
        oColor.addAction(self.oEditColor)
        oEdit.addSeparator()
        oColor.addAction(self.oNewColorsTaxon)
        oColor.addAction(self.oEditColorsTaxon)

        oSubstrates = oEdit.addMenu(_('Substrates'))
        oSubstrates.addAction(self.oNewSubstrate)
        oSubstrates.addAction(self.oEditSubstrate)
        oEdit.addSeparator()
        oEdit.addAction(self.oFind)

        # Create Tool menu
        oTools = oMenuBar.addMenu(_('&Tools'))
        oTools.addAction(self.oTaxonInfo)

        # Create Help menu
        oHelpMenu = oMenuBar.addMenu(_('&Help'))
        oHelpMenu.addAction(self.oOpenHelp)
        oHelpMenu.addAction(self.oAbout)

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
        self.oEditSynonym.triggered.connect(self.onEditSynonym)
        self.oNewColor.triggered.connect(self.onNewColor)
        self.oEditColor.triggered.connect(self.onEditColor)
        self.oNewColorsTaxon.triggered.connect(self.onNewColorTaxon)
        self.oEditColorsTaxon.triggered.connect(self.onEditColorTaxon)
        self.oNewSubstrate.triggered.connect(self.onNewSubstrate)
        self.oEditSubstrate.triggered.connect(self.onEditSubstrate)

        # Tool menu
        self.oTaxonInfo.triggered.connect(self.onTaxonInfo)

        # Menu Help
        self.oAbout.triggered.connect(self.onDisplayAbout)

    def get_page_taxon_info(self, sTaxonName):
        return TaxonBrowser(self.oConnector, sTaxonName)

    def get_taxon_list(self):
        lValues = []
        tTaxonList = self.oConnector.get_full_taxon_list()

        for tRow in tTaxonList:
            if tRow[1]:
                lValues.append(f'{tRow[0]}, {tRow[1]}')
            else:
                lValues.append(f'{tRow[0]}')
        return lValues

    def onDisplayAbout(self):
        """ Method open dialog window with information about the program. """
        oAbout = About(self)
        oAbout.exec_()

    def onOpenDB(self):
        pass

    def onOpenSetting(self):
        oSettingDialog = SettingDialog(self.oConnector, self.sPathApp, self)
        oSettingDialog.exec_()

    def onEditColor(self):
        oEditColor = EditColor(self.oConnector, self)
        oEditColor.exec_()

    def onEditColorTaxon(self):
        pass

    def onEditSubstrate(self):
        oEditSubstrate = EditSubstrateDialog(self.oConnector, self)
        oEditSubstrate.exec_()

    def onEditSynonym(self):
        oEditSynonym = EditSynonymDialog(self.oConnector, self)
        oEditSynonym.exec_()

    def onEditTaxon(self):
        oEditTaxonDialog = EditTaxonDialog(self.oConnector, self)
        oEditTaxonDialog.exec_()

    def onNewColor(self):
        oNewColor = NewColor(self.oConnector, self)
        oNewColor.exec_()

    def onNewColorTaxon(self):
        pass

    def onNewSubstrate(self):
        oNewSubstrate = NewSubstrateDialog(self.oConnector, self)
        oNewSubstrate.exec_()

    def onNewTaxon(self):
        oNewTaxonDialog = NewTaxonDialog(self.oConnector, self)
        oNewTaxonDialog.exec_()

    def onTaxonInfo(self):
        lTaxonList = self.get_taxon_list()
        oInputDialog = QInputDialog(self)
        oInputDialog.setWindowTitle('Taxon choosing')
        oInputDialog.setLabelText(_('Taxon list:'))
        oInputDialog.setComboBoxItems(lTaxonList)
        oInputDialog.setComboBoxEditable(True)
        oComboBox = oInputDialog.findChild(QComboBox)
        if oComboBox is not None:
            oCompleter = QCompleter(lTaxonList, oComboBox)
            oComboBox.setCompleter(oCompleter)

        ok = oInputDialog.exec_()
        if ok:
            sTaxonName = oInputDialog.textValue()
            oTaxonInfo = self.get_page_taxon_info(sTaxonName)
            self.oCentralWidget.add_tab(oTaxonInfo, sTaxonName)

    def onSetStatusBarMessage(self, sMassage='Ready'):
        """ Method create Status Bar on main window of program GUI. """
        self.statusBar().showMessage(sMassage)
