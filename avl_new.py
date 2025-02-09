"""
Jon Scales
Program 3
CMPS 5243 
Spring 2024
AVL Tree Program to store random words

"""

"""
CREDITS

The basis of this python AVL Tree Code was derived from code written by Brian Faure and taken from his github
bfaure/Python3_Data_Structures GitHub
https://github.com/bfaure/Python3_Data_Structures/blob/master/AVL_Tree/main.py 

Additional modifications were derived based on ChatGPT queries regarding python syntax

I removed methods for performing deletions to shorten the code. 

I added methods for calculating the average node height, complexity value, balance factor
node counter.  Some code was added to give nodes an ID # for output in graphviz and has 
no bearing on the other methods which count nodes and calculate average heights. 

Methods to produce a .dot file were added to aid in visualization of the tree structure. These methods
were provided by Tina Johnson and originated with Terry Griffin.  I modified them (with assistance of
ChatGPT) from C++ to python for use in this program
 
"""

import os
import math

""" syntax to generate path name for output of graphviz .dot file"""
script_dir=os.path.dirname(os.path.abspath(__file__))
outpath=os.path.join(script_dir, 'newavl.dot')

class Node:
    node_counter = 0 # class variable to generate node ID
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 0
        self.balance_factor = 0
        self.node_id=Node.node_counter # used for giving each node a numerical ID for output
        Node.node_counter +=1 # counter to generate the ID based on the order each word is inserted

class AVLTree:
    def __init__(self):
        """constructor method"""
        self.root = None
        self.num_nodes = 0
        self.sum_of_heights = 0

    def height(self, node):
        if node is None:
            return -1
        else:
            return node.height

    def update_height(self, node):
        """updates the height attribute of a node. called from rebalance method"""
        if node is not None:
            node.height = 1 + max(self.height(node.left), self.height(node.right))

    def update_balance_factor(self, node):
        """updates the balance factor attribute of a node. called from rebalance method"""
        if node is not None:
            node.balance_factor = self.height(node.left) - self.height(node.right)

    def rotate_left(self, x):
        """performs a left rotation on the node passed into the function, then calls update height
           and balance factor methods"""
        y = x.right
        x.right = y.left
        y.left = x
        self.update_height(x)
        self.update_height(y)
        self.update_balance_factor(x)
        self.update_balance_factor(y)
        return y

    def rotate_right(self, y):
        """performs a right rotation on the node passed into the function, then calls update height
           and balance factor methods"""
        x = y.left
        y.left = x.right
        x.right = y
        self.update_height(y)
        self.update_height(x)
        self.update_balance_factor(y)
        self.update_balance_factor(x)
        return x

    def rebalance(self, node):
        """calls update height & balance factor methods, then based on the balance factor of the 
           node, will call the appropriate rotation method to correct the bal factor to <2 or >-2"""
        self.update_height(node)
        self.update_balance_factor(node)
        if node.balance_factor == 2:
            if self.height(node.left.left) >= self.height(node.left.right):
                node = self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                node = self.rotate_right(node)
        elif node.balance_factor == -2:
            if self.height(node.right.right) >= self.height(node.right.left):
                node = self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                node = self.rotate_left(node)
        return node

    def insert(self, key):
        """Called to insert a word into the tree. Also increments the num_nodes attribute"""
        self.num_nodes += 1
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Called  by the public insert function to run recursively to put word into correct location"""
        if node is None:
            return Node(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        return self.rebalance(node)

    def complexity(self):
        """Returns the complexity of O(logn) for the size of the tree (n)"""
        return "{:.2f}".format(math.log(self.num_nodes, 2))

    def avg_height(self):
        """Returns the average height of the nodes"""
        return self.sum_of_heights/self.num_nodes
        
    def height_sum(self):
        """ will calculate a sum of the heights of all nodes in a tree. Is passed the tree itself
            then recursively calls each child until reaching leaf nodes. The sum of heights is stored
            as an attribute of the tree. The function also returns the value"""
        if self.root==None:
            self.sum_of_heights = 0
        else:
            self._height_sum(self.root)
        return self.sum_of_heights
            
    def _height_sum(self, cur_node):
        """ recursive height summation method called from the height_sum(root) method"""
        if cur_node != None:
            self.sum_of_heights += cur_node.height
            self._height_sum(cur_node.left)
            self._height_sum(cur_node.right)
                
    def tree_height(self):
        """ called to see if a tree exits, if so recursively calls _tree_height()"""
        if self.root!=None:
            return self._tree_height(self.root,0)

    def _tree_height(self,cur_node,cur_height):
        """recursive height function starts with the root & passes in child nodes until reaching leaf
            and adds height to node's height parameter. returns greatest of left or right path"""
        if cur_node==None: return cur_height
        left_height=self._tree_height(cur_node.left,cur_height+1)
        right_height=self._tree_height(cur_node.right,cur_height+1)
        return max(left_height,right_height)

    def calculate_heights(self):
        """public method to calculate node heights"""
        self._calculate_heights(self.root)

    def _calculate_heights(self, node, height=0):
        """private, recursive method to calculate all node heights"""
        if node is None: #base case stops at leaf node
            return
        node.height = height
        self._calculate_heights(node.left, height + 1)
        self._calculate_heights(node.right, height + 1)

    def calculate_balance_factors(self):
        """public method to calculate node balance factor"""
        self._calculate_balance_factors(self.root)

    def _calculate_balance_factors(self, node):
        """private, recursive method to calculate all node balance factors"""
        if node is None: # base case stops at leaf node
            return
        self.update_balance_factor(node)
        self._calculate_balance_factors(node.left)
        self._calculate_balance_factors(node.right)

    def inorder_print(self, node):
        """traverses tree in order and prints out node ID, key, height and balance factor"""
        if node:
            self.inorder_print(node.left)
            print(node.node_id, node.key, " H:", node.height, " BF:", node.balance_factor)
            self.inorder_print(node.right)
	
    #Methods to generate .dot file for use by GraphViz to visualize tree structure.
    #Credit to Terry Griffin via Tina Johnson
    def graphviz_get_ids(self, node, viz_out):
        """This method does an in-order read of the tree and create the node in the graphviz format"""
        if node:
            self.graphviz_get_ids(node.left, viz_out)
            viz_out.write(" node{} [label=\"{}-{}, H={}, BF={}\"];\n".format(node.node_id, node.node_id, node.key, node.height, node.balance_factor))
            self.graphviz_get_ids(node.right, viz_out)
        
    def graphviz_make_connections(self, node, viz_out):
        """ this method creates the connections between the existing nodes and addes them to the graphviz format"""
        if node:
            if node.left:
                viz_out.write("  node{} -> node{};\n".format(node.node_id, node.left.node_id))
                self.graphviz_make_connections(node.left, viz_out)
            if node.right:
                viz_out.write("  node{} -> node{};\n".format(node.node_id, node.right.node_id))
                self.graphviz_make_connections(node.right, viz_out)
                
    def graphviz_out(self,filename):
        """This is the parent method to call on the tree root to produce the graphviz .dot file"""
        with open(filename, 'w') as viz_out:
            viz_out.write("digraph g { \n")
            self.graphviz_get_ids(self.root, viz_out)
            self.graphviz_make_connections(self.root, viz_out)
            viz_out.write("} \n")

# Example usage:
avl = AVLTree()

#read in random words from text file and insert into tree
with open('words_20.txt','r') as file:
    for word in file:
        avl.insert(word.strip().lower())

#generate graphviz output
avl.graphviz_out(outpath)

#generate output and analysis
avl.inorder_print(avl.root)
print('The number of nodes in this AVL tree is : ', avl.num_nodes)
print('Tree height is : ', avl.tree_height())
print('O(log n) complexity value for this tree is : ', avl.complexity())
print('The total sum of all node heights is : ', avl.height_sum())
print('The average node height is : ', avl.avg_height())
