# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *

import urllib2, urllib
import json

class SparqlLayer(object):

    def __init__(self, main, name, url, displaySparql, updateSparql ):

        self.main = main

        self.layerPoints = QgsVectorLayer("MultiPoint", name+' (points)', "memory")
        self.layerLines = QgsVectorLayer("MultiLineString", name+' (lines)', "memory")
        self.layerPolygons = QgsVectorLayer("MultiPolygon", name+' (polygons)', "memory")


        self.layerPoints.beforeCommitChanges.connect( lambda: self.beforeCommitChanges(self.layerPoints) )
        self.layerLines.beforeCommitChanges.connect( lambda: self.beforeCommitChanges(self.layerLines) )
        self.layerPolygons.beforeCommitChanges.connect( lambda: self.beforeCommitChanges(self.layerPolygons) )


        QgsMapLayerRegistry.instance().addMapLayer(self.layerPolygons)
        QgsMapLayerRegistry.instance().addMapLayer(self.layerLines)
        QgsMapLayerRegistry.instance().addMapLayer(self.layerPoints)

        self.layers = {self.layerPoints, self.layerLines, self.layerPolygons}

        self.__name = name
        self.__url = url
        self.__displaySparql = displaySparql
        self.__updateSparql = updateSparql
        self.needsUpdate = True




    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, val):
        self.__name = val
        self.layerPoints.setLayerName( val +' (points)')
        self.layerLines.setLayerName( val +' (lines)')
        self.layerPolygons.setLayerName( val +' (polygons)')

    @property
    def url(self):
        return self.__url
    @url.setter
    def url(self, val):
        self.__url = val
        self.needsUpdate = True

    @property
    def displaySparql(self):
        return self.__displaySparql
    @displaySparql.setter
    def displaySparql(self, val):
        self.__displaySparql = val
        self.needsUpdate = True

    @property
    def updateSparql(self):
        return self.__updateSparql
    @updateSparql.setter
    def updateSparql(self, val):
        self.__updateSparql = val








    def unload(self):
        self.main.layers.remove( self )
        try:
            QgsMapLayerRegistry.instance().removeMapLayer(self.layerPoints.id())
        except Exception, e:
            pass
        try:
            QgsMapLayerRegistry.instance().removeMapLayer(self.layerLines.id())
        except Exception, e:
            pass
        try:
            QgsMapLayerRegistry.instance().removeMapLayer(self.layerPolygons.id())
        except Exception, e:
            pass
        

    def update(self):

        QgsMessageLog.logMessage( self.name+': making the http request...','SparqlLayer' )


        # Make the http request
        try:
            data = urllib.urlencode({'query' : self.displaySparql})
            request = urllib2.Request( url=self.url, data=data, headers={'Accept': 'application/json'} )
            content = urllib2.urlopen( request ).read()
        except Exception, e:            
            QgsMessageLog.logMessage( 'Error when executing the query !','SparqlLayer' )
            QgsMessageLog.logMessage( str(e), 'SparqlLayer' )
            return

        QgsMessageLog.logMessage( self.name+': parsing the json...','SparqlLayer' )

        # Load the JSON
        try:
            jsonData = json.loads(content)
        except Exception, e:
            QgsMessageLog.logMessage( 'Error when parsing the query !','SparqlLayer' )
            QgsMessageLog.logMessage( str(e), 'SparqlLayer' )
            return

        # Deleting the features

        for layer in self.layers:
            layer.dataProvider().deleteFeatures( layer.allFeatureIds() )


        QgsMessageLog.logMessage( self.name+': getting the fields...','SparqlLayer' )

        # Create the attributes
        fields = QgsFields ()
        for layer in self.layers:

            #provider.deleteAttributes()
            for attr in jsonData['head']['vars']:
                fields.append( QgsField(attr, QVariant.String) )

            layer.dataProvider().addAttributes( fields )
            layer.updateFields()

        QgsMessageLog.logMessage( self.name+': creating the features...','SparqlLayer' )


        # Create the features
        for jsonFeature in jsonData['results']['bindings']:

            geometry = QgsGeometry.fromWkt( jsonFeature['geom']['value'] )
            fet = QgsFeature()
            fet.setGeometry( geometry )


            fet.setFields( fields )

            for attr in jsonFeature:
                fet.setAttribute( attr, jsonFeature[attr]['value'] )

            if geometry.type() == QGis.Point:
                self.layerPoints.dataProvider().addFeatures([fet])

            elif geometry.type() == QGis.Line:
                self.layerLines.dataProvider().addFeatures([fet])

            elif geometry.type() == QGis.Polygon:
                self.layerPolygons.dataProvider().addFeatures([fet])

        QgsMessageLog.logMessage( self.name+': updating the extents...','SparqlLayer' )

        # Update the extents
        for layer in self.layers:
            layer.updateExtents()

        QgsMessageLog.logMessage( self.name+': finished !','SparqlLayer' )


        self.needsUpdate = False




    def beforeCommitChanges(self, layer):

        changedGeometries = layer.editBuffer().changedGeometries()

        request = QgsFeatureRequest()
        request.setFilterFids( changedGeometries.keys() )
        oldFeatures = layer.getFeatures( request )

        # DELETING THE OLD TRIPLES

        QgsMessageLog.logMessage( self.name+': making the http request...','SparqlLayer' )

        for feature in oldFeatures:

            sparql = self.updateSparql
            sparql = sparql.replace( '!subject', '<'+feature.attribute('subject')+'>' )
            sparql = sparql.replace( '!oldgeom', '"'+feature.attribute('geom')+'"^^virtrdf:Geometry' )
            sparql = sparql.replace( '!newgeom', '"'+feature.geometry().exportToWkt().upper()+'"^^virtrdf:Geometry' )

            QgsMessageLog.logMessage( 'Executing :' +sparql,'SparqlLayer' )
        
            # Make the http request
            try:
                data = urllib.urlencode({'query' : sparql})
                request = urllib2.Request( url=self.url, data=data, headers={'Accept': 'application/json'} )
                content = urllib2.urlopen( request ).read()
            except Exception, e:            
                QgsMessageLog.logMessage( 'Error when executing the query !','SparqlLayer' )
                QgsMessageLog.logMessage( str(e), 'SparqlLayer' )
                return

        return



        
