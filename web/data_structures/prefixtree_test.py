#!python3
'''
Credit to Alan Davis for providing the starter code used in implementing
this test suite:
https://github.com/Make-School-Courses/CS-2.1-Trees-Sorting/blob/master/Code/prefixtree_test.py
'''
from .prefixtree import PrefixTree, PrefixTreeNode, CompactPrefixTree
import unittest


class PrefixTreeStringTest(unittest.TestCase):

    def test_init_and_properties(self):
        tree = PrefixTree()
        # Verify tree size property
        assert isinstance(tree.size, int)
        assert tree.size == 0
        # Verify root node
        assert isinstance(tree.root, PrefixTreeNode)
        assert tree.root.character == PrefixTree.START_CHARACTER
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 0

    def test_init_with_string(self):
        tree = PrefixTree(['A'])
        # Verify root node
        assert tree.root.character == PrefixTree.START_CHARACTER
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child('A') is True
        # Verify node 'A'
        node_0 = tree.root.get_child('A')
        assert node_0.character == 'A'
        assert node_0.is_terminal() is True
        assert node_0.num_children() == 0

    def test_insert_with_string(self):
        tree = PrefixTree()
        tree.insert('AB')
        # Verify root node
        assert tree.root.character == PrefixTree.START_CHARACTER
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child('A') is True
        # Verify node 'A'
        node_0 = tree.root.get_child('A')
        assert node_0.character == 'A'
        assert node_0.is_terminal() is False
        assert node_0.num_children() == 1
        assert node_0.has_child('B') is True
        # Verify node 'B'
        node_B = node_0.get_child('B')
        assert node_B.character == 'B'
        assert node_B.is_terminal() is True
        assert node_B.num_children() == 0

    def test_insert_with_4_strings(self):
        tree = PrefixTree()
        # Insert new string that starts from root node
        tree.insert('ABC')
        # Verify root node
        assert tree.root.character == PrefixTree.START_CHARACTER
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child('A') is True
        # Verify new node 'A'
        node_0 = tree.root.get_child('A')
        assert node_0.character == 'A'
        assert node_0.is_terminal() is False
        assert node_0.num_children() == 1
        assert node_0.has_child('B') is True
        # Verify new node 'B'
        node_B = node_0.get_child('B')
        assert node_B.character == 'B'
        assert node_B.is_terminal() is False
        assert node_B.num_children() == 1
        assert node_B.has_child('C') is True
        # Verify new node 'C'
        node_C = node_B.get_child('C')
        assert node_C.character == 'C'
        assert node_C.is_terminal() is True
        assert node_C.num_children() == 0

        # Insert string with partial overlap so node 'B' has new child node 'D'
        tree.insert('ABD')
        # Verify root node again
        assert tree.root.character == PrefixTree.START_CHARACTER
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child('A') is True
        # Verify node 'A' again
        assert node_0.character == 'A'
        assert node_0.is_terminal() is False
        assert node_0.num_children() == 1
        assert node_0.has_child('B') is True
        # Verify node 'B' again
        assert node_B.character == 'B'
        assert node_B.is_terminal() is False
        assert node_B.num_children() == 2  # Node 'B' now has two children
        assert node_B.has_child('C') is True  # Node 'C' is still its child
        assert node_B.has_child('D') is True  # Node 'D' is its new child
        # Verify new node 'D'
        node_D = node_B.get_child('D')
        assert node_D.character == 'D'
        assert node_D.is_terminal() is True
        assert node_D.num_children() == 0

        # Insert substring already in tree so node 'A' becomes terminal
        tree.insert('A')
        # Verify root node again
        assert tree.root.character == PrefixTree.START_CHARACTER
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child('A') is True
        # Verify node 'A' again
        assert node_0.character == 'A'
        assert node_0.is_terminal() is True  # Node 'A' is now terminal
        assert node_0.num_children() == 1  # Node 'A' still has one child
        assert node_0.has_child('B') is True  # Node 'B' is still its child

        # Insert new string with no overlap that starts from root node
        tree.insert('XYZ')
        # Verify root node again
        assert tree.root.character == PrefixTree.START_CHARACTER
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 2  # Root node now has two children
        assert tree.root.has_child('A') is True  # Node 'A' is still its child
        assert tree.root.has_child('X') is True  # Node 'X' is its new child
        # Verify new node 'X'
        node_X = tree.root.get_child('X')
        assert node_X.character == 'X'
        assert node_X.is_terminal() is False
        assert node_X.num_children() == 1
        assert node_X.has_child('Y') is True
        # Verify new node 'Y'
        node_Y = node_X.get_child('Y')
        assert node_Y.character == 'Y'
        assert node_Y.is_terminal() is False
        assert node_Y.num_children() == 1
        assert node_Y.has_child('Z') is True
        # Verify new node 'Z'
        node_Z = node_Y.get_child('Z')
        assert node_Z.character == 'Z'
        assert node_Z.is_terminal() is True
        assert node_Z.num_children() == 0

    def test_size_and_is_empty(self):
        tree = PrefixTree()
        # Verify size after initializing tree
        assert tree.size == 0
        assert tree.is_empty() is True
        # Verify size after first insert
        tree.insert('A')
        assert tree.size == 1
        assert tree.is_empty() is False
        # Verify size after second insert
        tree.insert('ABC')
        assert tree.size == 2
        assert tree.is_empty() is False
        # Verify size after third insert
        tree.insert('ABD')
        assert tree.size == 3
        assert tree.is_empty() is False
        # Verify size after fourth insert
        tree.insert('XYZ')
        assert tree.size == 4
        assert tree.is_empty() is False
        # Verify that size still increases by 1 when spaces included in string
        tree.insert('WAFFLE TIME')
        assert tree.size == 5
        assert tree.is_empty() is False

    def test_size_with_repeated_insert(self):
        tree = PrefixTree()
        # Verify size after initializing tree
        assert tree.size == 0
        assert tree.is_empty() is True
        # Verify size after first insert
        tree.insert('A')
        assert tree.size == 1
        assert tree.is_empty() is False
        # Verify size after repeating first insert
        tree.insert('A')
        assert tree.size == 1
        # Verify size after second insert
        tree.insert('ABC')
        assert tree.size == 2
        # Verify size after repeating second insert
        tree.insert('ABC')
        assert tree.size == 2
        # Verify size after third insert
        tree.insert('ABD')
        assert tree.size == 3
        # Verify size after repeating third insert
        tree.insert('ABD')
        assert tree.size == 3
        # Verify size after fourth insert
        tree.insert('XYZ')
        assert tree.size == 4
        # Verify size after repeating fourth insert
        tree.insert('XYZ')
        assert tree.size == 4

    def test_contains(self):
        strings = ['ABC', 'ABD', 'A', 'XYZ']
        tree = PrefixTree(strings)
        # Verify contains for all substrings
        assert tree.contains('ABC') is True
        assert tree.contains('ABD') is True
        assert tree.contains('AB') is False
        assert tree.contains('BC') is False
        assert tree.contains('BD') is False
        assert tree.contains('A') is True
        assert tree.contains('B') is False
        assert tree.contains('C') is False
        assert tree.contains('D') is False
        assert tree.contains('XYZ') is True
        assert tree.contains('XY') is False
        assert tree.contains('YZ') is False
        assert tree.contains('X') is False
        assert tree.contains('Y') is False
        assert tree.contains('Z') is False

    def test_complete(self):
        strings = ['ABC', 'ABD', 'A', 'XYZ']
        tree = PrefixTree(strings)
        # Verify completions for all substrings
        assert tree.complete('ABC') == ['ABC']
        assert tree.complete('ABD') == ['ABD']
        assert tree.complete('AB') == ['ABC', 'ABD']
        assert tree.complete('BC') == []
        assert tree.complete('BD') == []
        assert tree.complete('A') == ['A', 'ABC', 'ABD']
        assert tree.complete('B') == []
        assert tree.complete('C') == []
        assert tree.complete('D') == []
        assert tree.complete('XYZ') == ['XYZ']
        assert tree.complete('XY') == ['XYZ']
        assert tree.complete('YZ') == []
        assert tree.complete('X') == ['XYZ']
        assert tree.complete('Y') == []
        assert tree.complete('Z') == []
        # Verify empty prefix string as input - aka "suggestions" feature
        completions_with_empty_string = tree.complete('')
        # Check length only
        assert len(completions_with_empty_string) == len(strings)
        # Ignore order
        self.assertCountEqual(completions_with_empty_string, strings)

    def test_strings(self):
        tree = PrefixTree()
        input_strings = []  # Strings that have been inserted into the tree
        for string in ['ABC', 'ABD', 'A', 'XYZ']:  # Strings to be inserted
            # Insert new string and add to list of strings already inserted
            tree.insert(string)
            input_strings.append(string)
            # Verify tree can retrieve all strings that have been inserted
            tree_strings = tree.strings()
            assert len(tree_strings) == len(input_strings)  # Check length only
            self.assertCountEqual(tree_strings, input_strings)  # Ignore order

    def test_strings_when_string_include_spaces(self):
        tree = PrefixTree()
        input_strings = []  # Strings that have been inserted into the tree
        for string in ['ABC', 'ABD', 'A', 'XYZ', "WAFFLE TIME"]:
            # Insert new string and add to list of strings already inserted
            tree.insert(string)
            input_strings.append(string)
            # Verify tree can retrieve all strings that have been inserted
            tree_strings = tree.strings()
            assert len(tree_strings) == len(input_strings)  # Check length only
            self.assertCountEqual(tree_strings, input_strings)  # Ignore order

    def test_delete_key_shares_prefix_with_other_strings(self):
        """
        A string is deleted from the trie without removing strings that contain
        the same prefix.
        """
        # Make the tree
        input = ['ABC', 'ABD', 'A', 'XYZ', "WAFFLE TIME"]
        tree = PrefixTree(input)
        # Remove a string who shares letters with other strings
        tree.delete('A')
        # test the length of trie is adjusted correctly
        assert tree.size == len(input) - 1
        # test all the other strings with common nodes can still be found
        assert tree.contains('ABC') is True
        assert tree.contains('ABD') is True
        # test that the deleted string cannot be found
        assert tree.contains('A') is False

    def test_delete_from_empty_trie(self):
        """
        If string cannot be found, a ValueError is raised.
        """
        # Make the tree
        tree = PrefixTree()
        # raise Exception
        with self.assertRaises(ValueError):
            tree.delete('CS Rocks!')


class CompactPrefixTreeTest(unittest.TestCase):

    def test_init_and_properties(self):
        tree = CompactPrefixTree()
        # Verify tree size property
        assert isinstance(tree.size, int)
        assert tree.size == 0
        # Verify root node
        assert isinstance(tree.root, PrefixTreeNode)
        assert tree.root.character == CompactPrefixTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 0

    def test_init_with_integer(self):
        tree = CompactPrefixTree(ids=[0])
        # Verify root node
        assert tree.root.character == CompactPrefixTree.START
        assert tree.root.is_terminal() is False
        assert tree.root.num_children() == 1
        assert tree.root.has_child(0) is True
        # Verify node 0
        node_0 = tree.root.get_child(0)
        assert node_0.character == 0
        assert node_0.is_terminal() is False
        assert node_0.num_children() == 0

    def test_insert_with_integer(self):
        tree = CompactPrefixTree()
        tree.insert('Virus', 0)
        # Verify root node
        assert tree.root.character == CompactPrefixTree.START
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
        tree = CompactPrefixTree()
        # Insert new int that starts from root node
        tree.insert(tree.root.character, 123)
        # Verify root node
        assert tree.root.character == CompactPrefixTree.START
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
        assert tree.root.character == CompactPrefixTree.START
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
        assert tree.root.character == CompactPrefixTree.START
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
        assert tree.root.character == CompactPrefixTree.START
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
        tree = CompactPrefixTree()
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
        tree = CompactPrefixTree()
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
        tree = CompactPrefixTree(ids=ids)
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
        tree = CompactPrefixTree(ids=ids)
        # Verify completions for all integers
        assert tree.complete(CompactPrefixTree.START) == (
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
        assert tree.complete(PrefixTree.START_CHARACTER) == []

    def test_ids(self):
        tree = CompactPrefixTree()
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
