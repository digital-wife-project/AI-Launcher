import sys
import os
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import warnings
import shutil

class GitCloneThread(QThread):
    # 定义信号，用于发送输出和错误信息
    outputsignal = pyqtSignal(str)
    errorsignal = pyqtSignal(str)
    clone_completed = pyqtSignal(str,str,list)  # 新增信号，用于通知克隆完成

    def __init__(self,install_args,user_path,project_name):
        super(GitCloneThread, self).__init__()
        self.gitpath = "./PortableGit/gitbin/git.exe"
        print(os.path.abspath(self.gitpath))
        self.repourl = install_args[1]
        self.clonedir = user_path+"/"+project_name
        self.project_name = project_name
        self.install_args = install_args

    def run(self):
        try:
            print("开始克隆仓库...")
            self.outputsignal.emit("开始克隆仓库...")
            result = subprocess.run([self.gitpath, 'clone', self.repourl, self.clonedir],
                                    check=True, text=True, capture_output=True)
            self.outputsignal.emit(result.stdout)

            print("克隆完成")
            self.outputsignal.emit(f"克隆完成，目录: {self.clonedir}")
            self.clone_completed.emit(self.clonedir,self.project_name,self.install_args)  # 发送克隆完成信号

        except subprocess.CalledProcessError as e:
            self.errorsignal.emit(e.stderr)
        finally:
            # 退出线程
            self.quit()

import os
import shutil
from PyQt5.QtCore import QThread, pyqtSignal

class BatExecutionThread(QThread):
    # 定义信号，用于发送输出信息
    outputsignal = pyqtSignal(str)

    def __init__(self, batpath, clonedir):
        super(BatExecutionThread, self).__init__()
        self.batpath = batpath
        self.clonedir = clonedir

    def run(self):
        
        os.chdir(self.clonedir)
        self.outputsignal.emit(f"切换到目录: {self.clonedir}")
        
        # 获取.bat文件的文件名
        batfilename = os.path.basename(self.batpath)
        # 目标路径
        destinationpath = os.path.join(self.clonedir, batfilename)
        # 复制文件
        shutil.copy(self.batpath, destinationpath)
        self.outputsignal.emit(f"{batfilename} 文件已复制到: {destinationpath}")
        # 退出线程
        self.quit()
