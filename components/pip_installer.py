import subprocess
import os
from PyQt5.QtCore import QThread, pyqtSignal

class GitCloneAndRunThread(QThread):
    output_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, url, path, batpath):
        print("开始pip安装")
        super().__init__()
        self.url = url
        self.path = path
        self.batpath = batpath

    def run(self):
        try:
            # 克隆 Git 仓库
            # 注意：这里假设 Dulwich 已经导入，并且版本检查已完成
            from dulwich import porcelain
            porcelain.clone(self.url, self.path)

            # 构建批处理文件的完整路径
            batfullpath = os.path.join(self.path, self.batpath)

            # 执行批处理文件
            with subprocess.Popen(batfullpath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True) as proc:
                # 实时读取输出
                for line in proc.stdout:
                    self.output_signal.emit(line.strip())
                # 等待进程结束
                proc.wait()
                # 检查错误输出
                stderr = proc.stderr.read()
                if stderr:
                    self.error_signal.emit(stderr.strip())

            # 发射完成信号
            self.finished_signal.emit()

        except Exception as e:
            self.error_signal.emit(f"意外错误: {str(e)}")

# 使用示例
# thread = GitCloneAndRunThread('https://github.com/user/repo.git', '/path/to/clone', 'script.bat')
# thread.output_signal.connect(lambda output: print("Output:", output))
# thread.error_signal.connect(lambda error: print("Error:", error))
# thread.finished_signal.connect(lambda: print("Finished"))
# thread.start()
