import re
import subprocess
repoid = 'wyyyz/dig'
file = 'py311.zip'

regex_percentage = re.compile(r"(\d+)%")
exe_path = './openi_download.exe'
repoid = ['--repo_id',f'{repoid}']  # 这是要传递给exe程序的参数
file= ['--file',f'{file}']
savepath = ['--save_path','./tmp']
print([exe_path, repoid, file, savepath])
# 使用subprocess.Popen来启动程序
def attackdetail(line):
    match_percentage = regex_percentage.search(line)
    percentage = match_percentage.group(1) if match_percentage else None
    return percentage
startupinfo = subprocess.STARTUPINFO()
# 设置子进程的启动标志，使其不显示窗口
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

process = subprocess.Popen([exe_path]+repoid+file+savepath, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
# 实时捕获输出
while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    print("输出:", output)
                    # 解析输出中的百分比
                    percentage = attackdetail(output)
                    if percentage:
                        print("百分比:", percentage)
process.wait()

def attackdetail(line):
    match_percentage = regex_percentage.search(line)
    percentage = match_percentage.group(1) if match_percentage else None
    return percentage
    
