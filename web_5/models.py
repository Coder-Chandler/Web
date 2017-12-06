import json

from utils import log


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
        # 获取数据文件名称
        classname = cls.__name__
        # 拼接文件完整路径
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
        ms = [cls.new(m) for m in models]
        # log('ms是什么 -> ', ms)
        return ms

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def find_by(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """

        log('kwargs, ', kwargs)
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
            if v == m.__dict__[k]:
                return m
        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        用法如下，kwargs 是只有一个元素的 dict
        u = User.find_by(username='gua')
        """
        log('kwargs, ', kwargs)
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        # 首先通过all函数拿到models
        # 比如all = [< User password: (1212) username: (gua1) id: (1) > , ....]
        all = cls.all()
        data = []
        for m in all:
            # getattr(m, k) 等价于 m.__dict__[k]
            if v == m.__dict__[k]:
                data.append(m)
        return data

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        log('debug save')
        # 首先通过all函数拿到models
        # models = [< Todo id: (3) title: (喝水) user_id: (1) > , < Todo id: (6) title: (你好) user_id: (2) >]
        models = self.all()
        # log('models', models)
        # 设置文件数据的索引，从0开始
        first_index = 0
        # 判断数据是否有id，没有id说明是新添加的，有id说明是用户修改数据，没有那么就要给它加上id，
        # 如果没有id，那么有可能是第一个数据，那么id就为first_index = 0，不是第一条数据，那么就赋值为最后一条数据的id加上1。
        if self.__dict__.get('id') is None:
            # log("self.__dict__.get('id')", self.__dict__.get('id'))
            # 如果models的长度不是0，那么说明已经有数据了，那么这个数据就是新加入的，需要给他加上id
            if len(models) > 0:
                log('用 log 可以查看代码执行的走向')
                # 不是第一个数据，id为最后一条数据的id加1
                self.id = models[-1].id + 1
            else:
                # 是第一个数据的话，那id就是 first_index=0
                log('first index', first_index)
                self.id = first_index
            # 处理完数据的id之后就把这条数据加入到models里面
            models.append(self)
        else:
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
            # 这里判断index是否大于之前赋值的-1，大于-1说明数据已经修改了，
            # 那么就看看是否找到下标对应的这条数据，
            # 如果找到，就替换掉这条数据为修改的数据
            if index > -1:
                models[index] = self
        # 保存数据，把models转换一下，比如
        # [< Todo id: (3) title: (喝水) user_id: (1) > , < Todo id: (6) title: (你好) user_id: (2) >]转换为
        # [{'id': 3, 'title': '喝水', 'user_id': 1}, {'id': 6, 'title': '你好', 'user_id': 2}]
        l = [m.__dict__ for m in models]
        log('l是什么格式', l, type(l))
        # 找到保存数据的数据文件，谁调用就是谁的名字，比如u = User.new(form)，然后u.save(), 那么对应的文件其实就是User.txt
        path = self.db_path()
        # 调用外部的save函数保存数据，这里就相当于 save(l, 'db/User.txt')
        save(l, path)

    def remove(self):
        # 首先通过all函数拿到models
        # models = [< Todo id: (3) title: (喝水) user_id: (1) > , < Todo id: (6) title: (你好) user_id: (2) >]
        models = self.all()
        if self.__dict__.get('id') is not None:
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并删除
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
                # 判断models里面有没有一个id和要删除的这条数据id相等的，因为不相等的话，那就等于再删除不属于当前用户的数据，
                # 这是绝对不允许的，比如微信，你不可能可以删除别人的好友，对不对，这是绝对绝对不允许的。
                if m.id == self.id:
                    # 如果删除的是自己的数据，那么index就改为当前修改的数据的id
                    index = i
                    break
            # 这里判断index是否大于之前赋值的-1，大于-1说明数据已经删除了，
            # 那么就看看是否找到下标对应的这条数据，
            # 如果找到，就删除掉这条数据
            if index > -1:
                del models[index]
        # 保存
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        # return self.username == 'gua' and self.password == '123'
        # 首先找到u里面的username，通过调用User的类方法find_by
        # 比如 u --> < User id: (None) username: (gua1) password: (123) >
        # 那么取self.username就是 u = User.find_by(username={'username': 'gua1'})
        # 并返回这个对应用户的数据，比如 < User password: (1212) username: (gua1) id: (1) >
        u = User.find_by(username=self.username)
        # us = User.all()
        # for u in us:
        #     if u.username == self.username and u.password == self.password:
        #         return True
        # return False
        # 如果 u是None说明登录用户错误，如果正确的话，那么就比较密码，密码对了最后才能成功登录
        return u is not None and u.password == self.password
        # 这样的代码是不好的，不应该用隐式转换
        # return u and u.password == self.password
        """
        0 None ''
        """

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    """
    Message 是用来保存留言的 model
    """

    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')


def test():
    # users = User.all()
    # u = User.find_by(username='gua')
    # log('users', u)
    form = dict(
        username='gua',
        password='gua',
    )
    u = User(form)
    u.save()
    # u.save()
    # u.save()
    # u.save()
    # u.save()
    # u.save()
    # u = User.find_by(id=1)
    # u.username = '瓜'
    # u.save()


if __name__ == '__main__':
    test()
