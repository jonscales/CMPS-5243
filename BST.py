"""
Binary Search Tree Code
Code copied from bfaure/Python3_Data_Structures GitHub
https://github.com/bfaure/Python3_Data_Structures/blob/master/Binary_Search_Tree/main.py
"""
class node:
	def __init__(self,value=None):
		self.value=value
		self.left_child=None
		self.right_child=None
		self.parent=None # pointer to parent node in tree

class binary_search_tree:
	def __init__(self):
		self.root=None

	def insert(self,value):
		if self.root==None:
			self.root=node(value)
		else:
			self._insert(value,self.root)

	def _insert(self,value,cur_node):
		if value<cur_node.value:
			if cur_node.left_child==None:
				cur_node.left_child=node(value)
				cur_node.left_child.parent=cur_node # set parent
			else:
				self._insert(value,cur_node.left_child)
		elif value>cur_node.value:
			if cur_node.right_child==None:
				cur_node.right_child=node(value)
				cur_node.right_child.parent=cur_node # set parent
			else:
				self._insert(value,cur_node.right_child)
		else:
			print("Value already in tree!")

<<<<<<< HEAD
	def in_order_print(self):
		if self.root!=None:
			self._in_order_print(self.root)
	def pre_order_print(self):
		if self.root!=None:
			self._pre_order_print(self.root)		
	def post_order_print(self):
		if self.root!=None:
			self._post_order_print(self.root)

	def _in_order_print(self,cur_node):
		if cur_node!=None:
			self._in_order_print(cur_node.left_child)
			print (str(cur_node.value))
			self._in_order_print(cur_node.right_child)
	
	def _pre_order_print(self,cur_node):
		if cur_node!=None:
			print (str(cur_node.value))
			self._pre_order_print(cur_node.left_child)
			self._pre_order_print(cur_node.right_child)

	def _post_order_print(self,cur_node):
		if cur_node!=None:
			self._post_order_print(cur_node.left_child)
			self._post_order_print(cur_node.right_child)		
			print (str(cur_node.value))
=======
	def inorder_print(self):
		if self.root!=None:
			self._inorder_print(self.root)

	def preorder_print(self):
		if self.root!=None:
			self._preorder_print(self.root)

	def postorder_print(self):
		if self.root!=None:
			self._postorder_print(self.root)				

	def _inorder_print(self,cur_node):
		if cur_node!=None:
			self._inorder_print(cur_node.left_child)
			print (str(cur_node.value))
			self._inorder_print(cur_node.right_child)

	def _preorder_print(self,cur_node):
		if cur_node!=None:
			print (str(cur_node.value))
			self._preorder_print(cur_node.left_child)
			self._preorder_print(cur_node.right_child)

	def _postorder_print(self,cur_node):
		if cur_node!=None:
			self._postorder_print(cur_node.left_child)
			self._postorder_print(cur_node.right_child)	
			print (str(cur_node.value))			
>>>>>>> 413f5878e827789539e8ac109da078701e4a7008

	def height(self):
		if self.root!=None:
			return self._height(self.root,0)
		else:
			return 0

	def _height(self,cur_node,cur_height):
		if cur_node==None: return cur_height
		left_height=self._height(cur_node.left_child,cur_height+1)
		right_height=self._height(cur_node.right_child,cur_height+1)
		return max(left_height,right_height)

	def find(self,value):
		if self.root!=None:
			return self._find(value,self.root)
		else:
			return None

	def _find(self,value,cur_node):
		if value==cur_node.value:
			return cur_node
		elif value<cur_node.value and cur_node.left_child!=None:
			return self._find(value,cur_node.left_child)
		elif value>cur_node.value and cur_node.right_child!=None:
			return self._find(value,cur_node.right_child)

	def delete_value(self,value):
		return self.delete_node(self.find(value))

	def delete_node(self,node):

		## -----
		# Improvements since prior lesson

		# Protect against deleting a node not found in the tree
		if node==None or self.find(node.value)==None:
			print("Node to be deleted not found in the tree!")
			return None 
		## -----

		# returns the node with min value in tree rooted at input node
		def min_value_node(n):
			current=n
			while current.left_child!=None:
				current=current.left_child
			return current

		# returns the number of children for the specified node
		def num_children(n):
			num_children=0
			if n.left_child!=None: num_children+=1
			if n.right_child!=None: num_children+=1
			return num_children

		# get the parent of the node to be deleted
		node_parent=node.parent

		# get the number of children of the node to be deleted
		node_children=num_children(node)

		# break operation into different cases based on the
		# structure of the tree & node to be deleted

		# CASE 1 (node has no children)
		if node_children==0:

			# Added this if statement post-video, previously if you 
			# deleted the root node it would delete entire tree.
			if node_parent!=None:
				# remove reference to the node from the parent
				if node_parent.left_child==node:
					node_parent.left_child=None
				else:
					node_parent.right_child=None
			else:
				self.root=None

		# CASE 2 (node has a single child)
		if node_children==1:

			# get the single child node
			if node.left_child!=None:
				child=node.left_child
			else:
				child=node.right_child

			# Added this if statement post-video, previously if you 
			# deleted the root node it would delete entire tree.
			if node_parent!=None:
				# replace the node to be deleted with its child
				if node_parent.left_child==node:
					node_parent.left_child=child
				else:
					node_parent.right_child=child
			else:
				self.root=child

			# correct the parent pointer in node
			child.parent=node_parent

		# CASE 3 (node has two children)
		if node_children==2:

			# get the inorder successor of the deleted node
			successor=min_value_node(node.right_child)

			# copy the inorder successor's value to the node formerly
			# holding the value we wished to delete
			node.value=successor.value

			# delete the inorder successor now that it's value was
			# copied into the other node
			self.delete_node(successor)

	def search(self,value):
		if self.root!=None:
			return self._search(value,self.root)
		else:
			return False

	def _search(self,value,cur_node):
		if value==cur_node.value:
			return True
		elif value<cur_node.value and cur_node.left_child!=None:
			return self._search(value,cur_node.left_child)
		elif value>cur_node.value and cur_node.right_child!=None:
			return self._search(value,cur_node.right_child)
		return False 

<<<<<<< HEAD

testlist1=binary_search_tree()
testlist1.insert(52)
testlist1.insert(61)
testlist1.insert(19)
testlist1.insert(23)
testlist1.insert(47)
testlist1.insert(32)
testlist1.insert(75)
testlist1.insert(46)
testlist1.insert(15)

print("inorder print")
testlist1.in_order_print()
input("Press enter to continue")
print("preorder print")
testlist1.pre_order_print()
input("Press enter to continue")
print("postorder print")
testlist1.post_order_print()
=======
mybst=binary_search_tree() 

mybst.insert(52)
mybst.insert(61)
mybst.insert(19)
mybst.insert(23)
mybst.insert(47)
mybst.insert(32)
mybst.insert(75)
mybst.insert(46)
mybst.insert(15)

print("In order print of bst")
mybst.inorder_print() 

input("hit enter to continue")

print("pre=order print of bst")
mybst.preorder_print() 

input("hit enter to continue")

print("post-order print of bst")
mybst.postorder_print() 
>>>>>>> 413f5878e827789539e8ac109da078701e4a7008
