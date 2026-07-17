# -*- coding: utf-8 -*-
#
# PipaRouter — roteirização de caminhões-pipa no QGIS
# Copyright (C) 2025  Antonio A. Coelho Neto
#
# Este programa é software livre: você pode redistribuí-lo e/ou modificá-lo
# sob os termos da GNU General Public License versão 2 ou posterior.
# Veja o arquivo LICENSE, ou <https://www.gnu.org/licenses/gpl-2.0.html>.
#
"""PipaRouter - entrada do plugin QGIS."""

import os
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction


class PipaRouterPlugin:

    def __init__(self, iface):
        self.iface = iface
        self.painel = None
        self.action = None
        self.menu = "&PipaRouter"

    def initGui(self):
        icone = os.path.join(os.path.dirname(__file__), "resources", "icon.png")
        self.action = QAction(
            QIcon(icone) if os.path.exists(icone) else QIcon(),
            "PipaRouter - Rotas de Caminhao-Pipa",
            self.iface.mainWindow(),
        )
        self.action.setCheckable(True)
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(self.menu, self.action)

    def unload(self):
        if self.painel:
            self.iface.removeDockWidget(self.painel)
            self.painel.close()
            self.painel = None
        self.iface.removePluginMenu(self.menu, self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self, checked=None):
        from .ui.painel import PainelPipa
        if self.painel is None:
            try:
                self.painel = PainelPipa(self.iface, self.iface.mainWindow())
            except Exception as e:
                # Sem isto o QGIS mostra so "Erro Python: consulte o
                # registro" — o usuario fica sem saber o que houve e eu
                # fico sem saber o que consertar. Melhor mostrar a linha.
                import traceback
                tb = traceback.format_exc()
                try:
                    from qgis.core import QgsMessageLog, Qgis
                    QgsMessageLog.logMessage(tb, "PipaRouter", Qgis.Critical)
                except Exception:
                    pass

                linha = ""
                for f in reversed(traceback.extract_tb(e.__traceback__)):
                    if "pipa_router" in (f.filename or ""):
                        arq = f.filename.split("pipa_router")[-1].lstrip("/\\")
                        linha = f"{arq}:{f.lineno} em {f.name}()"
                        break

                from qgis.PyQt.QtWidgets import QMessageBox
                cx = QMessageBox(self.iface.mainWindow())
                cx.setIcon(QMessageBox.Critical)
                cx.setWindowTitle("PipaRouter")
                cx.setText(
                    f"O plugin não abriu.\n\n"
                    f"{type(e).__name__}: {e}\n\n"
                    f"{linha}\n\n"
                    f"Isto é um defeito do plugin, não do seu computador. "
                    f"Mande o texto abaixo (botão 'Mostrar detalhes') para "
                    f"quem mantém o plugin.")
                cx.setDetailedText(tb)
                cx.exec_()
                self.painel = None
                return
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.painel)
            self.painel.visibilityChanged.connect(self.action.setChecked)
        self.painel.setVisible(True)
        self.painel.raise_()
