#!python3
'''
Credit to Alan Davis for providing the starter code used in implemennting
this class:
https://github.com/Make-School-Courses/CS-2.1-Trees-Sorting/blob/master/Code/prefixtree.py
'''
from prefixtreenode import PrefixTreeNode


class PrefixTree:
    """PrefixTree: A multi-way prefix tree that stores strings with efficient
       methods to insert a string into the tree, check if it contains a
       matching string, and retrieve all strings that start with a given prefix
       string.

       Time complexity of these methods depends only on the number of strings
       retrieved and their maximum length (size and height of subtree
       searched), but is independent of the number of strings stored in the
       prefix tree, as its height depends only on the length of the longest
       string stored in it.

       This makes a prefix tree effective for spell-checking and
       autocompletion. Each string is stored as a sequence of characters along
       a path from the tree's root node to a terminal node that marks the end
       of the string.

    """

    # Constant for the start character stored in the prefix tree's root node
    START_CHARACTER = ''

    def __init__(self, strings=None):
        """Initialize this prefix tree and insert the given strings, if any."""
        # Create a new root node with the start character
        self.root = PrefixTreeNode(PrefixTree.START_CHARACTER)
        # Count the number of strings inserted into the tree
        self.size = 0
        # Insert each string, if any were given
        if strings is not None:
            for string in strings:
                self.insert(string)

    def __repr__(self):
        """Return a string representation of this prefix tree."""
        return f'PrefixTree({self.strings()!r})'

    def is_empty(self):
        """Return True if this prefix tree is empty (contains no strings).

           Runtime Complexity:
           O(1), because the lookup and comparision
           operations do not change in duration.

        """
        return (self.size == 0)

    def contains(self, string):
        """Return True if this prefix tree contains the given string.

           Runtime Complexity:
           O(m), where m is the length of the string being searched.
           The runtime of this method scales asymptotically on the time it
           takes to traverse the tree, down the path of its longest string.

        """
        node, length = self._find_node(string)
        return length == len(string) and node.is_terminal()

    def insert(self, string):
        """Insert the given string into this prefix tree.
           Runtime Complexity:
           O((nm) + (np)), where n is the size of the trie, m is the length of
           string being searched as we look for a duplicate, and p is the
           length of the string being nserted. This runtime depends on calling
           the contains() method.
           In the average case it will then also insert the new string, an
           operation which the runtime depends on thethe size of the trie
           (i.e. the number of strings already being stored) because will
           increase the time we spend looking amongst the children of the root
           node. Also, this second step depends on the length of the new string
           being added.

        """
        # make sure the string not already in the tree
        if self.contains(string) is False:
            # find the node to start adding new letters from
            current_node, index = self._find_node(string)
            # for each index position in the string greater than index
            for i in range(index, len(string)):
                # returned, add a new child node of the node returned
                next_char = string[i]
                new_node = PrefixTreeNode(next_char)
                current_node.add_child(next_char, new_node)
                # then move the current node to its child
                current_node = new_node
            # mark the last node to be added as terminal
            current_node.terminal = True
            # increment size of the tree
            self.size += 1

    def _find_node(self, string):
        """Return a pair containing the deepest node in this prefix tree that
           matches the longest prefix of the given string and the node's depth.
           The depth returned is equal to the number of prefix characters
           matched. Search is done iteratively with a loop starting from the
           root node.

           Runtime Complexity:
           The runtime of the is method linearly with the size of the string
           being search. This can be expressed as O(m), where m is the length
           of the longest string stored in the trie.

        """
        # Match the empty string
        if len(string) == 0:
            return self.root, 0
        # Start with the root node
        node = self.root
        # loop through the letters in string
        index = 0
        # on each iteration see it that letter is a child of node
        while index < len(string) and node.has_child(string[index]) is True:
            # if it is, then move node to that child, and move to next char
            node = node.get_child(string[index])
            index += 1
        # return the pair of the node and the index
        return node, index

    def complete(self, prefix):
        """Return a list of all strings stored in this prefix tree that start
           with the given prefix string.

           Runtime Complexity:
           The runtime of this method depends on the length of the prefix
           given. If there are many possible strings to form based off the
           prefix, then the runtime depends on O(n * (m - prefix)), where n is
           the number of retrieved for completion, and (m - prefix)
           represents the number of strings that are yet to be found in each
           completed word. In the best case we are given a long prefix for the
           longest string in the trie, so there less strings we need to create
           completions of - in this case the runtime tends towards
           O(m - prefix).

        """
        # Create a list of completions in prefix tree
        completions = []
        # Make sure user is not looking for all strings
        if prefix == '':
            return self.strings()
        # init node to start traversal from
        node = self._find_node(prefix)[0]
        # if node has an empty string, there are no completions
        if node.character != '':
            self._traverse(node, prefix, completions.append)
        # add remove words equal to the prefix
        return completions

    def strings(self):
        """Return a list of all strings stored in this prefix tree.

          Runtime Complexity:
          This method performs a depth first traversal from the root, meaning
          that will have to visit all the nodes. This number will depend on
          the number of strings we have stored in the trie, as well as their
          lengths. This runtime will therefore grow asymptotically on the order
          of O(n * m), where n is the size of the trie, and m average length of
          the strings.

        """
        # Create a list of all strings in prefix tree
        all_strings = []
        self._traverse(self.root, '', all_strings.append)
        return all_strings

    def _traverse(self, node, prefix, visit):
        """Traverse this prefix tree with recursive depth-first traversal.
           Start at the given node with the given prefix representing its path
           in this prefix tree and visit each node with the given visit
           function.

           Runtime Complexity:
           The runtime of this method grows with respect to the number of
           strings we need to traverse, as well as the length of each of the
           strings. This will be give or take O(m * n), where m is the length
           of the longest string, and n is the number of retrieved strings.
           In the best case, the prefixes in the longest string will actually
           be the other, smaller strings, which will decrease the runtime by
           reducing the number of times we need to recursively invoke this
           method. In that scenario, the runtime tends towards O(m).

        """
        if node.is_terminal() is True and len(node.children) == 0:
            # add the prefix phrase we've built so far
            visit(prefix)
        elif node.is_terminal() is True:
            # add the prefix phrase we've built so far, and keep moving down
            visit(prefix)
        for char in node.children.keys():
            # move to the child node, continually build the string in traversal
            child = node.get_child(char)
            string = self._traverse(child, prefix + char, visit)

    def delete(self, key):
        """Removes all nodes containing letters of the given key to delete.
           Other keys whose keys are destroyed in the process are then
           re-inserted.

           Parameters:
           key(str): the entry being deleted from the trie.

           Returns: None

           Complexity Analysis:
           The runtime of this method asymptotically increases with the time it
           takes to check all strings in the tree, so that we know that the key
           is even a valid input. After that, we must also traverse the key to
           set the .terminal property of its last node to False, so that the
           whole string will no longer be found during depth first searches.
           The runtime of the second step asymptotically grows with the length
           of the key being deleted. Overall the runtime of this method can be
           expressed as O(k + (n * m)), where k is the length of the string
           being deleted, and (n * m) represents the time it takes to check if
           the input string is contained within the trie. In the worst case
           scenario, the key (aka string) being deleted is also the longest
           string in the data structure.

        """
        if self.contains(key) is True:  # O(m * n)
            # set the node at the end of key no longer signal end of a node
            last_node, depth = self._find_node(key[-1])  # O(m)
            last_node.terminal = False
            # decrement size of tree
            self.size -= 1
        else:  # key is not actually in the prefix tree
            raise ValueError('Word is not found and cannot be deleted.')


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
    main()
