
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

    def insert(self,parent,value):
        pass

def main():
    pass

if __name__ == "__main__":
    main()
