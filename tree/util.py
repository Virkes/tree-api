from tree.models import Node
from sqlalchemy import select, func
from tree.db import db

def is_descendant(node_id, potential_parent_id):
    current = Node.query.get(potential_parent_id)

    while current is not None:
        if current.id == node_id:
            return True
        current = current.parent

    return False


def find_next_ordering(parent_node_id):
    next_ordering = (
        db.session.execute(
            select(func.coalesce(func.max(Node.ordering), -1))
            .where(Node.parent_node_id == parent_node_id)
        )
        .scalar() + 1
        )
    
    return next_ordering