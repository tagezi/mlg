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
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from mli.gui.abstract_classes import AToolDialogButtons
from mli.gui.dialog_elements import VComboBox, HLineEdit, VLineEdit
from mli.gui.message_box import warning_no_synonyms, warning_lat_name,\
    warning_this_exist
from mli.lib.str import str_sep_name_taxon


class ATaxonDialog(AToolDialogButtons):
    """ Creates abstract class that contain common elements for Dialogs of
        taxon."""

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(ATaxonDialog, self).__init__(oConnector, oParent)

        self.iOldMainTaxonID = None
        self.sOldMainTaxonName = None
        self.sOldMainTaxonAuthor = None
        self.iOldTaxonRankID = None
        self.sOldTaxonRankName = None
        self.iOldTaxonID = None
        self.sOldTaxonName = None
        self.sOldAuthor = None
        self.sOldYear = None
        self.sOldStatus = None

        self.init_UI()
        self.fill_combobox()
        self.connect_actions()

    def init_UI(self):
        """ initiating a dialog view """
        self.oComboStatus = VComboBox(_('Taxon status:'), 180)
        self.oComboTaxRank = VComboBox(_('Taxon rank:'), 180)
        self.oLineEditLatName = VLineEdit(_('Latin name:'))
        self.oLineEditAuthor = VLineEdit(_('Author:'), 240)
        self.oLineEditYear = VLineEdit(_('Year:'), 50)
        self.oComboTaxNames = VComboBox(_('Taxon name:'), 500)
        self.oComboBoxSynonym = VComboBox(_('Synonym:'), 500)
        self.oComboMainTaxon = VComboBox(_('Main taxon:'), 500)
        self.oLineEditLocaleName = VLineEdit(_('Local name:'))

        oHLayoutAuthor = QHBoxLayout()
        oHLayoutAuthor.addLayout(self.oLineEditAuthor)
        oHLayoutAuthor.addStretch()
        oHLayoutAuthor.addLayout(self.oLineEditYear)

        oVLayoutRank = QVBoxLayout()
        oVLayoutRank.addLayout(self.oComboTaxRank)
        oVLayoutRank.addLayout(self.oComboStatus)

        oVLayoutTaxon = QVBoxLayout()
        oVLayoutTaxon.addLayout(self.oLineEditLatName)
        oVLayoutTaxon.addLayout(oHLayoutAuthor)

        self.oHLayoutTaxon = QHBoxLayout()
        self.oHLayoutTaxon.addLayout(oVLayoutRank)
        self.oHLayoutTaxon.addLayout(oVLayoutTaxon)

    def connect_actions(self):
        """ Connects buttons with actions they should perform. """
        (self.oComboMainTaxon.get_widget()).currentTextChanged.connect(
            self.onCurrentMainTaxonChanged)

    def clean_field(self):
        """ Clears all fields after use. """
        self.oComboMainTaxon.clear_list()
        self.oComboTaxRank.clear_list()
        self.oComboStatus.clear_list()
        self.oLineEditLatName.set_text('')
        self.oLineEditAuthor.set_text('')
        self.oLineEditYear.set_text('')
        self.oLineEditLocaleName.set_text('')
        self.oComboTaxNames.clear_list()

    def create_level_list(self, sTaxon='', bGetAll=None):
        """ Generates a list of taxon levels depending on a condition. At the
        first list initialization and using button Apply, all taxon levels are
        collected, at choosing Main taxon, only those that are below the
        selected taxon name.

        :param sTaxon: A name of main taxon.
        :type sTaxon: str
        :param bGetAll: It is needed to choose all levels.
        :type bGetAll: bool
        :return: list of taxon levels.
        :rtype: list[str]
        """
        oCursor = self.oConnector.sql_get_all('TaxonLevel')
        lRanks, lValues = [], []
        for tRow in oCursor:
            lValues.append(tRow[3])

        if bGetAll is None:
            sRankMainTaxon = sTaxon.split('(')[1].split(')')[0]
            sRow = lValues[0]
            while sRow != sRankMainTaxon:
                lValues.pop(0)
                sRow = lValues[0]
        lRanks = lValues
        lRanks.pop(0)

        return lRanks

    def create_status_list(self):
        """ Creates a list of statuses.

        :return: list[str]
        """
        tRows = self.oConnector.get_statuses()
        lList = []
        for Row in tRows:
            lList.append(Row[3])

        return lList

    def create_taxon_list(self):
        """ Creates a list of taxon names for further use in dialog elements.

        :return: A list in form - (Taxon Rank) Taxon Name
        :type: list[str]
        """
        lValues = []
        tRows = self.oConnector.get_taxon_list('ACCEPTED')

        for tRow in tRows:
            if tRow[3]:
                lValues.append(f'({tRow[1]}) {tRow[2]}, {tRow[3]}')
            else:
                lValues.append(f'({tRow[1]}) {tRow[2]}')
        return lValues

    def fill_combobox(self):
        """ Fills the fields with the drop-down list during the first
        initialization and after applying the Apply button."""
        lStatuses = self.create_status_list()
        self.oComboStatus.set_combo_list(lStatuses)
        self.oComboTaxRank.set_text(lStatuses[1])
        lTaxonRank = self.create_level_list(bGetAll=True)
        self.oComboTaxRank.set_combo_list(lTaxonRank)
        self.oComboTaxRank.set_text(lTaxonRank[0])
        self.oComboMainTaxon.set_combo_list(self.create_taxon_list())
        self.oComboTaxNames.set_combo_list(self.create_taxon_list())

    def fill_form(self, sSciName):
        if not sSciName:
            return

        sName, sAuthor = str_sep_name_taxon(sSciName)
        if sName == 'Biota':
            return

        lRow = self.oConnector.get_taxon_info(sName, sAuthor)
        self.iOldMainTaxonID = lRow[0]
        sOldMainTaxonRankName = lRow[1]
        self.sOldMainTaxonName = lRow[2]
        self.sOldMainTaxonAuthor = lRow[3]
        self.iOldTaxonRankID = lRow[4]
        self.sOldTaxonRankName = lRow[5]
        self.iOldTaxonID = lRow[6]
        self.sOldTaxonName = lRow[7]
        self.sOldAuthor = lRow[8]
        iOldYear = lRow[9]
        self.sOldStatus = lRow[10]

        if not iOldYear:
            self.sOldYear = ''
        else:
            self.sOldYear = str(iOldYear)

        sMainTaxon = f'({sOldMainTaxonRankName}) {self.sOldMainTaxonName}'
        if self.sOldMainTaxonAuthor:
            sMainTaxon = f'{sMainTaxon}, {self.sOldMainTaxonAuthor}'

        self.oComboMainTaxon.set_text(sMainTaxon)
        self.oComboTaxRank.set_text(self.sOldTaxonRankName)
        self.oLineEditLatName.set_text(self.sOldTaxonName)
        self.oLineEditAuthor.set_text(self.sOldAuthor)
        self.oLineEditYear.set_text(self.sOldYear)
        self.oComboStatus.set_text(self.sOldStatus)

    def onClickApply(self):
        sMainTaxon = self.oComboMainTaxon.get_text()
        sTaxonRank = self.oComboTaxRank.get_text()
        sLatName = self.oLineEditLatName.get_text()
        sAuthor = self.oLineEditAuthor.get_text()
        sYear = self.oLineEditYear.get_text()
        sStatus = self.oComboStatus.get_text()

        if not sLatName and not sLatName.isalpha() and not sLatName.isascii():
            warning_lat_name()
            return

        if self.sOldTaxonName != sLatName:
            self.save_('taxon_name', sLatName, self.iOldTaxonID)

        sMainTaxonName, sMainTaxonAuthor = str_sep_name_taxon(sMainTaxon)
        if sMainTaxonName != self.sOldMainTaxonName:
            iMainTaxonID = self.oConnector.get_taxon_id(sMainTaxonName,
                                                        sMainTaxonAuthor)
            self.save_('id_main_taxon', iMainTaxonID, self.iOldTaxonID)

        if sTaxonRank != self.sOldTaxonRankName:
            iRankID = self.oConnector.get_level_id('level_name', sTaxonRank)
            self.save_('id_level', iRankID, self.iOldTaxonID)

        if sAuthor and sAuthor != self.sOldAuthor:
            self.save_('author', sAuthor, self.iOldTaxonID)

        if sYear and sYear != self.sOldYear:
            self.save_('year', sYear, self.iOldTaxonID)

        if sStatus != self.sOldStatus:
            iStatusID = self.oConnector.get_status_id(sStatus)
            self.save_('id_status', iStatusID, self.iOldTaxonID)

        self.clean_field()
        self.fill_combobox()

    def onCurrentMainTaxonChanged(self, sTaxon=''):
        """ The slot that should fire after the taxon name in the Main taxon
        drop-down list.

        :param sTaxon: A name of main taxon.
        :type sTaxon: str
        """
        # If the user enters the name by hand, there will be an error.
        if sTaxon.find("(") >= 0 and sTaxon.find(")") > 1:
            lTaxonRank = self.create_level_list(sTaxon)
            self.oComboTaxRank.clear_list()
            self.oComboTaxRank.set_combo_list(lTaxonRank)
            self.oComboTaxRank.set_text(lTaxonRank[0])

    def save_(self, sSetCol, sUpdate, sWhere,
              sTable='Taxon', sWhereCol='id_taxon'):

        tValues = (sUpdate, sWhere,)
        self.oConnector.update(sTable, sSetCol, sWhereCol, tValues)


class EditSynonymDialog(ATaxonDialog):
    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(EditSynonymDialog, self).__init__(oConnector, oParent)

        self.lSynonym = None
        self.iTaxonID = None

    def init_UI(self):
        """ Creating a dialog window. """
        super().init_UI()
        self.setWindowTitle(_('Editing an existing taxon'))
        self.setModal(Qt.ApplicationModal)

        self.oLineEditLatName.set_label(_('New synonym name:'))
        self.oComboMainTaxon.set_text(_('New main taxon:'))

        oVLayout = QVBoxLayout()
        oVLayout.addLayout(self.oComboTaxNames)
        oVLayout.addLayout(self.oComboBoxSynonym)
        oVLayout.addLayout(self.oComboMainTaxon)
        oVLayout.addLayout(self.oHLayoutTaxon)
        oVLayout.addLayout(self.oHLayoutButtons)
        self.setLayout(oVLayout)

    def connect_actions(self):
        super().connect_actions()
        (self.oComboTaxNames.get_widget()).currentTextChanged.connect(
            self.onCurrentTaxonNamesChanged)
        self.oComboBoxSynonym.get_widget().currentTextChanged.connect(
            self.onCurrentSynonymChanged)

    def onCurrentSynonymChanged(self, sSynonym):
        self.fill_form(sSynonym)

    def onCurrentTaxonNamesChanged(self, sTaxonName):
        sName, sAuthor = str_sep_name_taxon(sTaxonName)
        self.iTaxonID = self.oConnector.get_taxon_id(sName, sAuthor)

        tSynonyms = self.oConnector.get_synonyms(self.iTaxonID)
        if not tSynonyms:
            if not sTaxonName or sName == 'Biota':
                return
            if sAuthor:
                warning_no_synonyms(f'{sName}, {sAuthor}')
            else:
                warning_no_synonyms(f'{sName}')
            return

        lSynonyms = []
        for lRow in tSynonyms:
            lSynonyms.append(f'({lRow[0]}) {lRow[1]}, {lRow[2]}')

        self.oComboBoxSynonym.set_combo_list(lSynonyms)


class EditTaxonDialog(ATaxonDialog):
    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(EditTaxonDialog, self).__init__(oConnector, oParent)

    def init_UI(self):
        """ Creating a dialog window. """
        super().init_UI()
        self.setWindowTitle(_('Editing of a taxon'))
        self.setModal(Qt.ApplicationModal)

        oVLayout = QVBoxLayout()
        oVLayout.addLayout(self.oComboTaxNames)
        oVLayout.addLayout(self.oComboMainTaxon)
        oVLayout.addLayout(self.oHLayoutTaxon)
        oVLayout.addLayout(self.oHLayoutButtons)
        self.setLayout(oVLayout)

    def connect_actions(self):
        super().connect_actions()
        (self.oComboTaxNames.get_widget()).currentTextChanged.connect(
            self.onCurrentTaxonNamesChanged)

    def onCurrentTaxonNamesChanged(self, sTaxonName):
        self.fill_form(sTaxonName)


class NewTaxonDialog(ATaxonDialog):
    """ Dialog window which adds information on new taxon. """

    def __init__(self, oConnector, oParent=None):
        """ Initiating a class. """
        super(NewTaxonDialog, self).__init__(oConnector, oParent)

    def init_UI(self):
        """ Creating a dialog window. """
        super().init_UI()
        self.setWindowTitle(_('Add new taxon to tree'))
        self.setModal(Qt.ApplicationModal)

        oVLayout = QVBoxLayout()
        oVLayout.addLayout(self.oComboMainTaxon)
        oVLayout.addLayout(self.oHLayoutTaxon)
        oVLayout.addLayout(self.oHLayoutButtons)
        self.setLayout(oVLayout)

    def onClickApply(self):
        """ Actions to be taken when adding a new taxon. """
        sRank = self.oComboTaxRank.get_text()
        sMainTaxon, sMAuthor = \
            str_sep_name_taxon(self.oComboMainTaxon.get_text())
        sName = self.oLineEditLatName.get_text()
        sAuthor = self.oLineEditAuthor.get_text()
        iYear = self.oLineEditYear.get_text()
        sStatus = self.oComboStatus.get_text()

        if not sName and sName.isalpha() and sName.isascii():
            warning_lat_name()
            return

        bTaxonName = self.oConnector.get_taxon_id(sName, sAuthor)

        if sName and bTaxonName:
            warning_this_exist(_('taxon name'), f'<i>{sName}</i>, {sAuthor}')
            return

        if sName and not bTaxonName:
            iRank = self.oConnector.get_level_id('level_name', sRank)
            iStatus = self.oConnector.get_status_id(sStatus)
            iMainTax = self.oConnector.get_taxon_id(sMainTaxon, sMAuthor)
            tValues = (iRank, iMainTax, sName, sAuthor, iYear, iStatus,)

            self.oConnector.insert_taxon(tValues)

            self.clean_field()
            self.fill_combobox()


if __name__ == '__main__':
    pass
