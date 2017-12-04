"""
课 4 上课内容预习
2017/02/21


本次上课的主要内容如下(都是概念性的内容, 需要上课解释)

cookie 是什么
客户端和服务器怎么实现 cookie
session 是什么
session 有什么用
客户端和服务器怎么实现 session
session 持久化（持久化就是重启后仍然可以使用）的两种方式
    保存到文件
    对称加密
session 共享


如何调试代码
    1，确定错误的根源，写一点测一点，写几行测几行，确保及早发现问题
    2，用 二分法 来查找问题的根源
    3，用 log 来查看代码是否被执行
    4，用 log 来查看变量的值是否是我们期待的值

作业中 model 类的新增方法实现
如何管理重复的数据
如何查找数据
"""


"""
POST /login?id=2 HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Content-Length: 25
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Cookie: Pycharm-7367d7d5=bf094603-b9e9-4994-9ebd-564f1f5ad2c0

username=gua&password=123
"""

"""
2017/02/22 19:42:48 login 的响应
HTTP/1.1 210 VERY OK
Content-Type: text/html
Set-Cookie: user=gua1

<html>
"""

"""
2017/02/22 19:45:16 ip and request, ('127.0.0.1', 50317)
GET /login HTTP/1.1
Host: localhost:3000
Connection: keep-alive
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Cookie: user=gua1
"""