#!python3
'''
Credit to Alan Davis for providing the starter code used in implemennting
this class:
https://github.com/Make-School-Courses/CS-2.1-Trees-Sorting/blob/master/Code/MWayTreeNode.py
'''


class MWayTreeNode:
    """MWayTreeNode: A node for use in a m-way tree that stores a
       single data value. Can have up to (m - 1) siblings.

    """
    # Choose an appropriate data structure to store children nodes in
    CHILDREN_TYPE = dict  # or list

    def __init__(self, id=None):
        """Initialize this m-way tree node with the given id value, an
        empty structure of children nodes."""
        # id that this node represents
        self.id = id
        # Data structure to associate id keys to children node values
        self.children = MWayTreeNode.CHILDREN_TYPE()

    def num_children(self):
        """Return the number of children nodes this m-way tree node has.

           Runtime Complexity: O(n)

        """
        return len(self.children.keys())

    def has_child(self, id):
        """Return True if this m-way tree node has a child node that
           represents the given id amongst its children.

           Runtime Complexity: O(n)

        """
        return (id in self.children.keys())

    def get_child(self, id):
        """Return this m-way tree node's child node that represents the given
           id if it is amongst its children, or raise ValueError if not.

           Runtime Complexity: O(n)

        """
        if self.has_child(id) is True:
            return self.children.get(id)
        else:
            raise ValueError(f'No child exists for id {id!r}')

    def add_child(self, id, child_node):
        """Add the given id and child node as a child of this node, or
           raise ValueError if given id is amongst this node's children.

           Runtime Complexity: O(n)

        """
        if self.has_child(id) is False:
            self.children[id] = child_node
        else:
            raise ValueError(f'Child exists for id {id!r}')

    def __repr__(self):
        """Return a code representation of this m-way tree node."""
        return f'MWayTreeNode({self.id!r})'

    def __str__(self):
        """Return a string view of this m-way tree node."""
        return f'({self.id})'
