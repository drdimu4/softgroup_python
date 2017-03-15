class Tree:
    def __init__(self, value, root=None):
        # left and right child nodes
        self.lchild = None
        self.rchild = None
        # node value
        self.value = value
        # parent element for current node
        self.root = root
    def add(self, value):
        # track current node (level)
        current_node = self
        # track parent node
        last_node = None
        # search the place to insert new node
        while current_node:
            last_node = current_node
            if value > current_node.value:
                current_node = current_node.rchild
            elif value < current_node.value:
                current_node = current_node.lchild
            else:
             return False#element already presented in tree
        # create new node and link it with parent
        new_node = Tree(value, last_node)
        if value > last_node.value:
            last_node.rchild = new_node
        else:
            last_node.lchild = new_node
        return True
    def find(self,value):
        current_node = self
        while current_node:
            if value > current_node.value:
                current_node = current_node.rchild
            elif value < current_node.value:
                current_node = current_node.lchild
            else:
                print('True')
                return False#element already presented in tree
        return print('False')

    def print(self):
        stack = []
        p = self
        while True:
            if p == None:
                if not stack:
                    return
                p = stack.pop()
                p = p.rchild
                continue
            print (p.value) #Прямий обхід
            stack.append(p)
            p = p.lchild

root = Tree(10)
root.add(9)
root.add(8)
root.add(11)
root.add(2)
root.add(15)
root.add(12)
root.add(16)
root.find(10)
root.print()


