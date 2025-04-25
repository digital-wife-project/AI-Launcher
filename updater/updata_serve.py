from fastapi import FastAPI
import json
app = FastAPI()

@app.get("/version")
def remote_project_json_reader():
    json_file_path="./data.json"
    with open(json_file_path, 'r', encoding='utf-8-sig') as file:
        data = json.load(file)
    if data["version"]:
        return data["version"]
    else:
        return None

@app.get("/config")
async def read_json_file():
    # 读取 JSON 文件
    with open("./data.json", "r") as file:
        data = json.load(file)
    
    # 返回 JSON 响应
    return data

@app.get("/change_config")
async def change_json_file(token: str,content: str):
    if token == "123456":
        json_file_path="./data.json"
        file=open(json_file_path,"w")
        file.write(content)
        file.close()
        return {"status": "success"}
    else:
        return {"status": "error"}

# 启动 FastAPI 应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=19257)
