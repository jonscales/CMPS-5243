"""
AVL Tree Code
Code copied from bfaure/Python3_Data_Structures GitHub
https://github.com/bfaure/Python3_Data_Structures/blob/master/AVL_Tree/main.py
"""
class node:
	def __init__(self,word=None):
		self.word=word
		self.left_child=None
		self.right_child=None
		self.parent=None # pointer to parent node in tree
		self.height=1 # height of node in tree (max dist. to leaf) NEW FOR AVL
		self.balance_factor=0 # store a balance factor calculated from the height calculations

class AVLTree:
	def __init__(self):
		"""constructor method"""
		self.root=None

	def __repr__(self):
		"""function to display the tree sort of """
		if self.root==None: return ''
		content='\n' # to hold final string
		cur_nodes=[self.root] # all nodes at current level
		cur_height=self.root.height # height of nodes at current level
		sep=' '*(2**(cur_height-2)) # variable sized separator between elements
		while True:
			cur_height+=-1 # decrement current height
			if len(cur_nodes)==0: break
			cur_row=' '
			next_row=''
			next_nodes=[]

			if all(n is None for n in cur_nodes):
				break

			for n in cur_nodes:

				if n==None:
					cur_row+='   '+sep
					next_row+='   '+sep
					next_nodes.extend([None,None])
					continue

				if n.word!=None:       
					buf=' '*int((5-len(str(n.word)))/2)
					cur_row+='%s%s%s'%(buf,str(n.word),buf)+sep
				else:
					cur_row+=' '*5+sep

				if n.left_child!=None:  
					next_nodes.append(n.left_child)
					next_row+=' /'+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)

				if n.right_child!=None: 
					next_nodes.append(n.right_child)
					next_row+='\ '+sep
				else:
					next_row+='  '+sep
					next_nodes.append(None)

			content+=(cur_height*'   '+cur_row+'\n'+cur_height*'   '+next_row+'\n')
			cur_nodes=next_nodes
			sep=' '*int(len(sep)/2) # cut separator size in half
		return content

	def insert(self,word):
		"""Called to insert a word into the tree"""
		if self.root==None:
			self.root=node(word)
		else:
			self._insert(word,self.root)

	def _insert(self,word,cur_node):
		"""Called recursively by the base insert function to put word into correct location
			will not insert duplicate words"""
		if word<cur_node.word:
			if cur_node.left_child==None:
				cur_node.left_child=node(word)
				cur_node.left_child.parent=cur_node # set parent
				self._inspect_insertion(cur_node.left_child)
			else:
				self._insert(word,cur_node.left_child)
		elif word>cur_node.word:
			if cur_node.right_child==None:
				cur_node.right_child=node(word)
				cur_node.right_child.parent=cur_node # set parent
				self._inspect_insertion(cur_node.right_child)
			else:
				self._insert(word,cur_node.right_child)
		else:
			print("word already in tree!")

	def print_tree(self):
		if self.root!=None:
			self._print_tree(self.root)

	def _print_tree(self,cur_node):
		if cur_node!=None:
			self._print_tree(cur_node.left_child)
			print ('%s, h=%d'%(str(cur_node.word),cur_node.height))
			self._print_tree(cur_node.right_child)

	def height(self):
		""" called to see if a tree exits, if so recursively calls _height()"""
		if self.root!=None:
			return self._height(self.root,0)
		else:
			return 0

	def _height(self,cur_node,cur_height):
		"""recursive height function continually passes in child nodes until reaching leaf
		   and adds height to node's height parameter. returns greates of left or right path"""
		if cur_node==None: return cur_height
		left_height=self._height(cur_node.left_child,cur_height+1)
		right_height=self._height(cur_node.right_child,cur_height+1)
		return max(left_height,right_height)

	def find(self,word):
		"""Called to find a word in the tree"""
		if self.root!=None:
			return self._find(word,self.root)
		else:
			return None

	def _find(self,word,cur_node):
		"""Called recursively by the base find function to find the word"""
		if word==cur_node.word:
			return cur_node
		elif word<cur_node.word and cur_node.left_child!=None:
			return self._find(word,cur_node.left_child)
		elif word>cur_node.word and cur_node.right_child!=None:
			return self._find(word,cur_node.right_child)

	def delete_word(self,word):
		"""Called to delete a word from the tree"""
		return self.delete_node(self.find(word))

	def delete_node(self,node):
		"""Called recursively by the delete_word function to delete a node with the word
		   uses multiple helper functions to get features of the nodes"""
		# Protect against deleting a node not found in the tree
		if node==None or self.find(node.word)==None:
			print("Node to be deleted not found in the tree!")
			return None 
		
		# returns the node with min word in tree rooted at input node
		def min_word_node(n):
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
			successor=min_word_node(node.right_child)

			# copy the inorder successor's word to the node formerly
			# holding the word we wished to delete
			node.word=successor.word

			# delete the inorder successor now that it's word was
			# copied into the other node
			self.delete_node(successor)

			# exit function so we don't call the _inspect_deletion twice
			return

		if node_parent!=None:
			# fix the height of the parent of current node
			node_parent.height=1+max(self.get_height(node_parent.left_child),self.get_height(node_parent.right_child))

			# begin to traverse back up the tree checking if there are
			# any nodes which now invalidate the AVL balance rules
			self._inspect_deletion(node_parent)

	def search(self,word):
		if self.root!=None:
			return self._search(word,self.root)
		else:
			return False

	def _search(self,word,cur_node):
		if word==cur_node.word:
			return True
		elif word<cur_node.word and cur_node.left_child!=None:
			return self._search(word,cur_node.left_child)
		elif word>cur_node.word and cur_node.right_child!=None:
			return self._search(word,cur_node.right_child)
		return False 

	# Functions for AVL balancing

	def _inspect_insertion(self,cur_node,path=[]):
		if cur_node.parent==None: return
		path=[cur_node]+path

		left_height =self.get_height(cur_node.parent.left_child)
		right_height=self.get_height(cur_node.parent.right_child)

		if abs(left_height-right_height)>1:
			path=[cur_node.parent]+path
			self._rebalance_node(path[0],path[1],path[2])
			return

		new_height=1+cur_node.height 
		if new_height>cur_node.parent.height:
			cur_node.parent.height=new_height

		self._inspect_insertion(cur_node.parent,path)

	def _inspect_deletion(self,cur_node):
		if cur_node==None: return

		left_height =self.get_height(cur_node.left_child)
		right_height=self.get_height(cur_node.right_child)

		if abs(left_height-right_height)>1:
			y=self.taller_child(cur_node)
			x=self.taller_child(y)
			self._rebalance_node(cur_node,y,x)

		self._inspect_deletion(cur_node.parent)

	def _rebalance_node(self,z,y,x):
		if y==z.left_child and x==y.left_child:
			self._right_rotate(z)
		elif y==z.left_child and x==y.right_child:
			self._left_rotate(y)
			self._right_rotate(z)
		elif y==z.right_child and x==y.right_child:
			self._left_rotate(z)
		elif y==z.right_child and x==y.left_child:
			self._right_rotate(y)
			self._left_rotate(z)
		else:
			raise Exception('_rebalance_node: z,y,x node configuration not recognized!')

	def _right_rotate(self,z):
		sub_root=z.parent 
		y=z.left_child
		t3=y.right_child
		y.right_child=z
		z.parent=y
		z.left_child=t3
		if t3!=None: t3.parent=z
		y.parent=sub_root
		if y.parent==None:
				self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y		
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))

	def _left_rotate(self,z):
		sub_root=z.parent 
		y=z.right_child
		t2=y.left_child
		y.left_child=z
		z.parent=y
		z.right_child=t2
		if t2!=None: t2.parent=z
		y.parent=sub_root
		if y.parent==None: 
			self.root=y
		else:
			if y.parent.left_child==z:
				y.parent.left_child=y
			else:
				y.parent.right_child=y
		z.height=1+max(self.get_height(z.left_child),
			self.get_height(z.right_child))
		y.height=1+max(self.get_height(y.left_child),
			self.get_height(y.right_child))

	def get_height(self,cur_node):
		if cur_node==None: return 0
		return cur_node.height

	def taller_child(self,cur_node):
		left=self.get_height(cur_node.left_child)
		right=self.get_height(cur_node.right_child)
		return cur_node.left_child if left>=right else cur_node.right_child
	
#Methods to generate .dot file for use by GraphViz to visualize tree structure.
	#Credit to Terry Griffin via Tina Johnson
	def graphviz_get_ids(self, node, viz_out):
		"""This method does an in-order read of the tree and create the node in the graphviz format"""
		if node:
			self.graphviz_get_ids(node.left_child, viz_out)
			viz_out.write(" node{} [label=\"{}-{}, H={}, BF={}\"];\n".format(node.node_id, node.node_id, node.word, node.height, node.balance_factor))
			self.graphviz_get_ids(node.right_child, viz_out)
		
	def graphviz_make_connections(self, node, viz_out):
		""" this method creates the connections between the existing nodes and addes them to the graphviz format"""
		if node:
			if node.left_child:
				viz_out.write("  node{} -> node{};\n".format(node.node_id, node.left_child.node_id))
				self.graphviz_make_connections(node.left_child, viz_out)
			if node.right_child:
				viz_out.write("  node{} -> node{};\n".format(node.node_id, node.right_child.node_id))
				self.graphviz_make_connections(node.right_child, viz_out)
				
	def graphviz_out(self,filename):
		"""This is the parent method to call on the tree root to produce the graphviz .dot file"""
		with open(filename, 'w') as viz_out:
			viz_out.write("digraph g { \n")
			self.graphviz_get_ids(self.root, viz_out)
			self.graphviz_make_connections(self.root, viz_out)
			viz_out.write("} \n")
	
avl=AVLTree()
#read in random words from text file and insert into tree
with open('words_25.txt','r') as file:
    for word in file:
        avl.insert(word.strip().lower())


avl.print_tree()


