from anytree import Node, RenderTree
from anytree.modifiers import tree_filter


def test_simple():
    tree = Node("root", children=[Node("a"), Node("b"), Node("c")])
    print(RenderTree(tree))
    no_c = tree_filter(tree, lambda n: n.name != "c")
    print(RenderTree(no_c))
    assert len(no_c.children) == 2


def test_remove_subtree():
    tree = Node(
        "root",
        children=[
            Node("a", children=[Node("a"), Node("b"), Node("c")]),
            Node("b", children=[Node("a"), Node("b"), Node("c")]),
            Node("c", children=[Node("a"), Node("b"), Node("c")]),
        ],
    )
    print(RenderTree(tree))
    no_c = tree_filter(tree, lambda n: n.name != "c")
    print(RenderTree(no_c))
    assert len(no_c.children) == 2
    for child in no_c.children:
        assert len(child.children) == 2
