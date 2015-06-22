# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SparqlForQGIS
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
# Import the code for the dialog
from sparql_for_qgis_dialog import SparqlForQGISDialog
import os.path


class SparqlForQGIS:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.dlg = SparqlForQGISDialog()
        self.toolbar = self.iface.addToolBar(u'SparqlForQGIS')

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.action = QAction( QIcon(os.path.join(self.plugin_dir,'icon.png')), 'SparqlForQGIS', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.toolbar.addAction(self.action)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self.iface.removeToolBarIcon(self.action)
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""

        self.dlg.show()
        result = self.dlg.exec_()

        if result:
            pass

