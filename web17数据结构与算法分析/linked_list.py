class Node(object):
    def __init__(self, element=-1):
        self.element = element
        self.next = None


"""
不完整的链表实现, 自行补全
"""


class LinkedList(object):
    def __init__(self):
        self.head = None
        self.size = 0

    # O(1)
    def is_empty(self):
        return self.head is None

    def length(self):
        index = 0
        node = self.head
        while node is not None:
            index += 1
            node = node.next
        return index

    def find(self, element):
        node = self.head
        while node is not None:
            if node.element == element:
                break
            node = node.next
        return node

    def _node_at_index(self, index):
        i = 0
        node = self.head
        while node is not None:
            if i == index:
                return node
            node = node.next
            i += 1
        return None

    def element_at_index(self, index):
        node = self._node_at_index(index)
        return node.element

    # O(n)
    def insert_before_index(self, position, element):
        this_node = self._node_at_index(position)
        pre_node = self._node_at_index(position - 1)
        new_node = Node(element)
        new_node.next = this_node
        pre_node.next = new_node
        self.size += 1

    # O(n)
    def insert_after_index(self, position, element):
        this_node = self._node_at_index(position)
        last_node = self._node_at_index(position + 1)
        new_node = Node(element)
        this_node.next = new_node
        new_node.next = last_node
        self.size += 1

        # O(1)
    def first_object(self):
        return self.head.next

    # O(n)
    def last_object(self):
        index = self.size-1
        last_node = self._node_at_index(index)
        return last_node

    # O(n)
    def append(self, node):
        tmp = Node(node)
        if self.head is None:
            self.head = tmp
            self.size += 1
        else:
            last_node = self.last_object()
            last_node.next = tmp
            # tmp.front = last_node
            self.size += 1


l = LinkedList()
l.append(31)
l.append(2)
l.append(3)
l.append(8)
l.append(9)
l.insert_before_index(2, 1000)
l.insert_after_index(4, 2000)


def log_list():
    i = 0
    s = ''
    linklist = l
    this_node = linklist.head
    while this_node is not None:
        s += (str(linklist.element_at_index(i)) + ' -> ')
        this_node = this_node.next
        i += 1
    print(linklist.length())
    print(s)


if __name__ == '__main__':
    log_list()

