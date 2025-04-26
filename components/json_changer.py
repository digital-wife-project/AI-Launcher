import json
import os

def json_adder(project_name:str,project_path:str):
    json_file_path = "./config/local_project.json"
    new_data={project_name:project_path}
    # 读取现有的JSON文件内容
    with open(json_file_path, 'r', encoding='utf-8-sig') as file:
    # 将JSON数据加载到字典中
        data = json.load(file)
    
        # 向字典中添加新项
        data.update(new_data)

        # 将更新后的字典写回JSON文件
    with open(json_file_path, 'w', encoding='utf-8-sig') as file:
        # 将字典转换为JSON格式的字符串，并写入文件
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("新项已添加到JSON文件。")

def loacl_project_json_reader(project_name: str):
    # 读取现有的JSON文件内容
    json_filepath = "./config/local_project.json"
    if not os.path.exists(json_filepath):
        # 如果文件不存在，创建一个新文件
        with open(json_filepath, 'w', encoding='utf-8-sig') as file:
            json.dump({}, file, ensure_ascii=False, indent=4)
    try:
        with open(json_filepath, 'r', encoding='utf-8-sig') as file:
            # 将JSON数据加载到字典中
            data = json.load(file)
            # 使用get方法安全地获取project_name的值，如果不存在则返回None
            return data.get(project_name)
    except json.JSONDecodeError:
        print(f"文件 {json_filepath} 不是有效的JSON格式。")
    except Exception as e:
        print(f"读取文件时发生错误: {e}")

def remote_project_json_reader(project_class:str):
    # 读取现有的JSON文件内容
    json_file_path="./config/avaliable_remote_project.json"
    with open(json_file_path, 'r', encoding='utf-8-sig') as file:
        # 将JSON数据加载到字典中
        data = json.load(file)
    if data[project_class]:
        return data[project_class]
    else:
        return None

def json_rewriter(project_name:str, project_path:str):
    json_file_path = "./config/local_project.json"
    # 读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8-sig') as file:
        # 解析 JSON 数据到 Python 字典
        data = json.load(file)
    
    # 更改特定键的值
    if project_name in data:
        data[project_name] = project_path
    else:
        print(f"Key '{project_name}' not found in the JSON data.")
    
    # 将更新后的字典转换回 JSON 格式
    updated_json_data = json.dumps(data, indent=4)
    
    # 将新的 JSON 数据写回文件
    with open(json_file_path, 'w', encoding='utf-8-sig') as file:
        file.write(updated_json_data)
    
def json_deleter(key_to_remove):

    # 读取JSON文件
    with open('./config/local_project.json', 'r') as file:
        data = json.load(file)
    
    # 移除指定的键
    if key_to_remove in data:
        del data[key_to_remove]
    
    # 将修改后的字典写回JSON文件
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)
    