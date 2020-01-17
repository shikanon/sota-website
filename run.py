#coding:utf-8
import database
import json
from util import Checker
from fastapi import FastAPI
from starlette.responses import JSONResponse


app = FastAPI()
db = database.DB()

# 版本号
version = "v1"

def gen_uri(url):
    return "/sota/api/%s"%(version) + url

@app.get(gen_uri("/index"))
async def getAPIIndex():
    rows = db.get_sotaindex()
    return json.loads(rows.export('json'))


@app.get(gen_uri("/index/{index_id}"))
async def getAPIList(index_id: int):
    checker = Checker(int)
    ok, message = checker.check(index_id)
    if not ok:
        return  JSONResponse(status_code=422, content={"message": message})
    rows = db.search_api_from_sotaindex(index_id)
    if len(rows.all()) == 0:
        return JSONResponse(status_code=400, content={"message": "无结果"})
    return json.loads(rows.export('json'))


@app.get(gen_uri("/detail/{item}"))
async def getAPIDetails(item: str):
    checker = Checker(str)
    ok, message = checker.check(item)
    if not ok:
        return  JSONResponse(status_code=422, content={"message": message})
    resp = db.api_col.find_one({"SDKName": item})
    resp["_id"] = str(resp["_id"])
    return resp