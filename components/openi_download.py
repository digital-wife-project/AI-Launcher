from doctest import REPORT_CDIFF
import subprocess
import re
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import zipfile
import os
from siui.core import SiGlobal



class OpeniDownloadWorker(QThread):

    presentage_updated = pyqtSignal(int)
    on_download_finished = pyqtSignal()
    finished_unzipping=pyqtSignal(str,str,list)

    def __init__(self,project_name, repoid, install_arg, savepath):
        super().__init__()
        self.project_name=project_name
        self.repoid = repoid
        self.savepath = savepath
        self.running = True
        # 将正则表达式定义移到类级别
        self.regex_percentage = re.compile(r"(\d+)%")
        if isinstance(install_arg, str):
            SiGlobal.siui.ThreadList["install"].append(self.project_name)
            self.file = install_arg
            self.install_arg = []
        elif isinstance(install_arg, list):
            self.file = install_arg[0]
            self.install_arg = install_arg

    def run(self):
        # 创建一个STARTUPINFO对象，用于设置子进程的启动信息
        startupinfo = subprocess.STARTUPINFO()
        # 设置子进程的启动标志，使其不显示窗口
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        # 检查文件是否存在
        if not (self.check_file_exists(f"./tmp/{self.file}")):
            # 设置下载文件的路径
            exe_path = './openi_download.exe'
            repoid = ['--repo_id',f'{self.repoid}']  # 这是要传递给exe程序的参数
            file= ['--file',f'{self.file}']
            savepath = ['--save_path','./tmp']
            # 使用subprocess.Popen来启动程序
            process = subprocess.Popen([exe_path]+repoid+file+savepath, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            # 实时捕获输出
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    # 解析输出中的百分比
                    percentage = self.attackdetail(output)
                    if percentage:
                        self.presentage_updated.emit(int(percentage))
            process.wait()

        # 发射下载完成信号
        self.on_download_finished.emit()
        # 解压下载的文件
        self.unzip(f"./tmp/{self.file}",self.savepath)


    def attackdetail(self, line):
        match_percentage = self.regex_percentage.search(line)
        percentage = match_percentage.group(1) if match_percentage else None
        return percentage
    
    def unzip(self,zip_file_path:str,extract_path:str):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # 获取ZIP文件中所有文件的总大小
            total_size = sum((file_info.file_size for file_info in zip_ref.infolist()))
            extracted_size = 0

            # 遍历ZIP文件中的所有文件
            for file_info in zip_ref.infolist():
                # 解压单个文件
                zip_ref.extract(file_info, extract_path)
                # 更新已解压的大小
                extracted_size += file_info.file_size
                # 发送信号以更新进度条
                self.presentage_updated.emit(int((extracted_size / total_size) * 100))

            # 发送信号表示解压完成

            self.finished_unzipping.emit(self.project_name,(self.savepath+"//"+self.file)[:-4],self.install_arg)
            if self.install_arg==[]:
                SiGlobal.siui.ThreadList["install"].remove(self.project_name)
            self.quit()

    def check_file_exists(self,file_path):
        # 检查路径是否存在
        if os.path.exists(file_path):
            # 检查是否为文件
            if os.path.isfile(file_path):
                return True
        else:
            return False
    

    def stop(self):
        self.running = False