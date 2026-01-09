from flask import Blueprint, jsonify, abort, request
from tree.models import Node
from tree.schemas import node_to_dto
from tree.services import create_node, change_node_title, delete_node, move_node, reorder_node

nodes = Blueprint("nodes", __name__, url_prefix="/nodes")

@nodes.route("/", methods=["GET"])
def get_all_nodes():
    nodes = Node.query.all()

    return jsonify([node_to_dto(e) for e in nodes])

@nodes.route("/<int:parent_node_id>", methods=["POST"])
def create_child_node(parent_node_id):
    data = request.get_json()

    title = data.get("title")

    if not title:
        abort(400, description="title is required")

    try:
        create_node(title, parent_node_id)
    except ValueError as e:
        abort(404, description=str(e))

    return '', 201


@nodes.route("/<int:node_id>", methods=["PUT"])
def update_node(node_id):
    data = request.get_json()

    title = data.get("title")

    if not title:
        abort(400, description="title is required")

    try:
        node = change_node_title(node_id, title)
    except ValueError as e:
        abort(404, description=str(e))

    return jsonify(node_to_dto(node))

@nodes.route("/<int:node_id>", methods=["DELETE"])
def delete_node_endpoint(node_id):
    try:
        delete_node(node_id)
    except ValueError as e:
        abort(403 if "Root" in str(e) else 404, description=str(e))

    return jsonify({"status": "deleted"}), 200


@nodes.route("/<int:node_id>/move", methods=["PUT"])
def move_node_endpoint(node_id):
    data = request.get_json()

    if not data:
        abort(400, description="Invalid JSON")

    new_parent_id = data.get("newParentId")
    if new_parent_id is None:
        abort(400, description="newParentId is required")

    try:
        node = move_node(node_id, new_parent_id)
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(409, description=str(e))

    return jsonify(node_to_dto(node))

@nodes.route("/<int:node_id>/reorder", methods=["PUT"])
def reorder_node_endpoint(node_id):
    data = request.get_json()

    if not data or "newOrder" not in data:
        abort(400, description="newOrder is required")

    try:
        siblings = reorder_node(node_id, data["newOrder"])
    except PermissionError as e:
        abort(403, description=str(e))
    except ValueError as e:
        abort(409, description=str(e))

    return jsonify([node_to_dto(n) for n in siblings])
