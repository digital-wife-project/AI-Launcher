import sys
from PyQt5.QtCore import QThread, pyqtSignal
import subprocess

class GitCloneThread(QThread):
    # 定义信号，用于发送输出和错误信息
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, repo_url, clone_dir, bat_path):
        super(GitCloneThread, self).__init__()
        self.git_path = "./PortableGit/bin/git.exe"
        self.repo_url = repo_url
        self.clone_dir = clone_dir
        self.bat_path = bat_path

    def run(self):
        try:
            # 克隆Git仓库
            self.output_signal.emit("开始克隆仓库...")
            result = subprocess.run([self.git_path, 'clone', self.repo_url, self.clone_dir],
                                    check=True, text=True, capture_output=True)
            self.output_signal.emit(result.stdout)

            # 执行.bat文件
            self.output_signal.emit("开始执行.bat文件...")
            result = subprocess.run(self.bat_path, check=True, text=True, capture_output=True)
            self.output_signal.emit(result.stdout)
        except subprocess.CalledProcessError as e:
            # 发送错误信号
            self.error_signal.emit(e.stderr)

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
    bat_path = './install_script/glm_6b/install.bat'

    # 创建并启动线程
    thread = GitCloneThread(repo_url, clone_dir, bat_path)
    thread.output_signal.connect(lambda output: print("输出：", output))
    thread.error_signal.connect(lambda error: print("错误：", error))
    thread.start()

    sys.exit(app.exec_())
