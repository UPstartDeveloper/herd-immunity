#!python3
'''
Credit to Alan Davis for providing the starter code used in implemennting
this class:
https://github.com/Make-School-Courses/CS-2.1-Trees-Sorting/blob/master/Code/prefixtreenode.py
'''


class PrefixTreeNode:
    """PrefixTreeNode: A node for use in a prefix tree that stores a single
       character from a string and a structure of children nodes below it,
       which associates the next character in a string to the next node along
       its path from the tree's root node to a terminal node that marks the end
       of the string.

    """
    # Choose an appropriate type of data structure to store children nodes in
    # Hint: Choosing list or dict affects implementation of all child methods
    CHILDREN_TYPE = dict  # or list

    def __init__(self, character=None):
        """Initialize this prefix tree node with the given character value, an
        empty structure of children nodes, and a boolean terminal property."""
        # Character that this node represents
        self.character = character
        # Data structure to associate character keys to children node values
        self.children = PrefixTreeNode.CHILDREN_TYPE()
        # Marks if this node terminates a string in the prefix tree
        self.terminal = False

    def is_terminal(self):
        """Return True if this prefix tree node terminates a string.

           Runtime Complexity: O(1)

        """
        return (self.terminal is True)

    def num_children(self):
        """Return the number of children nodes this prefix tree node has.

           Runtime Complexity: O(n)

        """
        return len(self.children.keys())

    def has_child(self, character):
        """Return True if this prefix tree node has a child node that
           represents the given character amongst its children.

           Runtime Complexity: O(n)

        """
        return (character in self.children.keys())

    def get_child(self, character):
        """Return this prefix tree node's child node that represents the given
           character if it is amongst its children, or raise ValueError if not.

           Runtime Complexity: O(n)

        """
        if self.has_child(character) is True:
            return self.children.get(character)
        else:
            raise ValueError(f'No child exists for character {character!r}')

    def add_child(self, character, child_node):
        """Add the given character and child node as a child of this node, or
           raise ValueError if given character is amongst this node's children.

           Runtime Complexity: O(n)

        """
        if self.has_child(character) is False:
            self.children[character] = child_node
        else:
            raise ValueError(f'Child exists for character {character!r}')

    def __repr__(self):
        """Return a code representation of this prefix tree node."""
        return f'PrefixTreeNode({self.character!r})'

    def __str__(self):
        """Return a string view of this prefix tree node."""
        return f'({self.character})'