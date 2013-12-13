# -*- coding: utf-8 -*-
"""
/***************************************************************************
 kuw_filter
                                 A QGIS plugin
 Applies Kuwahara Filter
                             -------------------
        begin                : 2013-02-05
        copyright            : (C) 2013 by Caio Hamamura/Laboratório de Silvicultura Urbana - Universidade de São Paulo (campus de Piracicaba)
        email                : caiohamamura@gmail.com
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

def classFactory(iface):
    # load kuw_filter class from file kuw_filter
    from kuw_filter import kuw_filter
    return kuw_filter(iface)
