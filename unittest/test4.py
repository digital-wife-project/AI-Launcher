import subprocess

# 使用原始字符串来避免反斜杠转义问题
result = subprocess.run(["powershell", "-Command", "Remove-Item", "-Recurse", "-Force", '-Path','D:\\test2'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(result.stdout.decode())
print(result.stderr.decode())
# 检查命令是否成功运行
if result.returncode == 0:
    print("命令成功运行")
else:
    print("命令运行失败")
