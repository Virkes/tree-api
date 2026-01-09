from tree.db import db
from tree.models import Node
from sqlalchemy import func, select
from tree.util import is_descendant, find_next_ordering
from tree.app import ROOT_NODE_ID


def create_node(title, parent_node_id):
    parent = Node.query.get(parent_node_id)
    if parent is None:
        raise ValueError("Parent node does not exist")

    next_ordering = find_next_ordering(parent_node_id)

    node = Node(
        title=title,
        parent_node_id=parent_node_id,
        ordering=next_ordering
    )

    db.session.add(node)
    db.session.commit()

    return node

def change_node_title(node_id, new_title):
    node = Node.query.get(node_id)

    if node is None:
        raise ValueError("Node not found")

    node.title = new_title
    db.session.commit()

    return node

def delete_node(node_id: int):

    if node_id==ROOT_NODE_ID:
        raise ValueError("Root node cannot be deleted")
    
    node = Node.query.get(node_id)

    if node is None:
        raise ValueError("Node not found")

    db.session.delete(node)
    db.session.commit()



def move_node(node_id, new_parent_id):
    if node_id == ROOT_NODE_ID:
        raise PermissionError("Root node cannot be moved")

    if node_id == new_parent_id:
        raise ValueError("Node cannot be its own parent")

    node = Node.query.get(node_id)
    if node is None:
        raise ValueError("Node not found")

    new_parent = Node.query.get(new_parent_id)
    if new_parent is None:
        raise ValueError("New parent does not exist")

    if is_descendant(node_id, new_parent_id):
        raise ValueError("Cannot move node into its own subtree")

    next_ordering = find_next_ordering(new_parent_id)

    node.parent_node_id = new_parent_id
    node.ordering = next_ordering

    db.session.commit()

    return node

def reorder_node(node_id: int, new_order: int):
    node = Node.query.get(node_id)
    if node is None:
        raise ValueError("Node not found")

    if node.parent_node_id is None:
        raise PermissionError("Root node cannot be reordered")

    parent_id = node.parent_node_id

    siblings = (
        Node.query
        .filter(Node.parent_node_id == parent_id)
        .order_by(Node.ordering)
        .all()
    )

    if new_order < 0 or new_order >= len(siblings):
        raise ValueError("newIndex out of range")

    siblings = [n for n in siblings if n.id != node_id]

    siblings.insert(new_order, node)

    for idx, sibling in enumerate(siblings):
        sibling.ordering = idx

    db.session.commit()

    return siblings