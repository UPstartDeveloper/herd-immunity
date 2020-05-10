#!python3
'''
Credit to Alan Davis for providing the starter code used in implementing
this test suite:
https://github.com/Make-School-Courses/CS-2.1-Trees-Sorting/blob/master/Code/prefixtree_test.py
'''
from .mwaytree import MWayTreeNode, MWayTree
import unittest


class MWayTreeTest(unittest.TestCase):

    def test_init_and_properties(self):
        tree = MWayTree()
        # Verify tree size property
        assert isinstance(tree.size, int)
        assert tree.size == 0
        # Verify root node
        assert isinstance(tree.root, MWayTreeNode)
        assert tree.root.character == MWayTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 0

    def test_init_with_integer(self):
        tree = MWayTree(ids=[0])
        # Verify root node
        assert tree.root.character == MWayTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child(0) is True
        # Verify node 0
        node_0 = tree.root.get_child(0)
        assert node_0.character == 0
        assert node_0.is_terminal() is False
        assert node_0.num_children() == 0

    def test_insert_with_integer(self):
        tree = MWayTree()
        tree.insert('Virus', 0)
        # Verify root node
        assert tree.root.character == MWayTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child(0) is True
        # Verify node 0
        node_0 = tree.root.get_child(0)
        assert node_0.character == 0
        assert node_0.is_terminal() is False
        assert node_0.num_children() == 0
        assert node_0.has_child(1) is False

    def test_insert_with_4_integers(self):
        tree = MWayTree()
        # Insert new int that starts from root node
        tree.insert(tree.root.character, 123)
        # Verify root node
        assert tree.root.character == MWayTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child(123) is True
        # Verify new node 123
        node_123 = tree.root.get_child(123)
        assert node_123.character == 123
        assert node_123.is_terminal() is False
        assert node_123.num_children() == 0
        assert node_123.has_child('B') is False

        # Insert int with partial overlap so node 'B' has new child node 'D'
        tree.insert(123, 234)
        # Verify root node again
        assert tree.root.character == MWayTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child(123) is True
        # Verify node 123 again
        assert node_123.character == 123
        assert node_123.is_terminal() is False
        assert node_123.num_children() == 1
        assert node_123.has_child(234) is True

        # Insert another node
        tree.insert('Virus', 456)
        # Verify root node again
        assert tree.root.character == MWayTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 2
        assert tree.root.has_child(123) is True
        assert tree.root.has_child(456) is True
        # Verify node 123 again
        assert node_123.character == 123
        assert node_123.is_terminal() is False
        assert node_123.num_children() == 1  # Node 0 still has one child
        assert node_123.has_child(234) is True

        # Insert new string with no overlap that starts from root node
        tree.insert(456, 567)
        # Verify root node again
        assert tree.root.character == MWayTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 2  # Root node now has two children
        assert tree.root.has_child(123) is True  # Node 0 is still its child
        assert tree.root.has_child(123) is True  # Node 'X' is its new child
        # Verify new node 567
        node_567 = tree.root.get_child(456).get_child(567)
        assert node_567.character == 567
        assert node_567.is_terminal() is False
        assert node_567.num_children() == 0
        assert node_567.has_child(678) is False

    def test_size_and_is_empty(self):
        tree = MWayTree()
        # Verify size after initializing tree
        assert tree.size == 0
        assert tree.is_empty() is True
        # Verify size after first insert
        tree.insert(tree.root.character, 0)
        assert tree.size == 1
        assert tree.is_empty() is False
        # Verify size after second insert
        tree.insert(0, 123)
        assert tree.size == 2
        assert tree.is_empty() is False
        # Verify size after third insert
        tree.insert('Virus', 234)
        assert tree.size == 3
        assert tree.is_empty() is False
        # Verify size after fourth insert
        tree.insert(234, 456)
        assert tree.size == 4
        assert tree.is_empty() is False

    def test_size_with_repeated_insert(self):
        tree = MWayTree()
        # Verify size after initializing tree
        assert tree.size == 0
        assert tree.is_empty() is True
        # Verify size after first insert
        tree.insert(tree.root.character, 0)
        assert tree.size == 1
        assert tree.is_empty() is False
        # Verify size after repeating first insert
        tree.insert(tree.root.character, 0)
        assert tree.size == 1
        # Verify size after second insert
        tree.insert(0, 1)
        assert tree.size == 2
        # Verify size after repeating second insert
        tree.insert(0, 1)
        assert tree.size == 2
        # Verify size after third insert
        tree.insert(1, 2)
        assert tree.size == 3
        # Verify size after repeating third insert
        tree.insert(1, 1)
        assert tree.size == 3
        # Verify size after fourth insert
        tree.insert(1, 2)
        assert tree.size == 3
        # Verify size after repeating fourth insert
        tree.insert(2, 3)
        assert tree.size == 4

    def test_contains(self):
        ids = [123, 234, 456, 567]
        tree = MWayTree(ids=ids)
        # Verify contains for all positive cases
        assert tree.contains(123) is True
        assert tree.contains(234) is True
        assert tree.contains(456) is True
        assert tree.contains(567) is True
        # Verify contains for negative cases
        assert tree.contains('B') is False
        assert tree.contains('C') is False
        assert tree.contains('D') is False

    def test_complete(self):
        ids = [123, 234, 456, 567]
        tree = MWayTree(ids=ids)
        # Verify completions for all integers
        assert tree.complete(MWayTree.START) == (
            ['Virus', 123, 234, 456, 567]
        )
        # Verify completions for 2nd level nodes
        assert tree.complete(123) == [123]
        assert tree.complete(234) == [234]
        assert tree.complete(456) == [456]
        assert tree.complete(567) == [567]
        # Verify completions after additional insertions
        tree.insert(234, 345)
        assert tree.complete(234) == [234, 345]
        # Verify completions on negative case
        assert tree.complete('') == []

    def test_ids(self):
        tree = MWayTree()
        ids = [123, 234, 456, 567]  # Ids to insert into the tree
        for id in ids:
            # Insert new string and add to list of strings already inserted
            tree.insert(tree.root.character, id)
        # Verify tree can retrieve all strings that have been inserted
        tree_ids = tree.ids()
        print(tree_ids)
        assert len(tree_ids) == (len(ids) + 1)  # Check length only
        # Verify all the inputted ids are in the output
        for node in tree_ids[1:]:
            assert node.character in ids


if __name__ == '__main__':
    unittest.main()
