import numpy
import os

current_module_path = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(current_module_path, './icons.dat')

class IconDictionary:
    def __init__(self, library_path=data_file_path, color=None):
        # 读取数据并解密
        f = open(library_path, 'rb')
        library_raw = f.read()
        library_list = list(library_raw)
        try:
            library = bytes(list((numpy.array(library_list) + numpy.array(range(len(library_list))) * 17) % 255)).decode('gbk')  # 尝试GBK编码
        except UnicodeDecodeError as e:
            print(f"解码错误: {e}")
            return

        # 整理成字典
        items = library.split('!!!')
        names = []
        datas = []
        for item in items[1:]:
            name, data = item.split('###')
            data = data.replace('/>', ' fill="{}" />'.format(color))
            names.append(name)
            datas.append(data.encode())
        self.icons = dict(zip(names, datas))

    def get(self, name):
        svg_data = self.icons[name]
        return svg_data.encode()
