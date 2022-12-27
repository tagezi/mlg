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

from PyQt5.QtWidgets import QWidget, QTextBrowser, QVBoxLayout

from mli.lib.gbif_parser import gbif_get_id_from_gbif
from mli.lib.str import str_sep_name_taxon


def get_name_string(sName, sAuthor):
    if sAuthor:
        return f'<i>{sName}</i>, {sAuthor}'
    else:
        return f'<i>{sName}</i>'


class TaxonBrowser(QWidget):
    def __init__(self, oConnector, sNameTaxon):
        super().__init__()

        self.oConnector = oConnector
        self.sNameTaxon = sNameTaxon

        self.initUI()

    def initUI(self):
        oTextBrowser = QTextBrowser()
        oTextBrowser.setOpenExternalLinks(True)
        oTextBrowser.setText(self.get_page_taxon_info())

        oBox = QVBoxLayout()
        oBox.addWidget(oTextBrowser)
        self.setLayout(oBox)

    def get_page_taxon_info(self):
        sNoData = _('There is no data.')
        sName, sAuthor = str_sep_name_taxon(self.sNameTaxon)
        iStatusID, sStatusName = \
            self.oConnector.get_status_taxon(sName, sAuthor)
        iLevelID, sLevelName = self.oConnector.get_level_taxon(sName, sAuthor)
        iTaxonID = self.oConnector.get_taxon_id(sName, sAuthor, iStatusID)
        sHTML = f'<h2>({sLevelName}) {get_name_string(sName, sAuthor)}</h2>'
        if iStatusID != 1:
            sIS = _(" is synonym of ")
            iMainID, sMainName, sMainAuthor = \
                self.oConnector.get_main_taxon((sName, sAuthor,))
            sHTML = f'{sHTML}{get_name_string(sName, sAuthor)} {sIS}' \
                    f'{get_name_string(sMainName, sMainAuthor)}'

        sHTML = f'{sHTML}<h3>{_("Status:")}</h3>'
        sHTML = f'{sHTML} {sStatusName}'
        if iStatusID == 1:
            lSynonyms = self.oConnector.get_synonyms(iTaxonID)
            if lSynonyms:
                sHTML = f'{sHTML}<h3>{_("Synonyms:")}</h3>'
                for sLevel, sName, sAuthor in lSynonyms:
                    sHTML = f'{sHTML} ({sLevel}) ' \
                            f'{get_name_string(sName, sAuthor)}<br>'

            sHTML = f'{sHTML}<h3>{_("Description:")}</h3>'
            sHTML = f'{sHTML} ({sNoData}) '
            sHTML = f'{sHTML}<h3>{_("Children:")}</h3>'
            lChildren = self.oConnector.get_taxon_children(iTaxonID, sStatusName)
            if lChildren:
                for sLevel, sName, sAuthor in lChildren:
                    sHTML = f'{sHTML} ({sLevel}) ' \
                            f'{get_name_string(sName, sAuthor)}<br>'
            else:
                sHTML = f'{sHTML} ({sNoData}) '

        sHTML = f'{sHTML}<h3>{_("Database links:")}</h3>'
        lTaxonDB = self.oConnector.get_taxon_db_link(iTaxonID)
        if lTaxonDB:
            for sSource, sLink, sIndex in lTaxonDB:
                sHTML = f'{sHTML} {sSource}: ' \
                        f'<a href="{sLink}{sIndex}">{sIndex}</a> '
        else:
            sLevelDB = \
                self.oConnector.get_level_name('level_en_name', iLevelID)[0][0]
            sTaxonGBIF = gbif_get_id_from_gbif(self.sNameTaxon, sLevelDB)

            sColumns = 'id_taxon, id_source, taxon_index'
            tValues = (iTaxonID, 12, sTaxonGBIF)
            self.oConnector.insert_row('DBIndexes', sColumns, tValues)

            lTaxonDB = self.oConnector.get_taxon_db_link(iTaxonID)
            for sSource, sLink, sIndex in lTaxonDB:
                sHTML = f'{sHTML} {sSource}: ' \
                        f'<a href="{sLink}{sIndex}">{sIndex}</a> '

        sHTML = f'{sHTML}<h3>{_("References to literature:")}</h3>'
        sHTML = f'{sHTML} ({sNoData}) '

        return sHTML


if __name__ == '__main__':
    pass
