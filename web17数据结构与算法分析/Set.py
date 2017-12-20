class Set(object):
    def __init__(self):
        self.table_size = 10007
        self.table = [0] * self.table_size

    def add(self, key):
        index = self._index(key)
        data = [key]
        v = self.table[index]
        if isinstance(v, int):
            self.table[index] = [data]
        else:
            self.table.append(data)

    def get(self, key):
        index = self._index(key)
        v = self.table[index]
        if isinstance(v, list):
            for kv in v:
                if kv[0] == key:
                    return kv[0]
        return None

    def remove(self, key):
        index = self._index(key)
        v = self.table[index]
        if isinstance(v, list):
            for kv in v:
                if kv[0] == key:
                    self.table[index].remove(kv)

    def __contains__(self, item):
        return self.has_key(item)

    def has_key(self, key):
        index = self._index(key)
        v = self.table[index]
        if isinstance(v, list):
            for kv in v:
                if kv[0] == key:
                    return True
        return False

    def _index(self, key):
        return self._hash(key) % self.table_size

    def _hash(self, s):
        assert isinstance(s, str)
        n = 1
        f = 10
        for i in s:
            n += ord(i) * f
            f *= 10
        return n


def test():
    names = [
        'xia',
        'yin',
        'chandler',
        'coder',
    ]

    s = Set()
    for i in names:
        s.add(i)
        print('add 元素', i)
    s.remove('coder')
    print('coder 已经被删除，get返回应该是None -> ', s.get('coder'))
    print('获取 xia 这个key -> ', s.get('xia'))


test()
