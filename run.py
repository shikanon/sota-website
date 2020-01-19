#coding:utf-8
import database
import json
from collections import defaultdict
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, HttpUrl
from starlette.responses import JSONResponse, UJSONResponse
from starlette.middleware.cors import CORSMiddleware
from util import Checker


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

db = database.DB()

# 版本号
version = "v1"

def gen_uri(url):
    return "/sota/api/%s"%(version) + url


@app.get(gen_uri("/index"))
async def getAPIIndex():
    """
    获取SOTA首页类别:

    用于获取SOTA模块首页接口类别展示。
    """
    rows = db.get_sotaindex()
    query_data = json.loads(rows.export('json'))
    result = defaultdict(list)
    for q in query_data:
        result[q["APIType"]].append(q)
    return result


@app.get(gen_uri("/category/{index_id}"))
async def getAPICategory(index_id: int):
    """
    获取API类别:

    通过首页大类(index)获取API类别(category)。
    """
    checker = Checker(int)
    ok, message = checker.check(index_id)
    if not ok:
        return  JSONResponse(status_code=422, content={"message": message})
    search_sql = 'select APIClass from api where index_id=:index_id'
    rows = db.record_db.query(search_sql, index_id=index_id)
    if len(rows.all()) == 0:
        return JSONResponse(status_code=400, content={"message": "无结果"})
    result = [i["APIClass"] for i in json.loads(rows.export('json'))]
    return result


@app.get(gen_uri("/api-list/"))
async def getAPIList(APIClass: str):
    """
    获取API详细列表:

    通过API类别(category)获取APIGroup列表。
    """
    checker = Checker(str)
    ok, message = checker.check(APIClass)
    if not ok:
        return  JSONResponse(status_code=422, content={"message": message})
    search_sql = 'select * from api where APIClass=:APIClass'
    rows = db.record_db.query(search_sql, APIClass=APIClass)
    if len(rows.all()) == 0:
        return JSONResponse(status_code=400, content={"message": "无结果"})
    query_data = json.loads(rows.export('json'))
    result = dict()
    result["APIClass"] = query_data[0]["APIClass"]
    result["APIClassDescription"] = query_data[0]["APIClassDescription"]
    result["data"] = list()
    for q in query_data:
        result["data"].append({k:q[k] for k in q if k in ["name", "APIGroup", "APIGroupDescription"]})
    return result


@app.get(gen_uri("/api-group"))
async def getAPIGroup(APIGroup: str=None, SDKName: str=None):
    """
    获取具体的open API详细用例:

    通过API Group(或者SDK名称) 获取每个具体的open API/SDK用例。
    """
    if APIGroup == None and SDKName == None:
        return JSONResponse(status_code=422, content={"message": "不能两个参数同时为空"})
    checker = Checker(str)
    ok, message = checker.check(APIGroup)
    if not ok:
        return  JSONResponse(status_code=422, content={"message": message})
    ok, message = checker.check(SDKName)
    if not ok:
        return  JSONResponse(status_code=422, content={"message": message})
    if APIGroup != None:
        resp = db.api_col.find({"APIGroup": APIGroup})
        result = list()
        for r in resp:
            r["_id"] = str(r["_id"])
            print(r)
            result.append(r)
    if SDKName != None:
        resp = db.api_col.find_one({"SDKName": SDKName})
        resp["_id"] = str(resp["_id"])
    return result

