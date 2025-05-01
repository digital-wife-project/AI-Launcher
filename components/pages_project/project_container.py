from socket import SHUT_RD
from PyQt5.QtCore import Qt, pyqtSignal
from siui.components import (
    SiDenseHContainer,
    )
from siui.components.button import (
    SiProgressPushButton,
    SiPushButtonRefactor,
)
from siui.core import SiGlobal

import os
import shutil

from .project_detail import ChildPage_ProjectDetail
from .model_windows import ModalDownloadDialog
from ..openi_download import OpeniDownloadWorker
from ..FolderMover import DeleteFolderThread
from .DemoLabel import DemoLabel
from ..pip_installer import GitCloneThread,BatExecutionThread
from .side_message import send_simple_message
from ..json_changer import json_adder,loacl_project_json_reader

class Row_for_each_project(SiDenseHContainer):

    on_download_click = pyqtSignal(object,str)

    def __init__(self,parent,project_name,insatller,project_detail,install_args):
        super().__init__(parent)
        self.project_name=project_name
        self.insatller=insatller
        self.project_detail=project_detail
        self.install_args=install_args
        self.launcher_root=os.getcwd()
        self.model_windows_connection=None
    
        self.setFixedWidth(900)
        self.demo_progress_button_text = SiProgressPushButton(self)
        self.demo_push_button_text = SiPushButtonRefactor(self)
        self.RefreshText()

        self.demo_push_button_text.setText("项目管理")
        self.demo_push_button_text.clicked.connect(lambda:self.RefreshText())
        self.demo_push_button_text.adjustSize()

        self.addWidget(DemoLabel(self,self.project_name,self.project_detail), "left")
        # self.addPlaceholder(500)
        self.addWidget(self.demo_progress_button_text, "right")
        self.addWidget(self.demo_push_button_text, "right")
        
        self.setAdjustWidgetsSize(True)
        self.addPlaceholder(12)
        self.adjustSize()
        self.arrangeWidget()

        self.on_download_click.connect(self.download_click)

    def Open_model_windows(self):
        SiGlobal.siui.windows["MAIN_WINDOW"].layerModalDialog().setDialog(ModalDownloadDialog(self,self.install_args))

    def download_click(self,file_name,user_path):
        self.downloader(self.project_name,file_name,user_path)

    def launch_click(self):
        self.demo_progress_button_text.setText("正在运行")
        self.launcher = BatExecutionThread(self.project_path,self.project_name,'launch')
        self.launcher.outputsignal.connect(lambda output: send_simple_message(1,output,True,1500))
        self.launcher.pip_finished.connect(self.on_pip_install_thread_finished)
        self.launcher.errorsignal.connect(lambda error,project_path: self.HandleInstallError(error,project_path))
        # 连接 finished 信号
        self.launcher.start()

    def RefreshText(self):
        self.project_path=loacl_project_json_reader(self.project_name)
        if self.project_path !=None:
            self.demo_progress_button_text.setText("开始使用")
            self.demo_progress_button_text.setToolTip("点击以开始使用")
            self.demo_progress_button_text.setProgress(100)
            self.demo_progress_button_text.adjustSize()
            self.demo_progress_button_text.clicked.connect(self.launch_click)
            self.demo_push_button_text.clicked.connect(lambda: SiGlobal.siui.windows["MAIN_WINDOW"].layerChildPage().setChildPage(ChildPage_ProjectDetail(self,self.project_name,self.project_path)))  # 连接点击信号到槽函数
            self.demo_push_button_text.adjustSize()
        else:
            self.demo_progress_button_text.setText("开始下载")
            self.demo_progress_button_text.setToolTip("点击以开始下载")
            self.model_windows_connection=self.demo_push_button_text.clicked.connect(self.Open_model_windows)
            self.demo_progress_button_text.clicked.connect(self.Open_model_windows)
            self.demo_progress_button_text.adjustSize()

    def RefreshSize(self):
        self.demo_progress_button_text.adjustSize()
        self.demo_push_button_text.adjustSize()
        self.adjustSize()

    def downloader(self,project_name,install_arg,user_path):
        self.demo_progress_button_text.setEnabled(False)
        self.demo_push_button_text.setEnabled(False)
        self.demo_progress_button_text.setText("正在下载")
        if self.insatller=="openi":
            print("使用openi下载")
            self.download_worker = OpeniDownloadWorker(project_name,install_arg[0],install_arg[1],user_path)
            self.download_worker.presentage_updated.connect(self.presentage_updated)
            self.download_worker.on_download_finished.connect(self.download_finished)
            self.download_worker.finished_unzipping.connect(self.OpeniunzipFinished)
            self.download_worker.start()
        if self.insatller=="pip":
            print("使用pip下载")
            self.demo_progress_button_text.setText("部署中")
            self.RefreshSize()   
            self.git_clone_thread = GitCloneThread(install_arg, user_path, project_name,'clone')
            self.git_clone_thread.outputsignal.connect(lambda output: send_simple_message(1,output,True,1500))
            self.git_clone_thread.errorsignal.connect(lambda error,project_path: self.HandleInstallError(error,project_path))
            self.git_clone_thread.clone_completed.connect(self.on_clone_thread_finished)  # 连接 finished 信号
            self.git_clone_thread.start()  # 启动线程

    def presentage_updated(self, percentage):
        self.demo_progress_button_text.setProgress(percentage/100)
        print(f"Download percentage: {percentage}%")

    def download_finished(self):
        self.demo_progress_button_text.setText("正在解压")

    def OpeniunzipFinished(self,project_name,save_path,_):
        self.demo_progress_button_text.setText("解压完成")
        abs_path = os.path.abspath(save_path)
        shutil.copy("./runner.exe",abs_path)
        print(f"Download finished for file: {abs_path}")
        self.demo_push_button_text.disconnect(self.model_windows_connection)
        self.demo_push_button_text.setEnabled(True)
        self.demo_progress_button_text.setEnabled(True)
        json_adder(project_name,abs_path)
        self.RefreshText()
        self.RefreshSize()

    def on_clone_thread_finished(self,clonedir,projectname,install_args_list):
        self.demo_progress_button_text.setText("克隆完成")
        self.RefreshSize()
        self.RefreshText()
        self.download_worker = OpeniDownloadWorker(projectname,"wyyyz/dig",install_args_list,clonedir)
        self.download_worker.presentage_updated.connect(self.presentage_updated)
        self.download_worker.on_download_finished.connect(self.download_finished)
        self.download_worker.finished_unzipping.connect(self.PythonEnvUnzipFinished)
        self.download_worker.start()

    def PythonEnvUnzipFinished(self, project_name, save_path, install_arg):
        self.demo_progress_button_text.setText("pip安装中")
        self.RefreshSize()       
        abs_path = os.path.abspath(save_path)
        print(f"Download finished for file: {abs_path}")
        project_bat_path=(os.path.abspath(os.path.join(abs_path, os.pardir)))
        abs_bat_path = os.path.abspath(install_arg[2])
        shutil.copy(abs_bat_path+"\\install.bat", project_bat_path)
        shutil.copy(abs_bat_path+"\\launch.bat", project_bat_path)
        shutil.copy("./runner.exe",project_bat_path)
        # 创建并启动线程
        self.thread = BatExecutionThread(project_bat_path,project_name,'install')
        self.thread.outputsignal.connect(lambda output: send_simple_message(1,output,True,1500))
        self.thread.pip_finished.connect(self.on_pip_install_thread_finished)
        self.thread.errorsignal.connect(lambda error,project_path: self.HandleInstallError(error,project_path))
        # 连接 finished 信号
        self.thread.start()

    def HandleInstallError(self, error,project_path):
        print(f"克隆失败: {error}")
        send_simple_message(4,error,False,1500)
        self.demo_progress_button_text.setText("安装失败")
        self.RefreshSize()
        send_simple_message(4,"安装失败，正在删除缓存",False,1500)
        delete_thread = DeleteFolderThread(project_path)
        delete_thread.finished_signal.connect(self.HandleInstallErrorAfterDelete)
        delete_thread.start()

    def HandleInstallErrorAfterDelete(self):
        send_simple_message(4,"安装失败，请尝试重装",False,1500)
        self.demo_progress_button_text.setText("重新安装")
        self.demo_progress_button_text.setEnabled(True)
        self.demo_push_button_text.setEnabled(True)

    def on_pip_install_thread_finished(self,project_path,project_name):
        os.chdir(self.launcher_root)
        print("GitCloneThread 已完成。")
        json_adder(project_name, project_path)
        self.demo_progress_button_text.setText("启动")
        self.RefreshSize()
        self.RefreshText()
        self.demo_push_button_text.disconnect(self.model_windows_connection)
        self.demo_push_button_text.setEnabled(True)
        self.demo_progress_button_text.setEnabled(True)

    def closeEvent(self, event):
        # 在窗口关闭前确保线程已经停止
        if self.thread.isRunning():
            self.thread.terminate()
            self.thread.wait()
        event.accept()
