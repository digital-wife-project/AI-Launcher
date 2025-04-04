import sys
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

import sys
import os
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

class GitCloneThread(QThread):
    # 定义信号，用于发送输出和错误信息
    outputsignal = pyqtSignal(str)
    errorsignal = pyqtSignal(str)

    def __init__(self, repourl, clonedir, batpath):
        super(GitCloneThread, self).__init__()
        self.gitpath = "./PortableGit/bin/git.exe"
        self.repourl = repourl
        self.clonedir = "D://test"
        self.batpath = batpath

    def run(self):
        try:
            # 克隆Git仓库
            self.outputsignal.emit("开始克隆仓库...")
            result = subprocess.run([self.gitpath, 'clone', self.repourl, self.clonedir],
                                    check=True, text=True, capture_output=True)
            self.outputsignal.emit(result.stdout)

            # # 切换到克隆目录
            os.chdir(self.clonedir)
            self.outputsignal.emit(f"切换到目录: {self.clonedir}")

            # 执行.bat文件
            self.outputsignal.emit("开始执行.bat文件...")
            with subprocess.Popen(self.batpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True) as process:
                for line in process.stdout:
                    self.outputsignal.emit(line.strip())
                process.stdout.close()
                # 等待进程结束
                returncode = process.wait()
                if returncode:
                    raise subprocess.CalledProcessError(returncode, process.args, process.stderr.read())

        except subprocess.CalledProcessError as e:
            # 发送错误信号
            self.errorsignal.emit(e.stderr)


# 示例用法
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)
    window = QMainWindow()

    # Git仓库的URL
    repo_url = 'https://github.moeyy.xyz/https://github.com/THUDM/ChatGLM-6B.git'
    # 克隆到指定的目录
    clone_dir = 'D://test'
    # .bat文件的路径
    bat_path = "D:\AI-Launcher\install_script\glm_6b\install.bat"

    # 创建并启动线程
    thread = GitCloneThread(repo_url, clone_dir, bat_path)
    thread.outputsignal.connect(lambda output: print("输出：", output))
    thread.errorsignal.connect(lambda error: print("错误：", error))
    thread.start()

    sys.exit(app.exec_())
