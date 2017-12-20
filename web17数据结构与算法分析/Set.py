class Set(object):
    # ...
    def __init__(self, *args):
        self.data = []
        for i in args:
            if i not in self.data:
                self.data.append(i)

    def __repr__(self):
        return str(self.data)

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        pass

    def remove(self, x):
        if x not in self.data:
            return False
        for i in range(len(self.data)):
            if self.data[i] == x:
                del self.data[i]

    def add(self, x):
        if x not in self.data:
            self.data.append(x)

    def has(self, x):
        if x in self.data:
            return True
        return False


def testSet():
    a = Set(1, 2, 2, 3, 4, 4)
    b = Set(1, 2, 2, 3, 4)
    c = Set(1, 3, 4, 2)
    d = Set(2, 3)
    print('ssssss')
    print(type(a))
    # assert (str(a) == '{1, 2, 3, 4}')
    print(a,b,c,d)
    # assert (a == b)
    # assert (a == c)
    # assert (a != d)
    # assert (a.has(1) == True)
    a.remove(1)
    # assert (a.has(1) == False)
    a.add(1)
    # assert (a.has(1) == True)

testSet()