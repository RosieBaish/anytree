"""Tree modification."""
import copy

from anytree.node import NodeMixin
from anytree import RenderTree


def tree_filter(node, filter_func=None, deep_copy_func=None):
    """
    Iterate across node and it's children and return a subset of the tree.

    Any node for which filter_func(node) evaluates to false is removed,
    along with it's subtree

    If deep_copy_func is not None, it is called with the old node as the
    first argument and the new node as the second.
    It should perform any required copying from the old node to the new one.

    Note: Any modifications filter_func makes to the note or it's children
    will affect the original node, not the new tree
    """
    if not filter_func(node):
        return None
    new_node = copy.copy(node)

    # NodeMixin uses properties for parent and children
    # We need to modify the underlying data structure to prevent accidentally
    # copying things around, so we mess with the private variables
    # This is horrible, I'm sorry
    new_node._NodeMixin__children = []
    new_node._NodeMixin__parent = None

    if deep_copy_func is not None:
        deep_copy_func(node, new_node)

    children = node.children
    new_children = []

    for child in children:
        new_children.append(tree_filter(child, filter_func, deep_copy_func))

    for (c1, c2) in zip(children, new_children):
        assert id(c1) != id(c2)

    if len(node.children) and len(new_node.children):
        assert id(node.children) != id(new_node.children)

    filtered_children = list(filter(None, new_children))
    new_node.children = filtered_children

    return new_node
