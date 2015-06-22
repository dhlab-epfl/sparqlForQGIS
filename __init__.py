# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SparqlForQGIS
                                 A QGIS plugin
 Display and update data from Sparql queries
                             -------------------
        begin                : 2015-06-22
        copyright            : (C) 2015 by Olivier Dalang
        email                : olivier.dalang@epfl.ch
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SparqlForQGIS class from file SparqlForQGIS.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .sparql_for_qgis import SparqlForQGIS
    return SparqlForQGIS(iface)
