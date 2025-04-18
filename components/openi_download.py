﻿import subprocess
import re
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import zipfile
import sys
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
        filepath = "openi dataset download"
        arguments = f" {self.repoid} {self.file} --cluster NPU --save_path ./tmp/"
        command = f"{filepath} {arguments}"
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8',errors='replace')

        for line in iter(process.stdout.readline, ''):
            if not self.running:
                break
            percentage = self.attackdetail(line)
            if percentage:
                self.presentage_updated.emit(int(percentage))

        self.on_download_finished.emit()
        self.unzip(f"./tmp/{self.file}",self.savepath)

        process.stdout.close()
        process.wait()

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


    def stop(self):
        self.running = False

