#coding:utf-8

class Checker:
    def __init__(self, check_type, length=-1):
        self.type = check_type
        self.length = length
    
    def check(self,value):
        '''
        返回参数：
        状态类型， 错误信息
        '''
        status = 1 # okay
        message = ""
        if type(value) != self.type:
            status = 0
            message = "类型错误: 请输入正确的参数类型"
            return status,message
        if self.length != -1:
            if len(value) > self.length:
                status = 0
                message = "长度超过规定"
        return status,message