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

from qgis.core import *

from SparqlLayer import SparqlLayer
from sparql_for_qgis_dialog import SparqlForQGISDialog

import os.path

class SparqlForQGIS:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.toolbar = self.iface.addToolBar(u'SparqlForQGIS')

        self.layers = []

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        self.action = QAction( QIcon(os.path.join(self.plugin_dir,'icon.png')), 'SparqlForQGIS', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.toolbar.addAction(self.action)

        self.updateAllAction = QAction( QIcon(os.path.join(self.plugin_dir,'icon_refresh_all.png')), 'Update all Sparql layer', self.iface.mainWindow())
        self.updateAllAction.triggered.connect(self.updateAll)
        self.toolbar.addAction(self.updateAllAction)

        self.updateOneAction = QAction( QIcon(os.path.join(self.plugin_dir,'icon_refresh_one.png')), 'Update one Sparql layers', self.iface.mainWindow())
        self.updateOneAction.triggered.connect(self.updateOne)
        self.toolbar.addAction(self.updateOneAction)

        QgsProject.instance().readProject.connect(self.readSettings)

        self.readSettings(None)


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        QgsProject.instance().readProject.disconnect(self.readSettings)

        for layer in self.layers:
            layer.unload()

        #self.iface.removeToolBarIcon(self.action)
        del self.toolbar





        
    def readSettings(self, qDomDocument):
        QgsMessageLog.logMessage('reading settings')

        for layer in self.layers:
            layer.unload()

        self.layers = []

        layersNames,ok = QgsProject.instance().readListEntry('SparqlForQGIS','LayersNames')
        layersUrl,ok = QgsProject.instance().readListEntry('SparqlForQGIS','LayersUrl')
        layersDisplaySparql,ok = QgsProject.instance().readListEntry('SparqlForQGIS','LayersDisplaySparql')
        layersUpdateSparql,ok = QgsProject.instance().readListEntry('SparqlForQGIS','LayersUpdateSparql')

        for i in range(0, len(layersNames)):
            self.layers.append( SparqlLayer( self, layersNames[i], layersUrl[i], layersDisplaySparql[i], layersUpdateSparql[i] ) )

    def run(self):
        """Run method that performs all the real work"""

        dlg = SparqlForQGISDialog(self)

        dlg.exec_()

        QgsProject.instance().writeEntry('SparqlForQGIS','LayersNames', [layer.name for layer in self.layers])
        QgsProject.instance().writeEntry('SparqlForQGIS','LayersUrl', [layer.url for layer in self.layers])
        QgsProject.instance().writeEntry('SparqlForQGIS','LayersDisplaySparql', [layer.displaySparql for layer in self.layers])
        QgsProject.instance().writeEntry('SparqlForQGIS','LayersUpdateSparql', [layer.updateSparql for layer in self.layers])

        for layer in self.layers:
            if layer.needsUpdate:
                layer.update()

    def updateAll(self):
        QgsMessageLog.logMessage("Update all",'SparqlLayer')
        for layer in self.layers:
            layer.update()
        QgsMessageLog.logMessage("Done",'SparqlLayer')

    def updateOne(self):
        QgsMessageLog.logMessage("Update one",'SparqlLayer')

        for layer in self.layers:
            if self.iface.activeLayer() in layer.layers:
                layer.update()
                QgsMessageLog.logMessage("Done",'SparqlLayer')
                return
        QgsMessageLog.logMessage("Not a SparqlLayer",'SparqlLayer')


