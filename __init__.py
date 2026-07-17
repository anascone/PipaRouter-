# -*- coding: utf-8 -*-
#
# PipaRouter — roteirização de caminhões-pipa no QGIS
# Copyright (C) 2025  Antonio A. Coelho Neto
#
# Este programa é software livre: você pode redistribuí-lo e/ou modificá-lo
# sob os termos da GNU General Public License versão 2 ou posterior.
# Veja o arquivo LICENSE, ou <https://www.gnu.org/licenses/gpl-2.0.html>.
#
def classFactory(iface):
    from .plugin import PipaRouterPlugin
    return PipaRouterPlugin(iface)
