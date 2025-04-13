from PyQt5.QtWidgets import QFileDialog
from siui.components import (
    SiPushButton, 
    SiTitledWidgetGroup,
    SiDenseHContainer,
    SiOptionCardPlane,
    )
from siui.core import SiColor, SiGlobal,GlobalFont
from siui.components.page.child_page import SiChildPage

import re
from .DemoLabel import DemoLabel
from .yes_no_model_windows import YesNoModelWindows
from .side_message import send_simple_message
from ..json_changer import json_rewriter,json_deleter
from ..FolderMover import FolderMover,DeleteFolderThread

class ChildPage_ProjectDetail(SiChildPage):
    def __init__(self,parent,project_name,project_path):
        super().__init__(parent)

        self.view().setMinimumWidth(800)
        self.content().setTitle("项目管理")
        self.content().setPadding(64)
        self.project_path=project_path
        self.project_name=project_name
        self.changed_path=None

        # page content
        self.titled_widget_group = SiTitledWidgetGroup(self)

        with self.titled_widget_group as group:
            self.option_card_general = SiOptionCardPlane(self)
            self.option_card_general.setTitle("项目位置设置")

            self.button2 = SiPushButton(self)
            self.button2.setFixedHeight(32)
            self.button2.attachment().setText("更改安装位置")
            self.button2.colorGroup().assign(SiColor.BUTTON_PANEL, self.getColor(SiColor.INTERFACE_BG_D))
            self.button2.clicked.connect(self.openFolderDialog)

            self.option_card_general.body().setAdjustWidgetsSize(True)
            self.option_card_general.body().addWidget(DemoLabel(self,f"当前项目根目录为{self.project_path}",""))
            self.option_card_general.body().addWidget(DemoLabel(self,f"当前项目启动bat为{self.project_path}\launch.bat",""))
            self.option_card_general.body().addWidget(self.button2)
            self.option_card_general.body().addPlaceholder(12)
            self.option_card_general.adjustSize()

            self.option_card_general2 = SiOptionCardPlane(self)
            self.option_card_general2.setTitle("项目状态设置")

            self.h_container = SiDenseHContainer(self)
            self.button3 = SiPushButton(self)
            self.button3.setFixedHeight(32)
            self.button3.attachment().setText("删除项目")
            self.button3.clicked.connect(lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().setDialog(YesNoModelWindows(self,"delet")))

            self.button4 = SiPushButton(self)
            self.button4.setFixedHeight(32)
            self.button4.attachment().setText("重装项目")
            self.button4.clicked.connect(lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().setDialog(YesNoModelWindows(self,"reinstall")))

            self.h_container.addWidget(self.button3)
            self.h_container.addWidget(self.button4)
            self.h_container.setAdjustWidgetsSize(True)
            self.h_container.addPlaceholder(12)
            self.h_container.adjustSize()

            self.option_card_general2.body().addWidget(self.h_container)
            self.option_card_general2.body().addPlaceholder(12)
            self.option_card_general2.adjustSize()
            group.addWidget(self.option_card_general)
            group.addWidget(self.option_card_general2)

        self.content().setAttachment(self.titled_widget_group)

        # control panel
        self.demo_button = SiPushButton(self)
        self.demo_button.resize(128, 32)
        self.demo_button.attachment().setText("保存")
        self.demo_button.clicked.connect(self.closeParentLayer)
        self.demo_button.clicked.connect(lambda: self.onSaveButtomClicked(parent))
        self.panel().addWidget(self.demo_button, "right")

        # load style sheet
        SiGlobal.siui.reloadStyleSheetRecursively(self)

    def onSaveButtomClicked(self,parent):
        if self.changed_path!=None:
            parent.demo_progress_button_text.setEnabled(False)
            parent.demo_push_button_text.setEnabled(False)
            parent.demo_progress_button_text.setText("正在迁移")
            parent.demo_progress_button_text.adjustSize()
            self.folder_Mover=FolderMover(self.project_path,self.changed_path)
            self.folder_Mover.progress_updated.connect(parent.presentage_updated)
            self.folder_Mover.start()
            json_rewriter(self.project_name,self.changed_path)

    def openFolderDialog(self):
    # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择安装位置")
        if folder_path:
            # 检查路径中是否包含中文或空格
            if re.search(r'[\u4e00-\u9fff\s]', (folder_path)):
                send_simple_message(4, "路径中不能包含中文或空格，请重新选择。" ,True, 100000)
                self.demo_button.setEnabled(False)

            else:
                self.changed_path = folder_path.replace("/", "\\")
                self.button2.attachment().setText(f"更改安装位置为{self.changed_path}")
                self.demo_button.setEnabled(True)

    def ProjectOperation(self,operation):
        if operation=="delet":
            self.delete_project()
        elif operation=="reinstall":
            self.reinstall_project()

    def delete_project(self):
        # 删除项目文件夹{self.project_path}
        send_simple_message(1,"开始删除",True,3000)
        delete_thread = DeleteFolderThread(self.project_path)
        delete_thread.finished_signal.connect(self.on_delete_project_finished)
        delete_thread.start()

    def on_delete_project_finished(self):
        json_deleter(self.project_name)
        send_simple_message(1,"删除成功",True,3000)
