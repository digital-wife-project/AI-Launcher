from PyQt5 import QtWidgets
import icons
from components.page_about import About
from components.page_tools import tools
from components.page_homepage import ExampleHomepage

from components.pages_project.page_digitalhuman import digitalhuman
from components.pages_project.page_LLM import LLM
from components.pages_project.page_TTS import TTS
from components.pages_project.page_others import others
from components.pages_project.page_SD import SD

from components.page_QA import QA
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget

import siui
from siui.core import SiColor, SiGlobal
from siui.templates.application.application import SiliconApplication

from components.pages_project.side_message import send_simple_message

# 载入图标
siui.core.globals.SiGlobal.siui.loadIcons(
    icons.IconDictionary(color=SiGlobal.siui.colors.fromToken(SiColor.SVG_NORMAL)).icons
)


class MySiliconApp(SiliconApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        screen_geo = QDesktopWidget().screenGeometry()
        self.setMinimumSize(1024, 380)
        self.resize(1366, 916)
        self.move((screen_geo.width() - self.width()) // 2, (screen_geo.height() - self.height()) // 2)
        self.layerMain().setTitle("AL All In One AI Launcher")
        self.setWindowTitle("AL Launcher")
        self.setWindowIcon(QIcon("./img/empty_icon.png"))

        self.layerMain().addPage(ExampleHomepage(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_home_filled"),
                                 hint="主页", side="top")

        self.layerMain().addPage(TTS(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_person_voice_regular"),
                                 hint="TTS", side="top")

        self.layerMain().addPage(LLM(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_textbox_regular"),
                                 hint="LLM", side="top")

        self.layerMain().addPage(SD(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_wand_filled"),
                                 hint="SD", side="top")

        self.layerMain().addPage(digitalhuman(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_scan_person_filled"),
                                 hint="数字人", side="top")

        self.layerMain().addPage(others(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_desktop_arrow_down_filled"),
                                 hint="其他", side="top")

        self.layerMain().addPage(QA(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_question_filled"),
                                 hint="疑难解答", side="top")
        self.layerMain().addPage(tools(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_toolbox_regular"),
                                 hint="工具箱", side="top")

        self.layerMain().addPage(About(self),
                                 icon=SiGlobal.siui.iconpack.get("ic_fluent_info_filled"),
                                 hint="关于", side="bottom")

        self.layerMain().setPage(0)

        SiGlobal.siui.reloadAllWindowsStyleSheet()


    def closeEvent(self, event):
        print("进入closeEvent")
        installing = ''
        running = ''
    
        if SiGlobal.siui.ThreadList["install"]:
            installing = '正在安装：'
            for i in SiGlobal.siui.ThreadList["install"]:
                installing += i + '，'
    
        if SiGlobal.siui.ThreadList["running"]:
            running = '正在运行：'
            for i in SiGlobal.siui.ThreadList["running"]:
                running += i + '，'
    
        if installing or running:
            message = f"{installing}\n{running}" if installing and running else installing or running
            result = QtWidgets.QMessageBox.question(self, "真的要关闭喵？", message, QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if result == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
    