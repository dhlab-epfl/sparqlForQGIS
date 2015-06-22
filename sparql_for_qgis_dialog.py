# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SparqlForQGISDialog
                                 A QGIS plugin
 Display and update data from Sparql queries
                             -------------------
        begin                : 2015-06-22
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Olivier Dalang
        email                : olivier.dalang@epfl.ch
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'sparql_for_qgis_dialog_base.ui'))


class SparqlForQGISDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(SparqlForQGISDialog, self).__init__(parent)

        self.setupUi(self)
