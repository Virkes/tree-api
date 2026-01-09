from tree.models import Node

def node_to_dto(node: Node):
    return {
        "id": node.id,
        "title": node.title,
        "ordering": node.ordering,
        "parentNodeId": node.parent_node_id
    }
