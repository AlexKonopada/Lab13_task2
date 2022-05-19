"""
File: linkedbst.py
Author: Ken Lambert
"""
import random
import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log
import sys

sys.setrecursionlimit(11000)

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = 'L'
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = 'L'
                currentNode = currentNode.left
            else:
                direction = 'R'
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None \
                and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0

            if top.right is not None:
                right_height = height1(top.right)
            else:
                right_height = -1

            if top.left is not None:
                left_height = height1(top.left)
            else:
                left_height = -1

            return max(right_height, left_height) + 1

        return height1(self._root)
            
        
    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        nodes = len(list(self.inorder()))
        return self.height() < 2 * log(nodes+1, 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        nodes = sorted(list(self.inorder()))
        lst = []
        for i in range(len(nodes)):
            if low <= nodes[i] <= high:
                lst.append(nodes[i])
        return lst

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        nodes = self.inorder()
        def rebalance1(nodes):
            if len(nodes) == 0:
                return None
            i = len(list(nodes)) // 2

            cental_node = BSTNode(nodes[i])
            cental_node.right = rebalance1(nodes[i+1:])
            cental_node.left = rebalance1(nodes[:i])
            return cental_node
        self._root =  rebalance1(list(nodes))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        nodes = sorted(list(self.inorder()))
        if nodes[-1] == item or item > nodes[-1]:
            return None
        else:
            for i in range(len(nodes)):
                if nodes[i] > item:
                    return nodes[i]
                    
    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        
        nodes = sorted(list(self.inorder()))
        for i in range(len(nodes)-1, -1, -1):
            if item > nodes[i]:
                return nodes[i]
                    
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, encoding='utf-8') as f:
            all_words = f.read().splitlines()
        random_10000 = random.sample(all_words, 10000)
        
        #list 
        start_time_lst = time.time()

        for i in range(len(random_10000)): 
            random_10000.index(random_10000[i])

        end_time_lst = time.time()

        time_spent_lst = end_time_lst - start_time_lst

        print("Time spent for finding 10000 words in a random list: ", time_spent_lst)

        #ordered tree

        ordered_tree = LinkedBST()

        for j in range(10000):
            ordered_tree.add(all_words[j].lower())
        
        ordered_bst_start_time = time.time()

        for j in range(10000):
            ordered_tree.find(all_words[j])

        ordered_bst_end_time = time.time()
        ordered_bst_spent_time = ordered_bst_end_time - ordered_bst_start_time
        print("Time spent for finding 10000 words in a ordered binary search tree: ", ordered_bst_spent_time)
        
        #inordered tree
        inordered_tree = LinkedBST()

        for idx in range(len(random_10000)):
            inordered_tree.add(random_10000[idx])
        inordered_bst_start_time = time.time()

        for idx in range(len(random_10000)):
            inordered_tree.find(random_10000[idx])

        inordered_bst_end_time = time.time()
        inordered_bst_spent_time = inordered_bst_end_time - inordered_bst_start_time
        print("Time spent for finding 10000 words in a inordered binary search tree: ", inordered_bst_spent_time)
        
        # balanced
        inordered_tree.rebalance()

        balanced_bst_start_time = time.time()

        for idx2 in range(len(random_10000)):
            inordered_tree.find(random_10000[idx2])

        balanced_bst_end_time = time.time()
        balanced_bst_spent_time = balanced_bst_end_time - balanced_bst_start_time
        print("Time spent for finding 10000 words in a balanced binary search tree: ", balanced_bst_spent_time)
        
if __name__ == '__main__':
    lbst = LinkedBST()
    print(lbst.demo_bst('/home/alex/Desktop/labs/Lab13/task1/words.txt'))