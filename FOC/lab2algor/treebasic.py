
class BinaryTreeNode():

    def __init__(self,value):
        self.value = value
        self.leftChild = None
        self.rightChild = None

    """
    These getter and setter methods are here to highlight
    the kinds of data you want to access or retrieve.
    """
    def getLeftChild(self):
        return self.leftChild

    def getRightChild(self):
        return self.rightChild

    def getValue(self):
        return self.value

    def setLeftChild(self,node):
        self.leftChild = node

    def setRightChild(self,node):
        self.rightChild = node

    def setValue(self,value):
        self.value = value

class BinaryTree():
    def __init__(self,rootValue):
        self.root = BinaryTreeNode(rootValue)

    def getRootNode(self):
        return self.root

    def insertAtRoot(self,value):
        self.insert(self.root,value)

    def insert(self,value,parent=None):
        if parent == None:
            parent=self.getRootNode()
        child=BinaryTreeNode(value)
        if value<parent.value :
            if parent.leftChild==None:
                parent.leftChild=child
            else:
                self.insert(value,parent=parent.leftChild)
        else:
            if parent.rightChild==None:
                parent.rightChild=child
            else:
                self.insert(value,parent=parent.rightChild)

    def BFS(self,queue=[]):
        if not queue:
            queue.append(self.getRootNode())
        current=queue.pop(0)
        print(current.getValue())
        if current.leftChild:
            queue.append(current.leftChild)
        if current.rightChild:
            queue.append(current.rightChild)

        if len(queue)==0:
            pass
        else:
            self.BFS(queue)

def DFSInOrder(node):
    leftChild = node.getLeftChild()
    if(leftChild is not None):
        DFSInOrder(leftChild)

    print (node.getValue())

    rightChild = node.getRightChild()
    if(rightChild is not None):
        DFSInOrder(rightChild)

def DFSPreOrder(node):
    print (node.getValue())

    leftChild = node.getLeftChild()
    if(leftChild is not None):
        DFSPreOrder(leftChild)

    rightChild = node.getRightChild()
    if(rightChild is not None):
        DFSPreOrder(rightChild)

def DFSPostOrder(node):
    leftChild = node.getLeftChild()
    if(leftChild is not None):
        DFSPostOrder(leftChild)

    rightChild = node.getRightChild()
    if(rightChild is not None):
        DFSPostOrder(rightChild)

    print (node.getValue())

def main():
    value=int(input('enter node to tree: '))
    bTree=BinaryTree(value)
    while True:
        try:
            value=int(input('enter node to tree or enter 0 to finish: '))
            bTree.insert(value)
        except (ValueError):
            break
    bTree.BFS()
    DFSPreOrder(bTree.getRootNode())
    DFSInOrder(bTree.getRootNode())
    DFSPostOrder(bTree.getRootNode())

if __name__ == "__main__":
    main()
