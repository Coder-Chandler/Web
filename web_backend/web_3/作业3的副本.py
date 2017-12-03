# 2017/02/21
#
# ========


# 作业 3.1
#
# 更新 User 类的 validate_login
# 实现真正的验证
# 提示, 先读取所有 users, 然后验证用户名和密码是否匹配


# 作业 3.2
#
# 为 request 增加一下 headers 属性, 它是一个字典
# 保存了 HTTP 请求中的 header 区域的所有内容


# 作业 3.3
#
# 为 Model 添加一个类方法 find_by
# 用法和例子如下
"""
u = User.find_by(username='gua')

上面这句可以返回一个 username 属性为 'gua' 的 User 实例
如果有多条这样的数据, 返回第一个
如果没这样的数据, 返回 None

注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
"""


# 作业 3.4
#
# 为 Model 添加一个类方法 find_all
# 用法和例子如下
"""
us = User.find_all(password='123')
上面这句可以以 list 的形式返回所有 password 属性为 '123' 的 User 实例
如果没这样的数据, 返回 []

注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
"""


# 作业 3.5
#
# 对每一个 Model 添加一个 id 属性, 初始值为 None
# 每一个 Model 的 id 是独一无二并且增长的数字
# save 的时候, 如果 id 属性为 None 就给它赋值并添加/保存
# 如果 id 属性不为 None 就在所有数据中修改并保存
# 
# 用法例子如下
"""
# 假设有这个用户
u = User.find_by(username='gua')
u.password = 'pwd'
u.save()
# 直接保存


form = dict(
	username='newgua',
    password='123'
	)
u = User(form)
u.save()
# 因为这是一个新用户, 并没有 id
# 所以 save 的时候被赋予了一个 id
"""


# 作业 3.6
#
# 该看资料中提及的那本《head first html and css》了
# 另外请大致阅读下面这篇文章的内容(读读就好 不要求完全掌握)
http://www.ituring.com.cn/tupubarticle/1204