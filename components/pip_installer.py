import sys
import os
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

from siui.core import SiGlobal

class GitCloneThread(QThread):
    # 定义信号，用于发送输出和错误信息
    outputsignal = pyqtSignal(str)
    errorsignal = pyqtSignal(str,str)
    clone_completed = pyqtSignal(str, str, list)  # 新增信号，用于通知克隆完成

    def __init__(self, install_args, user_path, project_name,operation):
        super(GitCloneThread, self).__init__()
        self.gitpath = "git.exe"
        self.operation=operation
        print(os.path.abspath(self.gitpath))
        self.repourl = install_args[1]
        self.clonedir = os.path.join(user_path, project_name)  # 使用os.path.join来拼接路径
        self.project_name = project_name
        self.install_args = install_args
        SiGlobal.siui.ThreadList["install"].append(self.project_name)


    def run(self):
        try:
            print("开始克隆仓库...")
            self.outputsignal.emit("开始克隆仓库...")
            
            # 使用Popen来实时获取输出
            proc = subprocess.Popen([self.gitpath, self.operation, self.repourl, self.clonedir],
                                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
            # 实时读取输出
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                self.outputsignal.emit(line.strip())
            # 等待进程结束
            proc.wait()
            # 检查是否有错误发生
            if proc.returncode != 0:
                raise subprocess.CalledProcessError(proc.returncode, proc.args, output=proc.stdout.read())
            print("克隆完成")
            self.outputsignal.emit(f"克隆完成，目录: {self.clonedir}")
            self.clone_completed.emit(self.clonedir, self.project_name, self.install_args)  # 发送克隆完成信号

        except subprocess.CalledProcessError as e:
            self.errorsignal.emit(e.output,self.clonedir)  # 发射错误信息
        finally:
            # 退出线程
            self.quit()

class BatExecutionThread(QThread):
    # 定义信号，用于发送输出信息
    outputsignal = pyqtSignal(str)
    errorsignal = pyqtSignal(str,str)
    pip_finished = pyqtSignal(str, str)  # 假设信号需要传递这些参数

    def __init__(self, clonedir, project_name,operation):
        super(BatExecutionThread, self).__init__()
        self.clonedir = clonedir
        self.operation=operation
        self.project_name = project_name

    def run(self):
        try:
            print("开始运行bat...")
            self.outputsignal.emit("开始运行...")
            install_bat_path = os.path.join(self.clonedir, "runner.exe")
            print(install_bat_path)
            if self.operation=="install":
                # 使用subprocess.Popen来实时获取输出
                result = subprocess.run([install_bat_path,'--install'], check=True, capture_output=True, text=True)
                if result.returncode == 0:
                    self.outputsignal.emit(f"安装完成，目录: {self.clonedir}")
                    print("运行完成")
                    self.pip_finished.emit(self.clonedir, self.project_name)  # 发送克隆完成信号
                SiGlobal.siui.ThreadList["install"].remove(self.project_name)

            elif self.operation=="launch":
                SiGlobal.siui.ThreadList["launch"].append(self.project_name)
                result = subprocess.run([install_bat_path,'--install'], check=True, capture_output=True, text=True)
                self.outputsignal.emit("启动完成")
                self.outputsignal.emit(f"{self.project_name}运行退出")
                SiGlobal.siui.ThreadList["launch"].remove(self.project_name)

        except subprocess.CalledProcessError as e:
            # 处理错误情况
            error_message = f"运行失败: {e}"
            print(error_message)
            self.errorsignal.emit(error_message,self.clonedir)
        finally:
            # 退出线程
            self.quit()
