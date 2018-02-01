class node:
    """
    This is the class that defines the structure of each node in the tree
    """

    def __init__(self, val=None):
        """
        The constructor that initializes the node.
        Args:
            val: String
        """
        self.value = val


class tree:
    """
    The Class that is used to maintain the tree.
    """

    def __init__(self):
        """
        The constructor that initializes the tree.
        """
        self.root = None
