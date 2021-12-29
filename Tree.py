class Tree:
  def __init__(self, root_value = None, depth=0):
    self.root = root_value
    self.children = [] 
    self.depth = depth
  
  def getRoot(self):
    return self.root
  
  def getDepth(self):
    return self.depth
  
  def getChildren(self):
    return self.children
  
  def insert(self, node):
    if self.root:
      self.children.append(Tree(node, self.depth+1))
    else:
      self.root = node
  
  def printTree(self, root):
    if (root.getRoot() == None):
      print("empty root")
      return None
    q = [] 
    q.append(root)
    while (len(q) != 0):
      n = len(q)
      while (n > 0):
        p = q[0]
        q.pop(0);
        print(p.root, end=" ")
        for i in range(len(p.children)):
          q.append(p.children[i]);
        n -= 1
      print()
      

if __name__ == "__main__":
  test1 = Tree()
  print("Empty Tree created")
  test1.printTree(test1)


  test = Tree([1,1,2])
  print("next Tree created")
  print("depth :",test.getDepth())
  print()

  test.insert([1,1.5])
  test.insert([1,4,5,1])
  test.printTree(test)
  print("depth :",test.getChildren()[1].getDepth())

  child = test.getChildren()[1]
  child.insert([7,7])
  test.printTree(test)
  print("depth :", child.getChildren()[0].getDepth())