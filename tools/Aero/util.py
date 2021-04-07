from lxml import etree


def write_node_path(path_nodes, tree):
    """Writes nodes to tree starting from root."""
    parent = tree.getroot()
    path = "."
    for node in path_nodes:
        path += "/" + node
        check_node = tree.find(path)
        if check_node is None:
            parent.insert(-1, etree.Element(node))
        parent = tree.find(path)


def write_value(node, parent_path, value, tree):
    path = "{}/{}".format(parent_path, node)
    if tree.find(path) is None:
        tree.find(parent_path).insert(-1, etree.Element(node))
    tree.find(path).text = "%f" % value
