from fastapi import FastAPI
import json
app = FastAPI()

@app.get("/version")
async def read_json_file_version():
    # 读取 JSON 文件
    with open("./data.json", "r") as file:
        data = json.load(file)
    version=data.get("version")
    # 返回 JSON 响应
    return version

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
