import sys
import os
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess
import shutil

class GitCloneThread(QThread):
    # 定义信号，用于发送输出和错误信息
    outputsignal = pyqtSignal(str)
    errorsignal = pyqtSignal(str)

    def __init__(self, repourl, clonedir, batpath):
        super(GitCloneThread, self).__init__()
        self.gitpath = "./PortableGit/bin/git.exe"
        self.repourl = repourl
        self.clonedir = clonedir
        self.batpath = batpath

    def run(self):
        try:
            print("开始克隆仓库...")
            self.outputsignal.emit("开始克隆仓库...")
            result = subprocess.run([self.gitpath, 'clone', self.repourl, self.clonedir],
                                    check=True, text=True, capture_output=True)
            self.outputsignal.emit(result.stdout)

            print("克隆完成")
            os.chdir(self.clonedir)
            self.outputsignal.emit(f"切换到目录: {self.clonedir}")

            print("开始执行.bat文件...")
            self.outputsignal.emit("开始执行.bat文件...")
            with subprocess.Popen(self.batpath+"//install.bat", stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True) as process:
                for line in process.stdout:
                    self.outputsignal.emit(line.strip())
                process.stdout.close()
                returncode = process.wait()
                if returncode:
                    raise subprocess.CalledProcessError(returncode, process.args, process.stderr.read())
            print(".bat文件执行完成")
            # .bat 文件执行完成后，复制 .bat 文件到 clonedir
            self.copy_bat_file_to_clonedir()

        except subprocess.CalledProcessError as e:
            self.errorsignal.emit(e.stderr)
        finally:
            # 退出线程
            self.quit()

    def copy_bat_file_to_clonedir(self):
        # 获取.bat文件的文件名
        bat_filename = os.path.basename(self.batpath+"//launch.bat")
        # 目标路径
        destination_path = os.path.join(self.clonedir, bat_filename)
        try:
            # 复制文件
            shutil.copy(self.batpath, destination_path)
            self.outputsignal.emit(f"launch.bat 文件已复制到: {destination_path}")
        except IOError as e:
            self.errorsignal.emit(f"复制 .bat 文件失败: {e}")