import re
from PyQt5.QtCore import pyqtSignal
from siui.components import SiLabel, SiLongPressButton, SiPushButton
from siui.core import SiColor, SiGlobal

from siui.templates.application.components.dialog.modal import SiModalDialog

from siui.core import SiGlobal

class YesNoModelWindows(SiModalDialog):


    def __init__(self,parent,opeartion):
        super().__init__(parent)
        self.setFixedWidth(500)
        self.operation = opeartion
        self.icon().load(SiGlobal.siui.iconpack.get("ic_fluent_save_filled",
                                                    color_code=SiColor.mix(
                                                        self.getColor(SiColor.SVG_NORMAL),
                                                        self.getColor(SiColor.INTERFACE_BG_B),
                                                        0.05))
                         )

        self.label = SiLabel(self)
        self.label.setStyleSheet(f"color: {self.getColor(SiColor.TEXT_E)}")
        self.label.setText(
            f'<span style="color: {self.getColor(SiColor.TEXT_B)}; font-size: 16px;">您确认进行操作吗？</span><br>')
        self.label.adjustSize()
        self.contentContainer().addWidget(self.label)

        self.button2 = SiPushButton(self)
        self.button2.setFixedHeight(32)
        self.button2.attachment().setText("确定")
        self.button2.colorGroup().assign(SiColor.BUTTON_PANEL, self.getColor(SiColor.INTERFACE_BG_D))
        self.button2.clicked.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)
        self.button2.clicked.connect(lambda: parent.ProjectOperation(self.operation))

        self.button4 = SiPushButton(self)
        self.button4.setFixedHeight(32)
        self.button4.attachment().setText("取消")
        self.button4.colorGroup().assign(SiColor.BUTTON_PANEL, self.getColor(SiColor.INTERFACE_BG_D))
        self.button4.clicked.connect(SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().closeLayer)

        self.buttonContainer().addWidget(self.button2)
        self.buttonContainer().addWidget(self.button4)
        SiGlobal.siui.reloadStyleSheetRecursively(self)
        self.adjustSize()
        
