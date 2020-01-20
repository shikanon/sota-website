#coding:utf-8
import database
import pytest
import datetime
import time
import json
import random

db = database.DB()
db.reset()

def test_insert_api_record_data():
    api_index_records = [
        {
            "name": "基础模型",
            "APIType": "官方模型",
            "TypeID": 0,
            "Image": "icon-concept.svg"
        },
        {
            "name": "SOTA模型",
            "APIType": "官方模型",
            "TypeID": 0,
            "Image": "icon-concept.svg"
        },
        {
            "name": "工业",
            "TypeID": 1,
            "APIType": "行业解决方案",
            "Image": "icon-concept.svg"
        },
        {
            "name": "交通",
            "TypeID": 1,
            "APIType": "行业解决方案",
            "Image": "icon-concept.svg"
        },
        {
            "name": "教育",
            "TypeID": 1,
            "APIType": "行业解决方案",
            "Image": "icon-concept.svg"
        },
        {
            "name": "公开数据集",
            "TypeID": 2,
            "APIType": "数据集",
            "Image": "icon-concept.svg"
        },
        {
            "name": "行业数据集",
            "TypeID": 2,
            "APIType": "数据集",
            "Image": "icon-concept.svg"
        }
    ]

    db.insert_sotaindex(api_index_records)

    rows = db.get_sotaindex()
    result = json.loads(rows.export('json'))
    assert len(result) == len(api_index_records)

    api_record_origin = {
        "name": "坐姿识别",
        "index_id": 1,
        "APIGroup": "行为识别", # API组，属于API种类下的子类
        "APIGroupDescription": "APIGroupDescription...",
        "APIClass": "图像识别", # API种类，如图像生成、人脸识别
        "DeploymentTime": datetime.datetime.now(), # API部署时间
        "APIClassDescription": "APIClassDescription...",
        "Description": "接口描述....",
        }
    api_records = [api_record_origin]
    for i in range(20):
        api_record_copy = api_record_origin.copy()
        api_record_copy["name"] = "骨架识别%s"%(i)
        api_record_copy["APIGroup"] = "行为识别%s"%(random.randint(0,i))
        api_record_copy["APIClass"] = "图像识别%s"%(i)
        api_record_copy["index_id"] = random.randint(1,4)
        api_records.append(api_record_copy)

    db.insert_api(api_records)
    rows = db.search_api_from_sotaindex(1)
    result = json.loads(rows.export('json'))
    assert len(result) == len([r for r in api_records if r["index_id"]==1])


test_insert_api_record_data()

def test_mongo_db():
    # mongodb客户端

    data_class = {
        "name": "坐姿识别v1", # API NAME
        "version": "v1",
        "SDKName": "坐姿识别",
        "APIGroup": "行为识别", # API组，属于API种类下的子类
        "SDK":{
            "SdkDemos": { # SDK demo
                "SdkDemo": [
                    {
                        "IdeKey": "curl",
                        "CallDemo": "curl -i -k -X POST 'https://goodsdect.market.alicloudapi.com/goodsdect'  -H 'Authorization:APPCODE 你自己的AppCode' --data 'src=%E5%9B%BE%E7%89%87base64%E7%BC%96%E7%A0%81'"
                    },
                    {
                        "IdeKey": "Java",
                        "CallDemo": "\tpublic static void main(String[] args) {\r\n\t    String host = \"https://goodsdect.market.alicloudapi.com\";\r\n\t    String path = \"/goodsdect\";\r\n\t    String method = \"POST\";\r\n\t    String appcode = \"你自己的AppCode\";\r\n\t    Map<String, String> headers = new HashMap<String, String>();\r\n\t    //最后在header中的格式(中间是英文空格)为Authorization:APPCODE 83359fd73fe94948385f570e3c139105\r\n\t    headers.put(\"Authorization\", \"APPCODE \" + appcode);\r\n\t    //根据API的要求，定义相对应的Content-Type\r\n\t    headers.put(\"Content-Type\", \"application/x-www-form-urlencoded; charset=UTF-8\");\r\n\t    Map<String, String> querys = new HashMap<String, String>();\r\n\t    Map<String, String> bodys = new HashMap<String, String>();\r\n\t    bodys.put(\"src\", \"图片base64编码\");\r\n\r\n\r\n\t    try {\r\n\t    \t/**\r\n\t    \t* 重要提示如下:\r\n\t    \t* HttpUtils请从\r\n\t    \t* https://github.com/aliyun/api-gateway-demo-sign-java/blob/master/src/main/java/com/aliyun/api/gateway/demo/util/HttpUtils.java\r\n\t    \t* 下载\r\n\t    \t*\r\n\t    \t* 相应的依赖请参照\r\n\t    \t* https://github.com/aliyun/api-gateway-demo-sign-java/blob/master/pom.xml\r\n\t    \t*/\r\n\t    \tHttpResponse response = HttpUtils.doPost(host, path, method, headers, querys, bodys);\r\n\t    \tSystem.out.println(response.toString());\r\n\t    \t//获取response的body\r\n\t    \t//System.out.println(EntityUtils.toString(response.getEntity()));\r\n\t    } catch (Exception e) {\r\n\t    \te.printStackTrace();\r\n\t    }\r\n\t}\r\n"
                    },
                    {
                        "IdeKey": "C#",
                        "CallDemo": "//using System.IO;\r\n//using System.Text;\r\n//using System.Net;\r\n//using System.Net.Security;\r\n//using System.Security.Cryptography.X509Certificates;\r\n\r\n        private const String host = \"https://goodsdect.market.alicloudapi.com\";\r\n        private const String path = \"/goodsdect\";\r\n        private const String method = \"POST\";\r\n        private const String appcode = \"你自己的AppCode\";\r\n\r\n        static void Main(string[] args)\r\n        {\r\n            String querys = \"\";\r\n            String bodys = \"src=%E5%9B%BE%E7%89%87base64%E7%BC%96%E7%A0%81\";\r\n            String url = host + path;\r\n            HttpWebRequest httpRequest = null;\r\n            HttpWebResponse httpResponse = null;\r\n\r\n            if (0 < querys.Length)\r\n            {\r\n                url = url + \"?\" + querys;\r\n            }\r\n\r\n            if (host.Contains(\"https://\"))\r\n            {\r\n                ServicePointManager.ServerCertificateValidationCallback = new RemoteCertificateValidationCallback(CheckValidationResult);\r\n                httpRequest = (HttpWebRequest)WebRequest.CreateDefault(new Uri(url));\r\n            }\r\n            else\r\n            {\r\n                httpRequest = (HttpWebRequest)WebRequest.Create(url);\r\n            }\r\n            httpRequest.Method = method;\r\n            httpRequest.Headers.Add(\"Authorization\", \"APPCODE \" + appcode);\r\n            //根据API的要求，定义相对应的Content-Type\r\n            httpRequest.ContentType = \"application/x-www-form-urlencoded; charset=UTF-8\";\r\n            if (0 < bodys.Length)\r\n            {\r\n                byte[] data = Encoding.UTF8.GetBytes(bodys);\r\n                using (Stream stream = httpRequest.GetRequestStream())\r\n                {\r\n                    stream.Write(data, 0, data.Length);\r\n                }\r\n            }\r\n            try\r\n            {\r\n                httpResponse = (HttpWebResponse)httpRequest.GetResponse();\r\n            }\r\n            catch (WebException ex)\r\n            {\r\n                httpResponse = (HttpWebResponse)ex.Response;\r\n            }\r\n\r\n            Console.WriteLine(httpResponse.StatusCode);\r\n            Console.WriteLine(httpResponse.Method);\r\n            Console.WriteLine(httpResponse.Headers);\r\n            Stream st = httpResponse.GetResponseStream();\r\n            StreamReader reader = new StreamReader(st, Encoding.GetEncoding(\"utf-8\"));\r\n            Console.WriteLine(reader.ReadToEnd());\r\n            Console.WriteLine(\"\\n\");\r\n\r\n        }\r\n\r\n        public static bool CheckValidationResult(object sender, X509Certificate certificate, X509Chain chain, SslPolicyErrors errors)\r\n        {\r\n            return true;\r\n        }\r\n"
                    },
                    {
                        "IdeKey": "PHP",
                        "CallDemo": "<?php\r\n    $host = \"https://goodsdect.market.alicloudapi.com\";\r\n    $path = \"/goodsdect\";\r\n    $method = \"POST\";\r\n    $appcode = \"你自己的AppCode\";\r\n    $headers = array();\r\n    array_push($headers, \"Authorization:APPCODE \" . $appcode);\r\n    //根据API的要求，定义相对应的Content-Type\r\n    array_push($headers, \"Content-Type\".\":\".\"application/x-www-form-urlencoded; charset=UTF-8\");\r\n    $querys = \"\";\r\n    $bodys = \"src=%E5%9B%BE%E7%89%87base64%E7%BC%96%E7%A0%81\";\r\n    $url = $host . $path;\r\n\r\n    $curl = curl_init();\r\n    curl_setopt($curl, CURLOPT_CUSTOMREQUEST, $method);\r\n    curl_setopt($curl, CURLOPT_URL, $url);\r\n    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);\r\n    curl_setopt($curl, CURLOPT_FAILONERROR, false);\r\n    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);\r\n    curl_setopt($curl, CURLOPT_HEADER, true);\r\n    if (1 == strpos(\"$\".$host, \"https://\"))\r\n    {\r\n        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);\r\n        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false);\r\n    }\r\n    curl_setopt($curl, CURLOPT_POSTFIELDS, $bodys);\r\n    var_dump(curl_exec($curl));\r\n?>"
                    },
                    {
                        "IdeKey": "Python",
                        "CallDemo": "import urllib, urllib2, sys\r\nimport ssl\r\n\r\n\r\nhost = 'https://goodsdect.market.alicloudapi.com'\r\npath = '/goodsdect'\r\nmethod = 'POST'\r\nappcode = '你自己的AppCode'\r\nquerys = ''\r\nbodys = {}\r\nurl = host + path\r\n\r\nbodys['src'] = '''图片base64编码'''\r\npost_data = urllib.urlencode(bodys)\r\nrequest = urllib2.Request(url, post_data)\r\nrequest.add_header('Authorization', 'APPCODE ' + appcode)\r\n//根据API的要求，定义相对应的Content-Type\r\nrequest.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')\r\nctx = ssl.create_default_context()\r\nctx.check_hostname = False\r\nctx.verify_mode = ssl.CERT_NONE\r\nresponse = urllib2.urlopen(request, context=ctx)\r\ncontent = response.read()\r\nif (content):\r\n    print(content)\r\n"
                    },
                    {
                        "IdeKey": "ObjectC",
                        "CallDemo": "NSString *appcode = @\"你自己的AppCode\";\r\nNSString *host = @\"https://goodsdect.market.alicloudapi.com\";\r\nNSString *path = @\"/goodsdect\";\r\nNSString *method = @\"POST\";\r\nNSString *querys = @\"\";\r\nNSString *url = [NSString stringWithFormat:@\"%@%@%@\",  host,  path , querys];\r\nNSString *bodys = @\"src=%E5%9B%BE%E7%89%87base64%E7%BC%96%E7%A0%81\";\r\n\r\nNSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:[NSURL URLWithString: url]  cachePolicy:1  timeoutInterval:  5];\r\nrequest.HTTPMethod  =  method;\r\n[request addValue:  [NSString  stringWithFormat:@\"APPCODE %@\" ,  appcode]  forHTTPHeaderField:  @\"Authorization\"];\r\n[request addValue: @\"application/x-www-form-urlencoded; charset=UTF-8\" forHTTPHeaderField: @\"Content-Type\"];\r\nNSData *data = [bodys dataUsingEncoding: NSUTF8StringEncoding];\r\n[request setHTTPBody: data];\r\nNSURLSession *requestSession = [NSURLSession sessionWithConfiguration:[NSURLSessionConfiguration defaultSessionConfiguration]];\r\nNSURLSessionDataTask *task = [requestSession dataTaskWithRequest:request\r\n    completionHandler:^(NSData * _Nullable body , NSURLResponse * _Nullable response, NSError * _Nullable error) {\r\n    NSLog(@\"Response object: %@\" , response);\r\n    NSString *bodyString = [[NSString alloc] initWithData:body encoding:NSUTF8StringEncoding];\r\n\r\n    //打印应答中的body\r\n    NSLog(@\"Response body: %@\" , bodyString);\r\n    }];\r\n\r\n[task resume];"
                    }
                ]
            },
            "Description": "商品识别",
            "RequestQueries": {
                "RequestParam": []
            },
            "PathParameters": {
                "PathParameter": []
            },
            "ErrorCodeSamples": {
                "ErrorCodeSample": []
            },
            "HttpProtocol": "HTTP,HTTPS",
            "ResultDescriptions": {
                "ResultDescription": []
            },
            "RequestHeaders": {
                "RequestParam": []
            },
            "RequestBody": {
                "RequestParam": [
                    {
                        "DemoValue": "图片base64编码",
                        "DefaultValue": "无",
                        "ParameterType": "STRING",
                        "Description": "图片base64编码",
                        "Required": "REQUIRED",
                        "ApiParameterName": "src"
                    }
                ]
            },
            "Path": "/goodsdect",
            "ResultSample": "{\"status\":200,\"msg\":[{\"description\":\"个人护理\",\"score\":0.9782632,\"topicality\":0.9782632}]}",
            "StageName": "RELEASE",
            "ResultType": "JSON",
            "FailResultSample": "{\"status\":500}",
            "ServiceTimeout": 10000,
            "BodyFormat": "FORM",
            "HttpMethod": "POST"
        }
    }

    data_copy = data_class.copy()
    data_copy2 = data_class.copy()
    data_copy["name"] = "坐姿识别v2"
    data_copy["version"] = "v2"
    data_copy2["name"] = "坐姿识别v3"
    data_copy2["version"] = "v3"

    
    db.api_col.insert_one(data_class)
    db.api_col.insert_many([data_copy, data_copy2])
    result = db.api_col.find({"SDKName": "坐姿识别"})
    assert len([r for r in result])==3
    result = db.api_col.find_one({"name": "坐姿识别v1"})
    assert result == data_class

test_mongo_db()