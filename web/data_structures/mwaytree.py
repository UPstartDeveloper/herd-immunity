#!python3
'''
Credit to Alan Davis for providing the starter code used in implementing
this class:
https://github.com/Make-School-Courses/CS-2.1-Trees-Sorting/blob/master/Code/prefixtree.py
'''
from .mwaytreenode import MWayTreeNode
from queue import Queue


class MWayTree:
    """MWayTree: subclass of PrefixTree, where each node stores the
       full, unique id number of a person in the Experiment.

    """
    START = 'Virus'

    def __init__(self, virus_name=None, ids=None):
        """Initialize this prefix tree and insert the given ids, if any."""
        # Create a new root node with the start character
        if virus_name is None:
            virus_name = MWayTree.START
        self.root = MWayTreeNode(virus_name)
        # Count the number of ids inserted into the tree
        self.size = 0
        # Insert each id, if any were given
        if ids is not None:
            for id in ids:
                self.insert(virus_name, id)

    def contains(self, id):
        '''Return True if this prefix tree contains the given id.'''
        ids = self.ids()
        # see if id matches the values of any of the nodes
        for node in ids:
            if id == node.character:
                return True
        return False

    def is_empty(self):
        """Return True if this prefix tree is empty (contains no strings).

           Runtime Complexity:
           O(1), because the lookup and comparision
           operations do not change in duration.

        """
        return (self.size == 0)

    def insert(self, parent_id, child_id):
        '''Insert a new child node into the tree.'''
        # make sure the child_id not already in the tree
        if self.contains(child_id) is False:
            # increment size of the tree
            self.size += 1
            # find the node to start adding new id under
            parent_node = self._find_node(parent_id)
            assert parent_node is not None
            # add the newly infected person's id in
            child_node = MWayTreeNode(child_id)
            parent_node.add_child(child_id, child_node)

    def _find_node(self, id):
        """Return the node storing the id, and the depth
           that was searched to find the value in the tree.
           Traversal performed using breadth first search.


        """
        if not self.is_empty():
            # Traverse tree level-order from root, appending each node's item
            queue = Queue()
            # Enqueue given starting node
            queue.put(self.root)
            # Loop until queue is empty
            while not queue.qsize() == 0:
                # Dequeue node at front of queue
                node = queue.get()
                # check if this is the node we're looking for
                node_id = node.character
                if node_id == id:
                    return node
                # Enqueue the node's children as well
                for next_node in node.children:
                    queue.put(node.children[next_node])
        # Return None if the node is not found
        return None

    def _traverse_pre_order(self, node, id, visit):
        """Traverse this prefix tree with recursive depth-first traversal.
           Start at the given node with the given prefix representing its path
           in this prefix tree and visit each node with the given visit
           function.

        """
        if node is not None:
            # Visit this node's data with given function
            visit(node.character)
            # Traverse the subtrees of all the children
            for next_id in node.children:
                self._traverse_pre_order(node.children[next_id], id, visit)

    def complete(self, id):
        """Return a list of all ids that fall under a specific id.

        """
        # Create a list of completions in prefix tree
        completions = []
        # init node to start traversal from
        node = self._find_node(id)
        # if node has an empty string, there are no completions
        if node is not None:
            self._traverse_pre_order(node, id, completions.append)
        # add remove words equal to the prefix
        return completions

    def _traverse_level_order(self, start_node, visit):
        """Traverse this binary tree with iterative level-order traversal
           (BFS). Start at the given node and visit each node with the given
           function.

       """
        # Create queue to store nodes not yet traversed in level-order
        queue = Queue()
        # Enqueue given starting node
        queue.put(start_node)
        # Loop until queue is empty
        while not queue.qsize() == 0:
            # Dequeue node at front of queue
            node = queue.get()
            # Visit the node
            visit(node)
            # Enqueue the node's children as well
            for next_node in node.children:
                queue.put(node.children[next_node])

    def ids(self):
        """Return a list of all ids stored in this prefix tree.
           Implements breadth first search.

        """
        # Create a list of all ids in prefix tree
        all_ids = []
        self._traverse_level_order(self.root, all_ids.append)
        print(all_ids)
        return all_ids


# test script for PrefixTree class
def create_prefix_tree(strings):
    print(f'strings: {strings}')

    tree = PrefixTree()
    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')
    print(f'strings: {tree.strings()}')

    print('\nInserting strings:')
    for string in strings:
        tree.insert(string)
        print(f'insert({string!r}), size: {tree.size}')

    print(f'\ntree: {tree}')
    print(f'root: {tree.root}')

    print('\nSearching for strings in tree:')
    for string in sorted(set(strings)):
        result = tree.contains(string)
        print(f'contains({string!r}): {result}')

    print('\nSearching for strings not in tree:')
    prefixes = sorted(set(string[:len(string)//2] for string in strings))
    for prefix in prefixes:
        if len(prefix) == 0 or prefix in strings:
            continue
        result = tree.contains(prefix)
        print(f'contains({prefix!r}): {result}')

    print('\nCompleting prefixes in tree:')
    for prefix in prefixes:
        completions = tree.complete(prefix)
        print(f'complete({prefix!r}): {completions}')

    print('\nRetrieving all strings:')
    retrieved_strings = tree.strings()
    print(f'strings: {retrieved_strings}')
    matches = set(retrieved_strings) == set(strings)
    print(f'matches? {matches}')


def main():
    # Simpe test case of string with partial substring overlaps
    strings = ['ABC', 'ABD', 'A', 'XYZ']
    create_prefix_tree(strings)

    # Create a dictionary of tongue-twisters with similar words to test with
    tongue_twisters = {
        'Seashells': 'Shelly sells seashells by the sea shore'.split(),
        'Peppers': 'Peter Piper picked a peck of pickled peppers'.split(),
        'Woodchuck': ('How much wood would a wood chuck chuck'
                      ' if a wood chuck could chuck wood').split()
    }
    # Create a prefix tree with the similar words in each tongue-twister
    for name, strings in tongue_twisters.items():
        print(f'{name} tongue-twister:')
        create_prefix_tree(strings)
        if len(tongue_twisters) > 1:
            print('\n' + '='*80 + '\n')


if __name__ == '__main__':
    main()  # script used to test if PrefixTree works with expected test inputs
