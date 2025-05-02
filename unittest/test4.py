import os
import subprocess

def delete_folder_silently(folder_path):
    """
    静默删除指定文件夹（支持非空目录）
    参数：
        folder_path (str): 要删除的文件夹路径
    返回：
        bool: 删除是否成功
    """
    try:
        if os.name == 'nt':
            # Windows系统使用rmdir命令
            subprocess.run(
                f'rmdir /s /q "{folder_path}"',
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        else:
            # Linux/macOS使用rm命令
            subprocess.run(
                f'rm -rf "{folder_path}"',
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        return True
    except subprocess.CalledProcessError as e:
        print(f"删除失败: {e}")
        return False
    except FileNotFoundError:
        print(f"路径不存在: {folder_path}")
        return False

# 使用示例
if __name__ == "__main__":
    folder_to_delete = r"D:\test2"  # Windows示例路径
    success = delete_folder_silently(folder_to_delete)
    print(f"删除结果: {'成功' if success else '失败'}")
