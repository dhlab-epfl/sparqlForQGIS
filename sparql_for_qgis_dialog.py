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

from SparqlLayer import SparqlLayer



class SparqlForQGISDialog(QtGui.QDialog):
    count = 0

    defaultDisplaySparql = '''PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
SELECT  ?subject
        ?geom
        ?class
WHERE   {
            ?subject geo:geometry ?geom .
            ?subject a ?class .
        }'''

    defaultUpdateSparql = '''PREFIX geo: <http://www.opengis.net/ont/geosparql#> 
WITH <http://dhlab.epfl.ch/vtm/>
DELETE  {
            ?subject geo:geometry ?geom
        }
INSERT  {
            ?subject geo:geometry !newgeom
        }
WHERE   {
            ?subject geo:geometry ?geom
            FILTER (
                ?subject=!subject
            )
        }'''    

    def __init__(self, main):
        super(SparqlForQGISDialog, self).__init__()

        self.main = main

        uic.loadUi(os.path.join( os.path.dirname(__file__), 'sparql_for_qgis_dialog_base.ui'), self)


        self.createButton.pressed.connect( self.createLayer )
        self.deleteButton.pressed.connect( self.deleteLayer )

        self.updateButton.pressed.connect( self.updateLayer )
        self.listWidget.currentRowChanged.connect( self.rowSelected )

        self.refreshList()

    def refreshList(self):

        self.listWidget.clear()

        for layer in self.main.layers:
            self.listWidget.addItem( layer.name + ('*' if layer.needsUpdate else '') )

    def createLayer(self):
        SparqlForQGISDialog.count += 1
        self.main.layers.append( SparqlLayer( self.main, 'Sparql Layer '+str(SparqlForQGISDialog.count), 'http://dhlabpc3.epfl.ch:8890/sparql/', self.defaultDisplaySparql, self.defaultUpdateSparql ) )

        self.refreshList()
        self.listWidget.setCurrentRow( self.listWidget.count() - 1 )

    def deleteLayer(self):
        row = self.listWidget.currentRow()
        layer = self.main.layers[ row ]
        layer.unload()

        self.refreshList()

    def rowSelected(self, row):
        layer = self.main.layers[row]

        self.nameLineEdit.setText( layer.name )
        self.urlLineEdit.setText( layer.url )
        self.displaySparqlPlainTextEdit.setPlainText( layer.displaySparql )
        self.updateSparqlPlainTextEdit.setPlainText( layer.updateSparql )

    def updateLayer(self):
        row = self.listWidget.currentRow()
        layer = self.main.layers[ row ]

        layer.name = self.nameLineEdit.text()
        layer.url = self.urlLineEdit.text()
        layer.displaySparql = self.displaySparqlPlainTextEdit.toPlainText()
        layer.updateSparql = self.updateSparqlPlainTextEdit.toPlainText()
        layer.needsUpdate = True

        self.refreshList()



