import json

from utils import log
import time


def save(data, path):
    """
        data 是 dict 或者 list
        path 是保存文件的路径
        """

    # 比如 save(l, 'db/User.txt')
    # 利用json的dumps来把l这个list转换为str
    """
    json.dumps把数据转换为str
    json.loads把数据转换为原来的格式
    json.dumps({"id": 3, "title": "dsfdsf", "user_id": 1}) --> '{"id": 3, "title": "dsfdsf", "user_id": 1}'
    json.loads('{"id": 3, "title": "dsfdsf", "user_id": 1}') --> {"id": 3, "title": "dsfdsf", "user_id": 1}
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    # 打开文件路径，比如'db/User.txt'，然后把dumps过的数据写进去
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    # 读取数据文件所有数据，通过json的loads方法
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


# Model 是一个 ORM（object relation mapper）
# 好处就是不需要关心存储数据的细节，直接使用即可
class Model(object):
    """
    Model 是所有 model 的基类
    @classmethod 是一个套路用法
    例如
    user = User()
    user.db_path() 返回 User.txt
    """
    @classmethod
    def db_path(cls):
        """
        cls 是类名, 谁调用的类名就是谁的
        classmethod 有一个参数是 class(这里我们用 cls 这个名字)
        所以我们可以得到 class 的名字
        """
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        # 通过db_path得到数据文件路径
        path = cls.db_path()
        # 通过load函数加载文件数据
        models = load(path)
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls.new(m) 可以初始化一个 cls 的实例
        # 比如models = [{'id': 3, 'title': '喝水', 'user_id': 1}, {'id': 6, 'title': '你好', 'user_id': 2},]
        # 经过 cls.new(m)之后 [< Todo id: (3) title: (喝水) user_id: (1) > , < Todo id: (6) title: (你好) user_id: (2) >]
        # log('models = load(path) -> ', models)
        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        ms = []
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        # 首先通过all函数拿到models
        # 比如all = [< User password: (1212) username: (gua1) id: (1) > , ....]
        all = cls.all()
        for m in all:
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                ms.append(m)
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs, type(kwargs))
        k, v = '', ''
        # 首先遍历出登录用户传入的username, 比如{'username': 'gua1'}
        for key, value in kwargs.items():
            # k='username', v='gua1'
            k, v = key, value
        # 首先通过all函数拿到models
        # 比如all = [< User password: (1212) username: (gua1) id: (1) > , ....]
        all = cls.all()
        # 遍历所有的用户数据
        for m in all:
            # getattr(m, k) 等价于 m.__dict__[k]
            # 判断v='gua1' 是否等于用户数据中某一条数据中的username，满足的话说明这个登录者就是我们的用户之一，
            # 那么就返回这个对应用户的数据m，比如 < User password: (1212) username: (gua1) id: (1) >
            # 也可以用 getattr(m, k) 取值
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def delete(cls, id):
        models = cls.all()
        index = -1
        # 用enumerate处理models这个list
        """
        enumerate用法: 
        l = ['a','ff','gg','wr4']
        for i, m in enumerate(l):
            print(i, m)

        output:
            0 a
            1 ff
            2 gg
            3 wr4
        """
        for i, e in enumerate(models):
            # 判断models里面有没有一个id和要删除的这条数据id相等的，因为不相等的话，那就等于再删除不属于当前用户的数据，
            # 这是绝对不允许的，比如微信，你不可能可以删除别人的好友，对不对，这是绝对绝对不允许的。
            if e.id == id:
                # 如果删除的是自己的数据，那么index就改为当前修改的数据的id
                index = i
                break
        # 这里判断index是否不等于之前赋值的-1，不等于-1说明数据已经删除了，
        # 如果找到，就删除掉这条数据
        if index == -1:
            # 没找到
            pass
        else:
            models.pop(index)
            # 保存
            l = [m.__dict__ for m in models]
            path = cls.db_path()
            save(l, path)

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        # log('debug save')
        # 首先通过all函数拿到models
        # models = [< Todo id: (3) title: (喝水) user_id: (1) > , < Todo id: (6) title: (你好) user_id: (2)
        models = self.all()
        # log('models', models)
        # 如果没有 id，说明是新添加的元素
        # 判断数据是否有id，没有id说明是新添加的，有id说明是用户修改数据，没有那么就要给它加上id，
        # 如果没有id，那么有可能是第一个数据，那么id就为1，不是第一条数据，那么就赋值为最后一条数据的id加上1
        if self.id is None:
            # 设置 self.id
            # 先看看是否是空 list
            if len(models) == 0:
                # 我们让第一个元素的 id 为 1（当然也可以为 0）
                self.id = 1
            else:
                # 不是第一个数据，id为最后一条数据的id加1
                m = models[-1]
                # log('m', m)
                self.id = m.id + 1
            # 处理完数据的id之后就把这条数据加入到models里面
            models.append(self)
        else:
            # index = self.find(self.id)
            # 有 id 说明已经是存在于数据文件中的数据，那么这就是编辑/修改数据
            # 那么就找到这条数据并替换之
            index = -1
            # 用enumerate处理models这个list
            """
            enumerate用法: 
            l = ['a','ff','gg','wr4']
            for i, m in enumerate(l):
                print(i, m)

            output:
                0 a
                1 ff
                2 gg
                3 wr4
            """
            for i, m in enumerate(models):
                # 判断models里面有没有一个id和修改的这条数据id相等的，因为不相等的话，那就等于再修改不属于当前用户的数据，
                # 这是绝对不允许的，比如微信，你不可能可以更改别人的用户名，对不对，这是绝对绝对不允许的。
                if m.id == self.id:
                    # 如果修改的是自己的数据，那么index就改为当前修改的数据的id
                    index = i
                    break
            log('debug', index)
            models[index] = self
        # 保存数据，把models转换一下，比如
        # [< Todo id: (3) title: (喝水) user_id: (1) > , < Todo id: (6) title: (你好) user_id: (2) >]转换为
        # [{'id': 3, 'title': '喝水', 'user_id': 1}, {'id': 6, 'title': '你好', 'user_id': 2}]
        l = [m.__dict__ for m in models]
        # 找到保存数据的数据文件，谁调用就是谁的名字，比如u = User.new(form)，然后u.save(), 那么对应的文件其实就是User.txt
        path = self.db_path()
        # 调用外部的save函数保存数据，这里就相当于 save(l, 'db/User.txt')
        save(l, path)


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.role = int(form.get('role', 10))

    def is_admin(self):
        return self.role == 1

    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.password
        else:
            return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    def todos(self):
        # 列表推倒和过滤
        # return [t for t in Todo.all() if t.user_id == self.id]
        ts = []
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)
        return ts


# 针对数据 TODO
# 要做 4 件事情
"""
C create 创建数据
R read 读取数据
U update 更新数据
D delete 删除数据

Todo.new() 来创建一个 todo
"""


class Todo(Model):
    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 todo 并且返回它
        Todo.new({'task': '吃饭'})
        :param form: 一个字典 包含了 todo 的数据
        :return: 创建的 todo 实例
        """
        # 下面一行相当于 t = Todo(form)
        t = cls(form, user_id)
        t.save()
        return t

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed'
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(t, key, form[key])
        # 修改更新时间
        t.updated_time = int(time.time())
        t.save()

    @classmethod
    def complete(cls, id, completed):
        """
        用法很方便
        Todo.complete(1, True)
        Todo.complete(2, False)
        """
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id

    def ct(self):
        format = '%H:%M:%S'
        value = time.localtime(self.created_time)
        dt = time.strftime(format, value)
        return dt

    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.task = form.get('task', '')
        self.completed = False
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        # 添加创建和修改时间
        self.created_time = form.get('created_time', None)
        self.updated_time = form.get('updated_time', None)
        if self.created_time is None:
            self.created_time = int(time.time())
            self.updated_time = self.created_time


# 微博类
class Tweet(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)

    def comments(self):
        return [c for c in Comment.all() if c.tweet_id == self.id]

# 评论类
class Comment(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.tweet_id = form.get('tweet_id', -1)


def test_tweet():
    # 用户 1 发微博
    form = {
        'content': 'hello tweet'
    }
    t = Tweet(form, 1)
    t.save()
    # 用户 2 评论微博
    form = {
        'content': '楼主说得对'
    }
    c = Comment(form, 2)
    c.tweet_id = 1
    c.save()
    # 取出微博 1 的所有评论
    t = Tweet.find(1)
    print('comments, ', t.comments())
    pass


def test():
    cs = Comment.find_all(user_id=2)
    print(cs, '评论数', len(cs))
    # test_tweet()
    # 测试数据关联
    # form = {
    #     'task': 'gua 的 todo'
    # }
    # Todo.new(form, 1)
    # 得到 user 的所有 todos
    # u1 = User.find(1)
    # u2 = User.find(2)
    # ts1 = u1.todos()
    # ts2 = u2.todos()
    # log('gua de todos', ts1)
    # log('xiao de todos', ts2)
    # assert len(ts1) > 0
    # assert len(ts2) == 0
    #
    # test_create()
    # test_read()
    # test_update()
    # test_delete()
    # Todo.complete(1, True)
    pass


# 假设要更新 id 1 的 todo 的完成状态
# 那么我们可以有两种方案
# # 方案 1 类方法
# form = {
#     'task': '再也不吃了',
#     'completed': True,
# }
# Todo.update(1, form)
#
# # 方案 2 查找出来再用实例方法更新
# t = Todo.get(1)
# t.update(form)
#
# # 方案 3 最野鸡的方案
# t = Todo.get(1)
# t.task = form.get('task', '')
# t.completed = True

# 写 what 不写 how
# 我们只关心结果，不关心过程和细节

def test_create():
    form = {
        'task': '吃瓜'
    }
    Todo.new(form)


def test_read():
    todos = Todo.all()
    # log('test read', todos)
    t = Todo.find(1)
    assert t is not None, 't is none'
    assert t.id == 1, 'id error'
    log('id 1 的 todo 是 ', t.task)


def test_update():
    form = {
        'id': 100,
        'task': '喝水 喝水',
    }
    Todo.update(1, form)
    #
    t = Todo.find(1)
    assert t.id == 1
    assert t.task == '喝水 喝水'


def test_delete():
    Todo.delete(2)
    t = Todo.find(2)
    assert t is None, '删除失败'


if __name__ == '__main__':
    test()
