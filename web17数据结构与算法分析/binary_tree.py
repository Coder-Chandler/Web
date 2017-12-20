class Tree(object):
    def __init__(self, element=None):
        self.element = element
        self.left = None
        self.right = None

    def fro_traversal(self):
        """
        树的前序遍历, 是一个递归操作
        """
        print(self.element)
        if self.left is not None:
            self.left.fro_traversal()
        if self.right is not None:
            self.right.fro_traversal()

    def mid_traversal(self):
        """
        树的中序遍历, 是一个递归操作
        """
        if self.left is not None:
            self.left.mid_traversal()
        print(self.element)
        if self.right is not None:
            self.right.mid_traversal()

    def bac_traversal(self):
        """
        树的后序遍历, 是一个递归操作
        """
        if self.left is not None:
            self.left.bac_traversal()
        if self.right is not None:
            self.right.bac_traversal()
        print(self.element)

    def reverse(self):
        """
        反转二叉树
        """
        self.left, self.right = self.right, self.left
        if self.left is not None:
            self.left.reverse()
        if self.right is not None:
            self.right.reverse()


def test():
    # 手动构建二叉树
    # 为什么手动这么麻烦呢, 因为一般都是自动生成的
    # 这里只需要掌握性质就好
    t = Tree(0)
    left = Tree(1)
    right = Tree(2)
    t.left = left
    t.right = right
    # 遍历
    t.fro_traversal()
    t.mid_traversal()
    t.bac_traversal()
    print('反转二叉树')
    t.reverse()
    t.fro_traversal()
    t.mid_traversal()
    t.bac_traversal()


if __name__ == '__main__':
    test()