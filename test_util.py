#coding:utf-8
import util

def test_check():
    check = util.Checker(int)
    assert check.check(1) == ""
    assert check.check("1") == "类型错误: 请输入正确的参数类型"
